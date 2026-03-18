# coding=utf-8
"""
@Time : 2022/4/15 下午4:19
@Author : HeXW
"""
import json
from back.lib.Manager import Manager
from back.util.CollectUtil import wait


class check:

    def __init__(self, receive_str, manage: Manager, logger):
        self.receive_str = receive_str
        self.manage = manage
        self.logger = logger

    def traverse_take_field(self, data, fields, values={}, currentKey=None):
        """
        遍历嵌套字典列表，取出某些字段的值
        :param data: 嵌套字典列表
        :param fields: 列表，某些字段
        :param values: 返回的值
        :param currentKey: 当前的键值
        :return: 列表
        """
        if isinstance(data, list):
            for i in data:
                self.traverse_take_field(i, fields, values, currentKey)
        elif isinstance(data, dict):
            for key, value in data.items():
                self.traverse_take_field(value, fields, values, key)
        else:
            if isinstance(fields, list):
                if currentKey in fields:
                    values[currentKey] = data
            else:
                if currentKey == fields:
                    values[currentKey] = data
        return values

    def deal_checkParams(self, checkParams: str):
        '''
        :param checkParams: 接口交验的参数 admin=123456
        :return: 字典
        '''

        if checkParams:
            expectParam = {}
            expectList = []
            checklist = str(checkParams).split(',')
            for i in checklist:
                if '=' in i:
                    expectParam[i.split('=')[0]] = i.split('=')[1]
                else:
                    expectList.append(i)
            return expectParam, expectList

    def check_receive_str(self, checkParams):
        if self.receive_str:
            receive_str = json.loads(self.receive_str)
            expectDict, expectList = self.deal_checkParams(checkParams)
            expectKey = []
            for key in expectDict:
                expectKey.append(key)
            actData = self.traverse_take_field(receive_str, expectKey, values={})
            self.logger.info('接口实际返回值：{}'.format(actData))
            self.logger.info('期望值:{}'.format(checkParams))
            if expectDict:
                for key, value in expectDict.items():
                    assert actData != {}
                    assert str(value) == str(actData[key])
                    self.logger.info("效验通过，期望值：{}=实际值:{}".format(value, actData[key]))
            if expectList:
                for i in expectList:
                    assert i in str(receive_str)
                    self.logger.info('校验通过，期望值：{}在返回值中'.format(i))
        else:
            raise CheckerError('接口检查错误，返回数据为空')

    def deal_with_dbChecker(self, sqlCheck):
        sqlList = sqlCheck.split(',') if ',' in sqlCheck else [sqlCheck]
        for eachSqlCheck in sqlList:
            dbDefaultName = 'default'
            if '#' in eachSqlCheck:
                dbDefaultName = sqlCheck.split('#')[0]
            if dbDefaultName not in self.manage.dbObject.db_conn_infos:
                self.manage.initDbObject(dbDefaultName)
            else:
                self.logger.info('数据库别名已在配置当中，直接返回')
            # 判断sql是交验还是赋值
            sql, check_or_param = self.deal_with_sql(eachSqlCheck)
            if sql.lower().startswith('select'):
                # 期望值中带$，表示复值
                if '$' in check_or_param:
                    dic = {}
                    variableKey = check_or_param.replace('$', '')
                    result = self.manage.dbObject.db_execute(sql)
                    if len(result) == 1 and isinstance(result, list):
                        dic[variableKey] = result[0]
                        self.manage.add_global(dic)
                        self.logger.info('数据库赋值完成，已经添加：{}到全局变量'.format(dic))
                        # self.logger.info('全局变量：{}'.format(self.manage.globalDict))
                    else:
                        raise CheckerError('sql查询结果为空或者同时有多个参数赋值')
                else:
                    expectVal = check_or_param
                    self.logger.info('开始执行sql：{}'.format(sql))
                    result = wait(sql, self.manage.dbObject, expectVal, timeOut=2)
                    assert result == 'true'
            else:
                self.logger.info('开始执行sql：{}'.format(sql))
                result = self.manage.dbObject.db_execute(sql)
                self.logger.info(result)
                assert result[0][0] == 1

    def export_Params(self, export_params: str, requestParam):
        params = export_params.split(',')
        if self.receive_str:
            receive_str = json.loads(self.receive_str)
            dic = {}
            # 输出response参数到局部全局变量
            if params:
                val = self.traverse_take_field(receive_str, params, values={})
                dic.update(val)
            # 输出请求参数到局部全局变量
            self.manage.globalDict.update(dic)
            self.logger.info('全局变量设置完成：{}'.format(self.manage.globalDict))
        else:
            # raise CheckerError('接口检查错误，返回数据为空')
            self.export_request_params(requestParam, params)
            self.logger.info('全局变量设置完成：{}'.format(self.manage.globalDict))

    def export_request_params(self, request_param, fields, currentKey=None):
        if isinstance(request_param, list):
            for i in request_param:
                self.export_request_params(i, fields, currentKey)
        elif isinstance(request_param, dict):
            for key, value in request_param.items():
                self.export_request_params(value, fields, key)
        else:
            if currentKey in fields:
                self.manage.globalDict.update({currentKey: request_param})

    def deal_with_sql(self, sql: str):
        sql, expect = sql.split('|')
        expect = expect.strip()
        sqlList = sql.split(' ')
        for i in range(len(sqlList)):
            if sqlList[i].startswith('$'):
                val = sqlList[i].replace('$', '')
                if val in self.manage.globalDict:
                    val = self.manage.globalDict[val]
                    sqlList[i] = repr(val)
                else:
                    raise CheckerError('变量{},不再全局变量中'.format(val))
            if '$' in str(sqlList[i]) and '=' in str(sqlList[i]):
                raise CheckerError('sql书写格式不正确,可能是没有空格{}'.format(sql))
            #     sing_sql = sqlList[i].split('$')
            #     val = sing_sql[1]
            #     if val in self.manage.get_global or val in headerObj_gal.get_global_dict():
            #         if val in self.manage.get_global:
            #             val = self.manage.get_global[val]
            #         else:
            #             val = headerObj_gal.get_value(val)
            #         sing_sql[1] = val
            #         sqlList[i] = ' '.join(sing_sql)
                # else:
                #     raise CheckerError('变量{},不再全局变量中'.format(val))

        sql = ' '.join(sqlList)
        return [sql, expect]


class CheckerError(Exception):
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


if __name__ == '__main__':
    data = 'message=success,token,111dd'
    dic = {'a': 2, 'b': 3, 'c': 4, 'b': 4}
    value = ['e']
    print(check('e').traverse_take_field(dic, value))
