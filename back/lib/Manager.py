# coding=utf-8
"""
@Time : 2021/4/17 下午3:23
@Author : HeXW
"""
from back.util.DbOpen import DbOpen


class Manager:
    def __init__(self, logger, test_object):

        self.logger = logger
        # 定义数据库对象
        self.dbObject = DbOpen()


        # 定义测试testObjectDict
        self.testObjectDict = {}
        testObjectDict_list = eval(test_object.get_value("test_object"))
        for testObject in testObjectDict_list:
            if testObject['port']:
                self.testObjectDict[testObject['name']] = testObject['url'] + ":" + testObject['port']
            self.testObjectDict[testObject['name']] = testObject['url']


        # 局部定义全局变量管理信息
        self.globalDict = {}
        google_variable = eval(test_object.get_value("google_variable"))
        self.globalDict.update(google_variable)


        # 数据库配置
        self.dbconfig = {}
        dbconfig_list = eval(test_object.get_value("database_config"))
        for db_config in range(len(dbconfig_list)):
            if db_config == 0:
                self.dbconfig['default'] = dbconfig_list[db_config]
            else:
                self.dbconfig[db_config['name']] = dbconfig_list[db_config]

        logger.info(f'测试对象：{self.testObjectDict}，全局变量{self.globalDict}，数据库配置{self.dbconfig}')





    def initDbObject(self, conn_name):
        try:
            db_connect = self.dbObject[conn_name]
        except Exception:
            raise ClassManager('数据库别名或者测试环境，未在测试对象信息中找到：{}'.format(conn_name))
        dbType = db_connect['dbType']
        dbIp = db_connect['dbIp']
        dbPort = db_connect['dbPort']
        dbName = db_connect['dbName']
        userName = db_connect['userName']
        passWord = db_connect['passWord']
        self.dbObject.add_db_info(dbType, dbIp, dbPort, userName, passWord, dbName, conn_name)
        print('数据库对象创建成功')

    def getDbObject(self, sqlCheck: str, tstObj):
        sqlList = sqlCheck.split('\n') if '\n' in sqlCheck else [sqlCheck]
        for eachSqlCheck in sqlList:
            if '#' in eachSqlCheck:
                dbDefaultName = sqlCheck.split('#')[0]
                if dbDefaultName not in self.dbObject.db_conn_infos:
                    self.initDbObject(dbDefaultName, tstObj)
                else:
                    print('数据库别名已在配置当中，直接返回')
            else:
                raise ClassManager('数据库检查格式书写有误: {}'.format(sqlCheck))

    # def add_tst_obj(self, tstObjName, tstObj):
    #     self.testObjectDict[tstObjName] = tstObj
    #
    # def add_global(self, dic):
    #     self.globalDict.update(dic)
    #
    # @property
    # def get_global(self):
    #     return self.globalDict[]



class ClassManager(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        print(repr(self.value))
        return repr(self.value)


if __name__ == '__main__':

    #测试对象信息：{'test_object': [{'name': '运维', 'url': 'https://m-gw-test.chocolateswap.com', 'port': '', 'protocol': 'HTTP'}],
    # 'database_config': [{'type': 'mysql', 'name': 'supper', 'host': '127.0.0.1', 'port': '3306', 'username': 'admin', 'password': '123456'}], 'google_variable': {'username': '12', 'password': '123456798'}}
    data = {'测试步骤': 'setp2', '参数': 'useName=$createRandomChinese,password=int.34', '接口名称': 'login', '测试对象': 'sit',
            '接口检查': 'message=success', 'header': 'headers',
            '数据库检查': '', '数据库别名': 'default', '数据输出': 'message'}
    manage = Manager()
    manage.initDbObject('default')
