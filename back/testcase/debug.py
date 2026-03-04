# coding=utf-8
"""
@Time : 2022/10/17 下午12:34
@Author : HeXW
"""
from lib.runCase import runCase
from lib.Config import config
from testcase import gol
import caseConfig as cf

headers = gol.headersObj()
headers.set_value('testEnvironment', cf.testEnvironment)
cookies_dict = {cook.split('=')[0]: cook.split('=')[1] for cook in cf.cookie.split('; ')}
headers.set_value('cookies', cookies_dict)
allCase = config().get_exe_data(cf.excelName, cf.sheetName)

if __name__ == '__main__':
    for i in allCase:
        i = i if isinstance(i, list) else [i]
        if i[0]['调试'] == 'N':
            pass
        else:
            runCase().runCase(i, headers)
