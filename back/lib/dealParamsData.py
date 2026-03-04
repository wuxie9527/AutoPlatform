# coding=utf-8
"""
@Time : 2021/11/6 下午1:52
@Author : HeXW
"""
import re
import json

from util import CollectUtil
from lib.Manager import Manager


class dealParamsError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        print(repr(self.value))
        return repr(self.value)


class dealRequestData:
    def __init__(self, manage: Manager):
        self.manage = manage

    def get_send_params(self, testData, tstObj, inter, gol_headers):
        testDada = self.deal_with_case_params(testData, gol_headers)
        testDada = self.deal_with_files(testDada)
        roadPass = self.deal_with_roadPass(inter.get('roadpass'))
        if roadPass.endswith('/'):
            roadPass = roadPass[:-1]
        url = tstObj.get_testObj_url(testData['测试对象']) + roadPass
        # inter_params = eval(self.deal_with_date(inter.get('params')))
        global false, null, true
        false = False
        true = True
        null = None
        inter_params = eval(inter.get('params'))
        param = self.deal_with_inter_params(inter_params)
        # print('接口测试数据::{}'.format(param))
        params = self.up_params(param, testDada['参数'])
        testDada['params'] = params
        testDada['url'] = url
        testDada['method'] = inter.get('method')
        # testDada.pop('参数')
        # testData.pop('接口名称')
        # self.manage.globalDict['deviceId'] = testDada['params']['deviceId']
        return testData

    def deal_with_case_params(self, testData, gol_headers):
        if isinstance(testData, dict):
            if testData['参数']:
                dic = {}
                param = testData['参数'].split(',')
                for i in param:
                    if '$' in i:
                        input_value = i.split('=')[1].replace('$', '')
                        input_key = i.split('=')[0]
                        # ids=[$time,$like]
                        if '[' and ']' in input_value:
                            inputValue = []
                            input_value_list = input_value.replace('[', '').replace(']', '').split(',')
                            for k in input_value_list:
                                if k in self.manage.globalDict:
                                    inputValue.append(self.manage.globalDict[k])
                                else:
                                    raise dealParamsError('参数{},在全局变量中找不到'.format(k))
                            dic[input_key] = inputValue
                        else:
                            if input_value in self.manage.globalDict or input_value in gol_headers:
                                if input_value in self.manage.globalDict:
                                    dic[i.split('=')[0]] = self.manage.globalDict[input_value]
                                else:
                                    dic[i.split('=')[0]] = gol_headers[input_value]
                            else:
                                try:
                                    starData = getattr(CollectUtil, input_value)()
                                except Exception:
                                    raise Exception('找不到自定义函数' + '：' + input_value)
                                dic[i.split('=')[0]] = starData
                    else:
                        try:
                            val = i.split('=')[1]
                            if 'int' in val:
                                val = int(i.split('=')[1].split('.')[1])
                            dic[i.split('=')[0]] = val
                        except Exception:
                            raise Exception('参数格式有误，请检查参数是否正确')
                testData['参数'] = dic
            # print('处理完参数化后的的参数：{}'.format(testData))
            return testData

    def deal_with_files(self, caseStep):
        if caseStep['files']:
            # {"imageFile": ('1614740668406.jpg', open(path, "rb"), 'image/jpg')}
            if '=' in caseStep['files']:
                fileDict = {}
                fileParams = caseStep['files'].split('=')
                fileDict[fileParams[0]] = fileParams[1]
                caseStep['files'] = fileDict
                return caseStep
            else:
                raise Exception('参数格式有误，请检查参数是否正确')
        else:
            return caseStep

    def up_params(self, data, fields: dict):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    self.up_params(value, fields)
                elif isinstance(value, list):
                    for i in value:
                        if type(i) == dict:
                            self.up_params(i, fields)
                        else:
                            if key in fields:
                                data[key] = fields[key]
                else:
                    if key in fields:
                        data[key] = fields[key]
        elif isinstance(data, list):
            for t in data:
                self.up_params(t, fields)
        else:
            print('参数是:{}'.format(data))
            raise Exception('接口参数处理异常')
        return data

    def deal_with_inter_params(self, interParams):
        if isinstance(interParams, dict):
            for key in interParams.keys():
                if isinstance(interParams[key], dict):
                    self.deal_with_inter_params(interParams[key])
                elif isinstance(interParams[key], list):
                    # if ':' in str(interParams[key]):
                    for i in interParams[key]:
                        if type(i) == dict:
                            self.deal_with_inter_params(i)
                else:
                    if '$' in str(interParams[key]):
                        if ':' in str(interParams[key]):
                            #['SFTPO', '$flow_task_offering_id']
                            interParams_list = str(interParams[key]).split(':')
                            value = interParams_list[0] + ':' + str(self.manage.globalDict[interParams_list[1].replace('$', '')])
                            interParams[key] = value
                        else:
                            value = interParams[key].replace('$', '')
                            if value in self.manage.globalDict:
                                interParams[key] = self.manage.globalDict[value]
                            elif hasattr(CollectUtil, value):
                                starData = getattr(CollectUtil, value)()
                                interParams[key] = starData
                            else:
                                raise dealParamsError('key值不在全局变量中，且不是自定义函数，请检查：{}'.format(value))
        elif isinstance(interParams, list):
            for t in interParams:
                self.deal_with_inter_params(t)
        else:
            print('参数是:{}'.format(interParams))
            raise Exception('接口参数处理异常')

        return interParams

    def deal_with_roadPass(self, roadPass: str):
        if '$' in roadPass:
            if roadPass.endswith('/'):
                road_change_list = re.findall('\$.*?(?=/)', roadPass)
                for i in road_change_list:
                    change_params = i.replace('$', '')
                    try:
                        params = self.manage.globalDict[change_params]
                    except KeyError:
                        raise dealParamsError('全局变量不存在，{}'.format(change_params))
                    roadPass = re.sub('\$' +change_params+ '(?=/)', str(params), roadPass)
                return roadPass
            else:
                raise dealParamsError('接口请求路径中存在变量，需要在结尾加上：/ ，{}'.format(roadPass))
        else:
            return roadPass

    def deal_with_date(self, receive_str):
        # 处理false、true和null，添加双引号
        needDelWith = ['false', 'true', 'null']
        for one in needDelWith:
            receive_str = re.sub('([: ]+)' + one + '([ ,]*)', lambda x: x.group(1) + '"' + one + '"' + x.group(2),
                                 receive_str)
        return receive_str

    def deal_with_ftn(self, receive_str):
        needDelWith = ['false', 'true', 'null']
        for one in needDelWith:
            if one == 'null':
                receive_str = re.sub('([: ]+)' + one + '([ ,]*)', lambda x: x.group(1) + 'None' + x.group(2),
                                     receive_str)
            else:
                receive_str = re.sub('([: ]+)' + one + '([ ,]*)', lambda x: x.group(1) + one.capitalize() + x.group(2),
                                     receive_str)
        return receive_str


if __name__ == '__main__':
    data = {'测试步骤': 'setp2', '参数': 'useName=$createRandomChinese,password=int.34', '接口名称': 'login', '测试对象': 'sit',
            '接口检查': 'message=success', 'header': 'headers',
            '数据库检查': '', '数据库别名': 'default', '数据输出': 'message'}
    print(dealRequestData().get_send_params(data))
