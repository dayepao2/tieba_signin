import copy
import datetime
import json
import os
import re
import sys
import time

import requests
from bs4 import BeautifulSoup


TIEBA_COOKIE = str(os.environ.get("TIEBA_COOKIE"))
PUSH_KEY = os.environ.get("PUSH_KEY")


def get_method(url, headers=None):
    k = 1
    while k < 6:
        try:
            res = requests.get(url, headers=headers, timeout=5)
        except Exception as e:
            k = k + 1
            print(sys._getframe().f_code.co_name + ": " + str(e))
            time.sleep(1)
            continue
        else:
            break
    try:
        return res
    except Exception:
        sys.exit(sys._getframe().f_code.co_name + ": " + "Max retries exceeded")


def post_method(url, postdata=None, postjson=None, headers=None):
    k = 1
    while k < 6:
        try:
            res = requests.post(url, data=postdata, json=postjson, headers=headers, timeout=5)
        except Exception as e:
            k = k + 1
            print(sys._getframe().f_code.co_name + ": " + str(e))
            time.sleep(1)
            continue
        else:
            break
    try:
        return res
    except Exception:
        sys.exit(sys._getframe().f_code.co_name + ": " + "Max retries exceeded")


def onekeysignin():
    url = "https://tieba.baidu.com/tbmall/onekeySignin1"
    res = get_method(url, headers)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)


def check_cookie():
    url = "http://tieba.baidu.com/dc/common/tbs"
    res = get_method(url, headers)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    jsonstr = json.loads(soup.text)
    is_login = jsonstr['is_login']
    return bool(is_login)


def start_signin():
    para.tbs = get_tbs()
    tiebalist = get_list()
    para.pushstr = para.pushstr + now + "\n\n开始签到，共" + str(len(tiebalist)) + "个贴吧\n"
    print(tiebalist)
    print("\n" + now + "\n开始签到，共" + str(len(tiebalist)) + "个贴吧")
    signin(tiebalist, 1)


def get_tbs():
    url = "http://tieba.baidu.com/dc/common/tbs"
    res = get_method(url, headers)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    jsonstr = json.loads(soup.text)
    tbs = jsonstr['tbs']
    return tbs


def get_list():
    print(now + "\n正在获取关注贴吧列表...\n")
    tiebalist = []
    key = 1
    while True:
        url = "http://tieba.baidu.com/f/like/mylike?&pn=" + str(key)
        res = get_method(url, headers)
        html = res.text
        temp_list = re.findall(re.compile('<a href="\\/f\\?kw=.*?" title="(.*?)">.+?<\\/a>'), html)
        if temp_list:
            tiebalist = tiebalist + temp_list
            key = key + 1
        else:
            break
        time.sleep(5)
    return tiebalist


def signin(tiebalist, key):
    temp_list = copy.deepcopy(tiebalist)
    stop_key = 3
    print("\n开始第" + str(key) + "轮签到")
    for tieba in tiebalist:
        url = 'https://tieba.baidu.com/sign/add'
        postdata = {'ie': 'utf-8', 'kw': tieba, 'tbs': para.tbs}
        res = post_method(url, postdata=postdata, headers=headers)
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        if 'success' in str(soup):
            signin_msg = tieba + "吧 签到成功"
            temp_list.remove(tieba)
        elif '\\u4eb2\\uff0c\\u4f60\\u4e4b\\u524d\\u5df2\\u7ecf\\u7b7e\\u8fc7\\u4e86' in str(soup):
            signin_msg = tieba + "吧 已经签到过了"
            temp_list.remove(tieba)
        else:
            signin_msg = tieba + "吧 签到失败: " + str(soup)
        print(signin_msg)
        time.sleep(5)
    para.pushstr = para.pushstr + "\n第" + str(key) + "轮签到: " + str(len(tiebalist) - len(temp_list)) + "个贴吧签到成功\n"
    tiebalist = copy.deepcopy(temp_list)
    if tiebalist:
        if key < stop_key:
            signin(tiebalist, key + 1)
        else:
            print("\n经过" + str(stop_key) + "轮签到后，下列贴吧签到失败\n" + str(tiebalist))
            para.pushstr = para.pushstr + "\n经过" + str(stop_key) + "轮签到后，下列贴吧签到失败\n" + str(tiebalist)


def push():
    pushurl = "https://push.dayepao.com/?pushkey=" + PUSH_KEY
    pushdata = {
        "touser": "@all",
        "msgtype": "text",
        "agentid": 1000002,
        "text": {
            "content": para.pushstr
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 0
    }
    res = post_method(pushurl, postjson=pushdata)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    print("\n推送状态: " + str(soup))


class para:
    pushstr = "百度贴吧自动签到\n"
    tbs = ""


if __name__ == '__main__':
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    headers = {
        'X-Forwarded-For': '121.238.47.136',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67',
        'Cookie': TIEBA_COOKIE
    }
    # onekeysignin()
    # get_list()
    if check_cookie():
        start_signin()
    else:
        print(now + "\nCookie已失效")
        para.pushstr = para.pushstr + now + "\n\nCookie已失效"

    PUSH_KEY and push()
