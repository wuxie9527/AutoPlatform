# coding=utf-8
"""
@Time : 2021/10/21 下午10:31
@Author : HeXW
"""
import os

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

flag = os.sep

config_path = os.path.dirname((os.path.abspath(__file__))) + flag
data_path = root_path + flag + 'Date' + flag
all_logger_path = root_path + flag + 'logs' + flag + "server.log"
error_logger_path = root_path + flag + 'logs' + flag + "error.log"
result_path = root_path + flag + 'report' + flag
image_path = root_path + flag + 'image' + flag

# 执行结果
ACTIONFAIL = 'FAIL'
ACTIONPASS = 'PASS'
ACTIONERROR='ERROR'
ACTIONSKIP='SKIP'
TIMEOUT = 20


if __name__ == '__main__':
    print(flag)
    print(root_path)