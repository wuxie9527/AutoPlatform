# coding=utf-8
"""
@Time : 2021/4/25 下午5:46
@Author : HeXW
"""
from lib.runCase import runCase
from lib.Config import config
import pytest
from testcase import gol
import caseConfig as cf

headers = gol.headersObj()
cookies_dict = {cook.split('=')[0]: cook.split('=')[1] for cook in cf.cookie.split('; ')}
headers.set_value('cookies', cookies_dict)
# 获取测试用例，输入sheet_name
allCase = config().get_exe_data(cf.excelName, cf.sheetName)
ids = ["测试用例名称：{}；---用例描述：{}".format(data["用例名称"], data['描述']) for data in
       list(map(lambda x: x if isinstance(x, dict) else x[0], allCase))]


def test_get_eve(get_cmdopts):
    headers.set_value('testEnvironment', get_cmdopts)
    print(headers.get_value('testEnvironment'))


class TestMain(object):
    def setup_class(self):
        pass

    @pytest.mark.parametrize("case", allCase, ids=ids)
    def test_main(self, case):
        data = case if isinstance(case, dict) else case[0]
        if data['调试'] == 'N':
            pytest.skip("用例设置了跳过标志：N")
        runCase().runCase(case, headers)


if __name__ == '__main__':
    pytest.main(["-sv", "test_start.py"])
    # 需要生成测试报告，在命令行/98du目录下执行：pytest --html=report/report.html --self-contained-html --eve=erp
