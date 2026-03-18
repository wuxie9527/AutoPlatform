# coding=utf-8
"""
@Time : 2022/4/19 下午5:53
@Author : HeXW
"""

from back.lib.dealParamsData import dealRequestData
from back.lib.interfale import HTTP
from back.lib.check import check
from back.lib.Manager import Manager
import re


def check_caseStep_params(caseStep):
    if '\n' in str(caseStep['参数']):
        caseStep['参数'] = caseStep['参数'].replace("\n", '')
    elif '，' in str(caseStep['参数']):
        caseStep['参数'] = caseStep['参数'].replace("，", ',')
    elif '\n' in caseStep['变量输出']:
        caseStep['变量输出'] = caseStep['变量输出'].replace("\n", '')
    elif '，' in caseStep['变量输出']:
        caseStep['变量输出'] = caseStep['变量输出'].replace("，", ',')
    elif caseStep['数据库检查']:
        if '\n' in caseStep['数据库检查']:
            caseStep['数据库检查'] = caseStep['数据库检查'].replace("\n", '')
    elif caseStep['数据库检查']:
        if '，' in caseStep['数据库检查']:
            caseStep['数据库检查'] = caseStep['数据库检查'].replace("，", ',')


class runCase:
    def __init__(self, logger, test_object):
        self.manage = Manager(logger, test_object)
        self.dealData = dealRequestData(self.manage, logger)
        self.logger = logger
        self.gol_val = test_object

    def runCase(self, CaseData):
        # 如果是字典说明只有一个步骤
        CaseData = CaseData if isinstance(CaseData, list) else [CaseData]
        for caseStep in CaseData:
            # 判断执行用例还是接口
            # if caseStep['执行方式'] == '用例':
            #     testCaseNum = int(caseStep['参数'])
            #     # allCase = config().get_exe_data(cf.excelName, cf.sheetName)
            #     # self.runCase(allCase[testCaseNum])
            #     continue
            # 获取测试对象名称
            self.logger.info('=================================================================')
            self.logger.info('开始执行测试步骤-{}：{}'.format(caseStep['步骤ID'], caseStep['步骤名称']))
            self.logger.info('测试步骤信息：{}'.format(caseStep))
            tstObj = self.manage.testObjectDict[caseStep["测试对象名称"]]
            self.logger.info('拼接好的url：{}'.format(tstObj))
            if caseStep['执行方式'] == 'redis':
                self.getInspect(caseStep, tstObj)
                continue

            # 检查文件格式是否正确
            check_caseStep_params(caseStep)

            # 处理params和url
            caseStep = self.dealData.get_send_params(caseStep)
            self.logger.info(f'处理完的测试步骤数据========”{caseStep}')
            # 获取请求头信息
            headersDict = caseStep["header"]
            headersDict = self.update_headersDict(eval(headersDict))
            headersDict = self.check_headerSpace(headersDict)
            # 发送request
            cookie = None
            if "cookies" in self.manage.globalDict:
                cookie = self.manage.globalDict["cookies"]
            http = HTTP(caseStep['url'], self.gol_val, self.logger, cookie)
            self.logger.info('请求url：{}'.format(caseStep['url']))
            self.logger.info('请求头：{}'.format(headersDict))
            self.logger.info('请求参数：{}'.format(caseStep['body']))
            # 处理上传文件
            files = None
            receive_str = http.send(caseStep['执行方式'], headersDict, caseStep['body'], files)
            self.logger.info('请求成功返回参数：{}'.format(receive_str))
            checker = check(receive_str, self.manage, self.logger)
            if caseStep['接口校验']:
                checker.check_receive_str(caseStep['接口校验'])
            if caseStep['变量输出']:
                checker.export_Params(caseStep['变量输出'], caseStep['body'])
            if caseStep['数据库检查']:
                checker.deal_with_dbChecker(caseStep['数据库检查'], tstObj)
            # if interName in caseConfig.location_to_headers:
            #     headersDict = eval(headersDict)
            #     headersDict['location'] = self.manage.globalDict['location']
            #     headers.set_value(key=caseStep['请求头'], value=headersDict)


    def check_headerSpace(self,headers):
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

    def update_headersDict(self, headersDict):
        if isinstance(headersDict, dict):
            headersDict_copy = headersDict.copy()
            for key, value in headersDict_copy.items():
                if "$" in value:
                    # 'header': '{"Content-Type":"application/json","ps-ticket": "${ticket}"}'
                    value = re.findall(r'\{(.*?)\}', value)[0]
                    if value in self.manage.globalDict:
                        headersDict[key] = value
                    else:
                        headersDict.pop(key)
            self.logger.info(f"处理后的请求头：{headersDict}")
            return headersDict
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
    data = {'用例名称': '上传文件', '测试步骤': 'setp1', '参数': 'imeiNum=1,"imsiNum"=2', '接口名称': 'startup',
            'method': 'post',
            'files': 'imageFile=1614740668406.jpg',
            '测试对象': 'sit', '接口检查': 'message=操作成功,code=200',
            '数据库检查': 'default#select username from user$admin',
            '变量输出': 'accessToken'}
