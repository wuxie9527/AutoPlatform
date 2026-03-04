# coding=utf-8
"""
@Time : 2021/10/27 下午3:07
@Author : HeXW
"""
from pathlib import Path
import configparser
from config.Commom import config_path
import xlrd
from config.Commom import data_path
from util.loger import get_loger


class config(object):
    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.logger = get_loger()

    def get_config(self, element, testName):
        path = config_path + testName
        if Path(path).is_file():
            self.config.read(path, encoding='utf-8')
            try:
                lis = str(self.config.items(element))
            except Exception:
                print(element, testName)
                raise ConfigError('接口名称,测试对象或者请求头在配置文件中未找到。')
            lis = lis.replace('(', '[').replace(')', ']')
            lis = eval(lis)
        else:
            raise Exception('配置文件不存在')
        return dict(lis)

    def get_exe_data(self, testName, sheetName):
        path = data_path + testName
        sheet = xlrd.open_workbook(path)
        lis = []
        sheetCon = sheet.sheet_by_name(sheetName)
        key_title = sheetCon.row_values(0)
        for i in range(1, sheetCon.nrows):
            # lis = []
            dic = {}
            nlowList = sheetCon.row_values(i)
            if nlowList[1].startswith("step"):
                if nlowList[1] == 'step1':
                    for cell in range(0, sheetCon.ncols):
                        dic[key_title[cell]] = nlowList[cell]
                    lis.append(dic)
                else:
                    newList = lis[-1] if isinstance(lis[-1], list) else [lis[-1]]
                    dic['用例名称'] = newList[-1]['用例名称']
                    for cell in range(1, sheetCon.ncols):
                        dic[key_title[cell]] = nlowList[cell]
                    newList.append(dic)
                    lis[-1] = newList
            else:
                raise Exception('测试步骤必须以：step开头')
        return lis


class ConfigError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


if __name__ == '__main__':
    print(config().get_config('test', 'testObject.ini'))

