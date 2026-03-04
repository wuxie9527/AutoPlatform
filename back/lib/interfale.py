# coding=utf-8
'''
@Time : 2021/8/24 下午3:01
@Author : HeXW
'''

import re
import requests.exceptions as exceptions
from config.Commom import image_path
from urllib import parse


class ClassInterface(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        print(repr(self.value))
        return repr(self.value)


class HTTP(object):
    """
    http:接口测试相关函数
    """

    def __init__(self, url, headers, cookie=None):
        if cookie is None:
            cookie = {}
        self.module = __import__('requests')
        self.url = url
        self.cookie = cookie
        self.logger = None
        # self.hexReStr = "(\\\\u([a-f0-9]{4}))"
        self.method_2_method = {"post": self.post, "get": self.get, "put": self.put}
        self.glob = headers

    def is_chinese(self, string):
        '''
        判断字符串里是否有中文
        '''
        for i in list(str(string)):
            if u'\u9fff' >= i >= u'\u4e00':
                return True
        return False

    def put(self, url, paramsvalue=None, headers=None, json=None):
        req = self.module.put(url, params=paramsvalue, cookies=self.cookie, headers=headers, json=json)
        cookiesDict = dict(req.cookies)
        if cookiesDict:
            self.cookie.update(cookiesDict)
            self.glob.update_global_dict(self.cookie)
        return req.text

    def get(self, url, paramsvalue=None, headers=None, json=None):
        req = self.module.get(url, params=paramsvalue, cookies=self.cookie, headers=headers, json=json,
                              allow_redirects=False)
        cookiesDict = dict(req.cookies)
        if cookiesDict:
            self.cookie.update(cookiesDict)
            self.glob.update_one('cookies', self.cookie)
        return req.text

    def post(self, url, paramsvalue=None, headers=None, json=None, files=None):
        try:
            req = self.module.post(url, data=paramsvalue, cookies=self.cookie, headers=headers, json=json, files=files,
                                   allow_redirects=False)
            cookiesDict = dict(req.cookies)
        except exceptions.ConnectionError:
            raise ClassInterface('服务器连接出现异常，请确认config文件中测试对象配置信息是否书写正确，服务器应用是否正常启动！')
        if cookiesDict:
            self.cookie.update(cookiesDict)
            self.glob.update_one('cookies',self.cookie)
            self.glob.update_global_dict(self.cookie)
        return req.text

    def deal_with_recvdata(self, receive_str):
        # 处理false、true和null，添加双引号
        needDelWith = ['false', 'true', 'null']
        for one in needDelWith:
            receive_str = re.sub('([: ]+)' + one + '([ ,]*)', lambda x: x.group(1) + '"' + one + '"' + x.group(2),
                                 receive_str)
        return receive_str

    def send(self, method, headers, params, files: dict):
        headers = self.deal_with_header_data(headers)
        method = self.method_2_method.get(method)
        if method is None:
            raise ClassInterface('暂不支持此method:{}，仅支持POST,PUT和GET，请检查'.format(method))
        if files:
            data = self.get_header_params(headers, params, files)
            fileParamss = list(files.keys())[0]
            fileName = list(files.values())[0]
            data.pop('files')
            with open(image_path + fileName, 'rb') as f:
                file = {fileParamss: (image_path + fileName, f.read(), "image/jpg")}
            receive_str = method(self.url, files=file, **data)
        else:
            receive_str = method(self.url, **self.get_header_params(headers, params, files))
        receive_str = self.deal_with_recvdata(receive_str)
        return receive_str

    def deal_with_header_data(self, headers):
        isChinese = False
        headers = headers if isinstance(headers, dict) else eval(headers)
        for key, value in headers.items():
            if self.is_chinese(value):
                headers[key] = value.encode(encoding='utf_8')
                if not isChinese:
                    isChinese = True
        if isChinese:
            print('发现header中存在中文字段，将对中文字段进行utf8编码')
        return headers

    def get_header_params(self, headers, params, files=None):
        headers = headers if isinstance(headers, dict) else eval(headers)
        if files:
            headers.pop("Content-Type")
            return {"headers": headers, "paramsvalue": params, "files": files}
        else:
            if headers:
                if headers.get("Content-Type").startswith("application/json"):
                    return {"headers": headers, "json": params}
                elif headers.get("Content-Type").startswith("application/xml"):
                    headers["Content-Type"] = "application/xml;charset=utf-8"
                    return {"headers": headers, "paramsvalue": params.encode('utf-8').decode('latin1')}
                elif headers.get("Content-Type").startswith("application/x-www-form-urlencoded"):
                    return {"headers": headers, "paramsvalue": parse.urlencode(params)}
                else:
                    return {"headers": headers, "paramsvalue": params}
            else:
                return {"headers": headers, "paramsvalue": params}
