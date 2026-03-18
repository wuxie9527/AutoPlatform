# coding=utf-8
"""
@Time : 2022/10/17 下午12:34
@Author : HeXW
"""
from back.lib.runCase import runCase
from back.testcase import gol

gol_val = gol.headersObj()


def debug_case(cases, test_object, logger):
    gol_val.update_global_dict(test_object)
    for i in cases:
        logger.info(f"后端获取到数据：开始执行用例：{i}")
        runCase(logger,gol_val).runCase(i)