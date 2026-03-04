# coding=utf-8
"""
@Time : 2022/4/19 下午5:53
@Author : HeXW
"""
from lib.interObj import interObj
from lib.testObj import testObj
from lib.dealParamsData import dealRequestData
from lib.interfale import HTTP
from lib.check import check
from lib.Manager import Manager
import caseConfig
from lib.Config import config
import caseConfig as cf


def check_caseStep_params(caseStep):
    if '\n' in str(caseStep['参数']):
        caseStep['参数'] = caseStep['参数'].replace("\n", '')
    elif '，' in str(caseStep['参数']):
        caseStep['参数'] = caseStep['参数'].replace("，", ',')
    elif '\n' in caseStep['数据输出']:
        caseStep['数据输出'] = caseStep['数据输出'].replace("\n", '')
    elif '，' in caseStep['数据输出']:
        caseStep['数据输出'] = caseStep['数据输出'].replace("，", ',')
    elif '\n' in caseStep['数据库检查']:
        caseStep['数据库检查'] = caseStep['数据库检查'].replace("\n", '')
    elif '，' in caseStep['数据库检查']:
        caseStep['数据库检查'] = caseStep['数据库检查'].replace("，", ',')


class runCase:
    def __init__(self):
        self.manage = Manager()
        self.dealData = dealRequestData(self.manage)

    def runCase(self, CaseData, headers):
        # 如果是字典说明只有一个步骤
        CaseData = CaseData if isinstance(CaseData, list) else [CaseData]
        for caseStep in CaseData:
            # 判断执行用例还是接口
            if caseStep['调试'] == 'N':
                continue
            if caseStep['执行方式'] == '用例':
                testCaseNum = int(caseStep['参数'])
                allCase = config().get_exe_data(cf.excelName, cf.sheetName)
                self.runCase(allCase[testCaseNum], headers)
                continue
            # 获取测试对象名称
            print('=================================================================')
            print('开始执行测试用例：{}的{}，{}'.format(caseStep['用例名称'], caseStep['测试步骤'], caseStep['描述']))
            print('测试步骤信息：{}'.format(caseStep))
            testEnvironment = headers.get_value('testEnvironment')
            tstObj = self.get_test_obj(testEnvironment)
            if caseStep['执行方式'] == 'redis':
                self.getInspect(caseStep, tstObj)
                continue
            # 获取文件全局变量
            gloVal = tstObj.get_testObj_gloBallVal()
            if gloVal:
                # 将全局变量添加的局部全局变量
                self.manage.globalDict.update(eval(gloVal))
            # 检查文件格式是否正确
            check_caseStep_params(caseStep)
            # 获取接口路径
            interName = caseStep['接口名称']
            interData = interObj.readInter(interName, caseConfig.faceName)
            # 处理params和url
            caseStep = self.dealData.get_send_params(caseStep, tstObj, interData, headers.get_global_dict())
            # 获取请求头信息
            headersDict = self.get_header(headers, caseStep['请求头'])
            if caseStep['请求头参数']:
                self.update_headersDict(headersDict, caseStep['请求头参数'])
            # 将 device 添加到全局变量，在把全局变量更新到请求头
            # if caseStep['用例名称'].startswith('登陆') and caseStep['测试步骤'] == 'setp1':
            #     headersDict = self.deal_with_headers(caseStep, headersDict, headers)
            headersDict = self.check_headerSpace(headersDict)
            # 发送request
            cookie = None
            if headers.get_value('cookies'):
                cookie = eval(headers.get_value('cookies'))
            http = HTTP(caseStep['url'], headers, cookie)
            print('请求url：{}'.format(caseStep['url']))
            print('请求头：{}'.format(headersDict))
            print('请求参数：{}'.format(caseStep['params']))
            receive_str = http.send(caseStep['method'], headersDict, caseStep['params'], caseStep['files'])
            print('请求成功返回参数：{}'.format(receive_str))
            checker = check(receive_str, self.manage)
            if caseStep['接口检查']:
                checker.check_receive_str(caseStep['接口检查'])
            if caseStep['数据输出']:
                checker.export_Params(caseStep['数据输出'], caseStep['params'])
            if caseStep['数据库检查']:
                checker.deal_with_dbChecker(caseStep['数据库检查'], tstObj, headers)
            if interName in caseConfig.location_to_headers:
                headersDict = eval(headersDict)
                headersDict['location'] = self.manage.globalDict['location']
                headers.set_value(key=caseStep['请求头'], value=headersDict)
            elif interName == 'get-token':
                token = self.manage.globalDict['sessionToken']
                authorization = 'Bearer ' + token
                headers.update_one('headers', {'authorization': authorization})
            elif interName == 'getToken':
                token = self.manage.globalDict['sessionToken']
                authorization = 'Bearer ' + token
                headers.update_one('smyHeaders', {'authorization': authorization})
            elif interName == 'get-token-three':
                token = self.manage.globalDict['sessionToken']
                authorization = 'Bearer ' + token
                headers.update_one('hjsHeaders', {'authorization': authorization})
            elif interName == 'getToken-four':
                token = self.manage.globalDict['sessionToken']
                authorization = 'Bearer ' + token
                headers.update_one('shHeaders', {'authorization': authorization})
            if caseStep['请求头参数']:
                self.pop_headersDict(headersDict, caseStep['请求头参数'])

    @staticmethod
    def get_header(headersOBJ, headerName) -> dict:
        """
        headerName获取请求头，如在headersOBJ里面不存在，就去文件里找，在放到对象里
        :param headersOBJ: 全局变量，请求头管理对项
        :param headerName: 请求头名字
        :return: 根据请求头name，返回请求头字典格式
        """
        if headerName not in headersOBJ.get_global_dict():
            head = interObj.readHeaders(headerName, caseConfig.faceName)
            headersOBJ.set_value(headerName, eval(head['headers']))
        try:
            return eval(headersOBJ.get_value(headerName))
        except Exception:
            raise Exception('请求头格式不正确')

    @staticmethod
    def check_headerSpace(headers):
        """
        请求头key，value头尾去空格
        :param headers:
        :return:
        """
        for key, value in headers.items():
            key.strip()
            value.strip()
        return str(headers)

    @staticmethod
    def get_timestamp():
        import time
        return round(time.time() * 1000)

    def get_test_obj(self, tstEl):
        if tstEl in self.manage.testObjectDict:
            tstObj = self.manage.testObjectDict.get(tstEl)
        else:
            tstObj = testObj(testObj.redTestObj(tstEl))
            self.manage.add_tst_obj(tstEl, tstObj)
        return tstObj

    def deal_with_headers(self, caseStp, headersDict, headers):
        # self.manage.globalDict['deviceId'] = caseStp['params']['deviceId']
        headersDict.update(self.manage.globalDict)
        headers.set_value(key=caseStp['请求头'], value=headersDict)
        return headersDict

    def getInspect(self, caseStep, tstObj):
        import redis
        db = int(caseStep['参数'])
        redisConfig = tstObj.get_testObj_dbConfig('redis')
        r = redis.Redis(host=redisConfig['host'], port=6379, db=db, password=redisConfig['passWord'],
                        decode_responses=True)
        graphId = self.manage.globalDict['graphId']
        for_key = 'Oauth2:GraphCaptchaCache::' + graphId
        inspect = r.get(for_key).replace('"', '')
        self.manage.add_global({'inspect': inspect})

    def update_headersDict(self, headersDict, headerPms):
        if isinstance(headersDict, dict):
            dic = {}
            headerPm = headerPms.split(',')
            for i in headerPm:
                dic[i.split('=')[0]] = i.split('=')[1]
            headersDict.update(dic)
        else:
            raise Exception('请求头不是字典格式')

    def pop_headersDict(self, headersDict, headerPms):
        dic = {}
        if isinstance(headersDict, str):
            headersDict = eval(headersDict)
        if isinstance(headersDict, dict):
            headerPm = headerPms.split(',')
            for i in headerPm:
                dic[i.split('=')[0]] = i.split('=')[1]
        else:
            raise Exception('请求头不是字典格式')
        for key in dic:
            headersDict.pop(key)


if __name__ == '__main__':
    data = {'用例名称': '上传文件', '测试步骤': 'setp1', '参数': 'imeiNum=1,"imsiNum"=2', '接口名称': 'startup', 'method': 'post',
            'files': 'imageFile=1614740668406.jpg',
            '测试对象': 'sit', '接口检查': 'message=操作成功,code=200', '数据库检查': 'default#select username from user$admin',
            '数据输出': 'accessToken'}
