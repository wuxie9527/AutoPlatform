# coding=utf-8
"""
@Time : 2021/4/26 下午1:06
@Author : HeXW
"""


class headersObj:

    def __init__(self):  # 初始化
        # global global_dict
        self._global_dict = {}

    def set_value(self, key, value):
        """ 定义一个全局变量 """
        self._global_dict[key] = value

    def get_value(self, key, defValue=None):
        try:
            return str(self._global_dict[key])
        except KeyError:
            return None

    def get_global_dict(self):
        return self._global_dict

    def remove(self, key):
        self._global_dict.pop(key)

    def update_global_dict(self, newDict):
        if isinstance(newDict, dict):
            self._global_dict.update(newDict)
        else:
            raise golError('输入的格式必须是字典，请在此确认')

    def update_one(self, changeKey, changeValue):
        self._global_dict[changeKey].update(changeValue)



class golError:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
