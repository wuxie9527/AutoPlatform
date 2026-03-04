# coding=utf-8
"""
@Time : 2021/4/21 上午11:32
@Author : HeXW
"""
from lib.Config import config


class interObj:
    def __init__(self):
        pass

    @staticmethod
    def readInter(interFaceName, interIni='interfale.ini'):
        intObj = config().get_config(interFaceName, interIni)
        return intObj

    @staticmethod
    def readHeaders(headersName, interIni='interfale.ini'):
        intObj = config().get_config(headersName, interIni)
        return intObj


class dataObj:
    def __init__(self):
        pass

    @classmethod
    def get_each_case_data(cls, testName, sheetName):
        sheetData = config().get_exe_data(testName, sheetName)
        return sheetData


if __name__ == '__main__':
    initer = interObj.readInter('save-image')
    print(initer.get('params'))
    print(eval(initer.get('params')))


