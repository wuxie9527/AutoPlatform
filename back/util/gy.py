# coding=utf-8

import random
import re
from util import DbOpen
import requests

requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
requests = requests.session()
requests.keep_alive = False  # 关闭多余连接
params = {
    "reId": "81",
    "reType": "2",
    "pucType": "1",
    "currencyType": "2",
    "price": "39"
}
url2 = 'http://localdev.energy-java.98du.com/api/activity/draw'
url = 'http://localdev.energy-java.98du.com/api/order/prePurchaseGoods'
headers = {'myclient': '0120650000000000', 'Content-Type': 'application/json; charset=UTF-8',
           'appKey': '55270eb79ee6038a08a37cffe711675d', 'appPackage': 'com.ned.energybox', 'appVersion': '1.2.3',
           'channel': 'mb_guanwang', 'sysVersion': '9', 'platform': 'android', 'deviceId': '8849ca6bc1a40fc2',
           'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIiLCJleHAiOjMzODg0NTExMjcsInVzZXJJZCI6MTAwMDU4LCJjcmVhdGVkIjoxNjM1NDE4NDIzMzM2fQ.ZrnHnX_msmz-ZBX-MIt_xphzXZbPaX-RatKHkJZapNL2fwEMmhCR7DhdWMqy1mgyUIGs0oNIMQQQj2-NYPXRkg'}
db = DbOpen.DbOpen()
sql = 'UPDATE user_profit_data SET profit  = 71.70, draw_number  = 4 WHERE id = 5'
db.add_db_info('mysql', '192.168.100.10', 3306, 'hexingwei', '2GxCSuB7Qiy9AAiH', 'energy')


def test_gl(times):
    xy = 0
    ss = 0
    cs = 0
    for i in range(times):
        global rderNos
        header = updateHeader(str(headers))
        db.db_execute(sql)
        req = requests.post(url, json=params, headers=eval(header))
        print(req.text)
        if 'rderNos' in req.text:
            rderNos = re.findall("rderNos=.*?&", req.text)[0].replace('rderNos=', '').replace('&', '')
            rderNos = {'orderNos': rderNos}
        else:
            raise Exception('没钱了')
        result = requests.post(url2, json=rderNos, headers=headers)
        # print(result.text)
        if '传说' in result.text:
            cs += 1
        elif '稀有款' in result.text:
            xy += 1
        elif '史诗款' in result.text:
            ss += 1
    print('总共抽取了{}次'.format(times))
    print('稀有款出现了：{}次'.format(xy))
    print('史诗款出现了：{}次'.format(ss))
    print('传说款出现了：{}次'.format(cs))
    return '执行完毕'


def updateHeader(headersDict):
    """
    接口签名方案
    :param headersDict: 请求头
    :param params: 入参参数数
    :return: 返回加入签名之后的请求头
    """
    headersDict: dict = eval(headersDict)
    newDict = {}
    nonce = createRandomString(24)
    newDict['nonce'] = nonce
    timestamp = str(get_timestamp())
    newDict['timestamp'] = timestamp
    sign = get_sign(headersDict, newDict['nonce'], newDict['timestamp'])
    newDict['sign'] = sign
    headersDict.update(newDict)
    # print(headersDict)
    return str(headersDict)


def get_sign(expectHead: dict, nonce, timestamp):
    import hashlib
    signStr = {}
    if nonce and timestamp:
        signStr['nonce'] = nonce
        signStr['timestamp'] = timestamp
    else:
        raise Exception('noce或者timestamp值生成错误')
    if 'appPackage' in expectHead and expectHead.get('appPackage'):
        signStr['appPackage'] = expectHead.get('appPackage')
    if 'appVersion' in expectHead and expectHead.get('appVersion'):
        signStr['appVersion'] = expectHead.get('appVersion')
    if 'channel' in expectHead and expectHead.get('channel'):
        signStr['channel'] = expectHead.get('channel')
    if 'deviceId' in expectHead and expectHead.get('deviceId'):
        signStr['deviceId'] = expectHead.get('deviceId')
    if 'platform' in expectHead and expectHead.get('platform'):
        signStr['platform'] = expectHead.get('platform')
    if 'appKey' in expectHead and expectHead.get('appKey'):
        signStr['appKey'] = expectHead.get('appKey')

    signList = sorted(signStr)
    md5str = ''
    for i in range(len(signList)):
        if i == len(signList) - 1:
            md5str += signList[i] + '=' + signStr.get(signList[i])
        else:
            md5str += signList[i] + '=' + signStr.get(signList[i]) + '&'
    md5str = md5str + '2bf8659a9a43519b65ca19e036fe3bcf'
    return hashlib.md5(md5str.encode(encoding='utf-8')).hexdigest().upper()


def get_timestamp():
    import time
    return round(time.time() * 1000)


def createRandomString(lens=10):
    """
    生成随机数字和大小写字母的组合

    """
    randomising = ""
    ceaseless = int(lens)
    while ceaseless:
        tmpInt = random.randrange(1, 63)
        if tmpInt < 11:
            tmpInt += 47
        elif tmpInt < 37:
            tmpInt += 54
        else:
            tmpInt += 60
        randomising += chr(tmpInt)
        ceaseless -= 1
    return randomising


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor, as_completed

    pool = ThreadPoolExecutor(10)  # 最大线程池数
    all_task = []
    for i in range(1):  # 用户数
        all_task.append(pool.submit(test_gl, 1))  # 每个线程循环多少次
    for future in as_completed(all_task):
        result = future.result()
