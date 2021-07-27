import json
import os
import random
import re
import sys
import time

import execjs
import requests
from bs4 import BeautifulSoup

# pip install PyExecJS


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


def get_tbs(headers):
    url = "http://tieba.baidu.com/dc/common/tbs"
    res = get_method(url, headers)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    jsonstr = json.loads(soup.text)
    tbs = jsonstr['tbs']
    return tbs


def get_list(headers):
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


def get_post_list(tieba, headers):
    url = "https://tieba.baidu.com/f?kw=" + tieba
    res = get_method(url, headers)
    html = res.text
    post_list = re.findall(re.compile('<a rel="noreferrer" href="\\/p\\/(.+?)" title=".*?" target="_blank" class="j_th_tit ">.+?<\\/a>'), html)
    return post_list


def get_fid(tieba, headers):
    url = "https://tieba.baidu.com/f?kw=" + tieba
    res = get_method(url, headers)
    html = res.text
    html = html.replace('\r', '').replace('\n', '')
    PageData_forum = re.findall(re.compile('PageData.forum = {(.*?)}'), html)
    fid = re.findall(re.compile('\'id\': (.+?),'), PageData_forum[0])
    return fid[0]


def get_mouse_pwd():
    mouse_pwd_t = str(int(int(round(time.time() * 1000))))
    mouse_pwd_fix = '124,122,' + str(random.randint(80, 120)) + ', 98,127,126,122,' + str(random.randint(80, 120)) + ',126,71,127,98,126,98,' + str(random.randint(80, 120)) + ',98,126,98,127,98,126,98,' + str(
        random.randint(80, 120)) + ',98,126,98,127,98, ' + str(random.randint(80, 120)) + ',71,123,' + str(random.randint(80, 120)) + ',122,124,120,71,127,125,' + str(random.randint(80, 120)) + ',118,98,119,127,124, '
    mouse_pwd = mouse_pwd_fix + mouse_pwd_t + '1'
    return mouse_pwd, mouse_pwd_t


def get_BSK(tbs):
    path = os.path.join('.', 'js', 'bsk.js')
    with open(path, 'r') as f:
        source = f.read()
    return execjs.compile(source).call('solve_bsk', tbs)
