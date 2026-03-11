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
# headers.set_value('testEnvironment', cf.testEnvironment)
# cookies_dict = {cook.split('=')[0]: cook.split('=')[1] for cook in cf.cookie.split('; ')}
# headers.set_value('cookies', cookies_dict)
# allCase = config().get_exe_data(cf.excelName, cf.sheetName)




def debug_case(cases,test_object, logger):
    headers.set_value("test_object",test_object)
    for i in cases:
        logger.info(f"后端获取到数据：开始执行用例：{i}")
        return
        runCase().runCase(i, headers)
