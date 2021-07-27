import os
import random

from bs4 import BeautifulSoup

from method import (get_BSK, get_fid, get_mouse_pwd, get_post_list, get_tbs,
                    post_method)


def auto_post(headers, tieba, fid, tid, tbs, post_content, mouse_pwd, mouse_pwd_t, bsk):
    url = 'https://tieba.baidu.com/f/commit/post/add'
    headers['Referer'] = 'https://tieba.baidu.com/p/' + tid
    postdata = {
        'ie': 'utf-8',
        'kw': tieba,
        'fid': fid,  # 贴吧ID
        'tid': tid,  # 贴吧中的帖子ID
        'vcode_md5': '',
        'floor_num': '0',
        'rich_text': '1',
        'tbs': tbs,
        'content': post_content,
        'basilisk': '1',
        'files': [],
        'mouse_pwd': mouse_pwd,
        'mouse_pwd_t': mouse_pwd_t,
        'mouse_pwd_isclick': '0',
        '__type__': 'reply',
        '_BSK': bsk,
    }
    res = post_method(url, postdata=postdata, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


if __name__ == '__main__':
    TIEBA_COOKIE = str(os.environ.get("TIEBA_COOKIE2"))
    headers = {
        'X-Forwarded-For': '121.238.47.136',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67',
        'Cookie': TIEBA_COOKIE
    }

    tbs = get_tbs(headers)
    post_content = '[emotion pic_type=1 width=30 height=30]//tb2.bdstatic.com/tb/editor/images/face/i_f' + str(random.randint(10, 50)) + '.png?t=20140803[/emotion]'
    test_list = ['杨超越', '核战避难所']
    for tieba in test_list:
        post_list = get_post_list(tieba, headers)
        fid = get_fid(tieba, headers)
        mouse_pwd, mouse_pwd_t = get_mouse_pwd()
        bsk = get_BSK(tbs)
        print(bsk)
        # result = auto_post(headers, tieba, fid, post_list[random.randint(1, 5)], tbs, post_content, mouse_pwd, mouse_pwd_t, bsk)
        # print(result)
