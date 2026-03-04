# coding=utf-8
"""
@Time : 2021/4/21 上午11:14
@Author : HeXW
"""
from lib.Config import config


class testObj:
    def __init__(self, testEl):
        self.url = eval(testEl['url'])
        self.dbConfig = testEl['dbinfo']
        self.gloBalVal = testEl['globalval']

    @classmethod
    def redTestObj(cls, el):
        tetObj = config().get_config(el, 'testObject.ini')
        return tetObj

    def get_testObj_url(self, eve):
        return self.url[eve]

    def get_testObj_dbConfig(self, eve):
        return eval(self.dbConfig)[eve]

    def get_testObj_gloBallVal(self):
        return self.gloBalVal


if __name__ == '__main__':
    testdic = testObj.redTestObj('test')
    dbconect = (eval(testdic['dbinfo']))
    print(dbconect['redis']['host'])
