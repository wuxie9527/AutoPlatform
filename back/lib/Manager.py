# coding=utf-8
"""
@Time : 2021/4/17 下午3:23
@Author : HeXW
"""
from util.DbOpen import DbOpen
from lib.testObj import testObj


class Manager:
    def __init__(self):
        # 定义数据库对象
        self.dbObject = DbOpen()
        # 定义测试对象字典
        self.testObjectDict = {}
        # 局部定义全局变量管理信息
        self.globalDict = {}

    def initDbObject(self, conn_name, tstObj: testObj):
        try:
            db_connect = tstObj.get_testObj_dbConfig(conn_name)
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

    def add_tst_obj(self, tstObjName, tstObj):
        self.testObjectDict[tstObjName] = tstObj

    def add_global(self, dic):
        self.globalDict.update(dic)

    @property
    def get_global(self):
        return self.globalDict



class ClassManager(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        print(repr(self.value))
        return repr(self.value)


if __name__ == '__main__':
    data = {'测试步骤': 'setp2', '参数': 'useName=$createRandomChinese,password=int.34', '接口名称': 'login', '测试对象': 'sit',
            '接口检查': 'message=success', 'header': 'headers',
            '数据库检查': '', '数据库别名': 'default', '数据输出': 'message'}
    manage = Manager()
    manage.initDbObject('default')
