# encoding=utf-8
import random
from hyper.contrib import HTTP20Adapter
import requests
from urllib.parse import urlparse
import urllib
import os
import json


def get_cum():
    range_char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                  'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    result_str = ''
    for i in range(7):
        random_index = random.randint(0, 35)
        result_str = result_str + range_char.__getitem__(random_index)
    # print("cum:{cum}".format(cum=result_str))
    return result_str


def get_all_topic():
    cum = get_cum()
    check_token = 'e32a4e7618afbe3c3cc6ed65e9ddc90c'
    host = 'https://api.weibo.cn'

    total_query_url = get_query_url(check_token, 1, cum)
    total = get_total(host + "/2/searchall?" + total_query_url, get_header(total_query_url))
    print('total:' + str(total))
    total_page = int(total/10) + 1
    pos = 0
    for page in range(total_page):
        if page == 0:
            page = page + 1
        query_str_url = get_query_url(check_token, page, cum)
        headers = get_header(query_str_url)

        path_url = host + "/2/searchall" + "?" + query_str_url
        sessions = requests.session()
        sessions.mount(host, HTTP20Adapter())
        res = sessions.get(url=path_url, headers=headers, timeout=(60, 600))
        res_json_obj = json.loads(res.content)

        print("第{page}页微博:{con}".format(page=page, con=str(res_json_obj)))
        weibos = res_json_obj['cards']
        for weibo in weibos:
            card_type = weibo['card_type']
            pos = pos + 1
            # 普通微博card
            if card_type == 9:
                print('第{pos}条微博,card_type:9'.format(pos=pos))
                before_comment(weibo, check_token, pos, page)
            # 微博card list 更多热门微博、更多热门视频、实时微博、相关话题
            if card_type == 11:
                print('第{pos}条微博,card_type:11'.format(pos=pos))
                if 'card_group' in weibo:
                    card_group = weibo['card_group']
                    for card in card_group:
                        if card['card_type'] == 9:
                            before_comment(card, check_token, pos, page)
            # 其他微博card不处理



# url, headers
def get_total(url, headers):
    sessions = requests.session()
    sessions.mount(url, HTTP20Adapter())
    res = sessions.get(url=url, headers=headers, timeout=(60, 600))
    sessions.keep_alive = False
    res_json_obj = json.loads(res.content)
    total = res_json_obj['cardlistInfo']['total']
    return total


def get_header(query_str_url):
    headers = {
        "user-agent": "MuMu_6.0.1_weibo_9.8.4_android",
        ":authority": "api.weibo.cn",
        ":method": "GET",
        ":path": "/2/searchall?" + query_str_url,
        ":scheme": "https",
        "x-sessionid": "7fd91846-cf21-4a74-83e6-d7b817e4455b",
        "x-validator": "9q7W422S9D86SZyRcMld4v0d9vCkd9EHnQUftD+buP0=",
        "x-log-uid": "1020312395856",
        "accept-encoding": "gzip, deflate"
    }

    return headers


def get_query_url(checktoken, page, cum):
    query_url = 'networktype=wifi&extparam=c_type%3D2%26extquery%3D%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%26lxid%3D161205569629802854269%26phototab_style%3Dtrue&' \
                'sensors_device_id=none&orifid=231619%24%24100303type%3D1%26t%3D3&uicode=10000003&' \
                'moduleID=708&checktoken=checktoken={checktoken}&' \
                'featurecode=10000085&wb_version=4033&c=android&s=6d256569&ft=0&ua=Netease-MuMu__weibo__9.8.4__android__android6.0.1&wm=2468_1001&aid=01A-rd9_CYQtWAm4wSiN4kbxspdxQZKn1D79d7GvCc5JkZIU0.&did=ea134f63d2ebc546eff496ea78bbcb88e18b0cba&ext=orifid%3A231619%24%24100303type%3D1%26t%3D3%7Coriuicode%3A10000512_10000003&fid=100103type%3D1%26q%3D%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%26t%3D2&lat=39.90718833333334&lon=116.391075&uid=1020312395856&v_f=2&v_p=76&from=1098495010&gsid=_2AkMXSotJf8NhqwJRmvgWzWnhZYh_zw7EieKhFnqSJRM3HRl-wT9kqhZctRV6PMh-AW9WGnZqcenZXS6030dwUBzB0iTD&imsi=&lang=zh_CN&lfid=100303type%3D1%26t%3D3&' \
                'page={page}&skin=default&count=10&oldwm=2468_1001&sflag=1&oriuicode=10000512_10000003&containerid=100103type%3D1%26q%3D%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%26t%3D2&ignore_inturrpted_error=true&luicode=10000003&sensors_mark=0&android_id=9417726336afd1fa&client_key=8941330ed508132eb3da9328a81bd520&need_new_pop=1&sensors_is_first_day=none&container_ext=newhistory%3A0%7Cnettype%3Awifi%7Cshow_topic%3A1%7Cgps_timestamp%3A1612055655798&need_head_cards=1&' \
                'cum={cum}'.format(checktoken=checktoken, page=page, cum=cum)

    return query_url

def before_comment(weibo, checktoken, pos, page):

    item_id = weibo['itemid']
    mid = weibo['mblog']['mid']
    # print('item_id:' + str(item_id))
    cmt_count = weibo['mblog']['comments_count']
    print('第{page}页,第{pos}条微博,平均数:{cmt_count},内容:{content}'.format(page=page, pos=pos, cmt_count=cmt_count, content=str(weibo['mblog']['text'])))
    # 评论
    if len(item_id) != 0 and cmt_count > 0:
        storege = get_comments(urllib.parse.quote(item_id), checktoken, mid, cmt_count)
        with open("weibo.txt", 'a', encoding="utf-8") as finish_file:
            finish_file.write(str(storege) + "\r\n")


def get_comments(item_id, checktoken, mid, cmt_count):
    # https://api.weibo.cn/2/comments/build_comments?networktype=wifi&sensors_device_id=none&is_mix=1&max_id=0&recommend_page=1&orifid=231619%24%24100303type%3D1%26t%3D3%24%24100103type%3D1%26q%3D%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%26t%3D2&is_show_bulletin=2&uicode=10000002&moduleID=700&checktoken=e32a4e7618afbe3c3cc6ed65e9ddc90c&trim_user=0&is_reload=1&featurecode=10000085&wb_version=4033&is_encoded=0&refresh_type=1&lcardid=seqid%3A1310177437%7Ctype%3A1%7Ct%3A2%7Cpos%3A1-2-1%7Cq%3A%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%7Cext%3A%26cate%3D26%26mid%3D4585651297584222%26qri%3D576460752303423488%26qrt%3D1%26qtime%3D1612057172%26&c=android&s=6d256569&ft=0&id=4585651297584222&ua=Netease-MuMu__weibo__9.8.4__android__android6.0.1&wm=2468_1001&aid=01A-rd9_CYQtWAm4wSiN4kbxspdxQZKn1D79d7GvCc5JkZIU0.&did=ea134f63d2ebc546eff496ea78bbcb88e18b0cba&ext=orifid%3A231619%24%24100303type%3D1%26t%3D3%24%24100103type%3D1%26q%3D%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%26t%3D2%7Coriuicode%3A10000512_10000003_10000003%7Cseqid%3A1310177437%7Ctype%3A1%7Ct%3A2%7Cpos%3A1-2-1%7Cq%3A%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%7Cext%3A%26cate%3D26%26mid%3D4585651297584222%26qri%3D576460752303423488%26qrt%3D1%26qtime%3D1612057172%26&v_f=2&v_p=76&from=1098495010&gsid=_2AkMXSotJf8NhqwJRmvgWzWnhZYh_zw7EieKhFnqSJRM3HRl-wT9kqhZctRV6PMh-AW9WGnZqcenZXS6030dwUBzB0iTD&lang=zh_CN&lfid=100103type%3D1%26q%3D%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%26t%3D2&skin=default&count=20&oldwm=2468_1001&sflag=1&oriuicode=10000512_10000003_10000003&ignore_inturrpted_error=true&luicode=10000003&sensors_mark=0&android_id=9417726336afd1fa&fetch_level=0&is_append_blogs=1&request_type=default&max_id_type=0&sensors_is_first_day=none&cum=800B27B4
    storege = {'name': '', 'content': '', 'comments': []}
    comments = []
    cum = get_cum()
    host = 'https://api.weibo.cn'
    # 总评论数
    cmt_count = cmt_count
    # 单页数据量
    count = (int(cmt_count / 10) + 1) * 10

    query = get_cmt_query_url(item_id, mid, checktoken, cum, count)
    headers = get_cmt_header(query)
    path_url = host + "/2/comments/build_comments" + "?" + query
    sessions = requests.session()
    sessions.mount(host, HTTP20Adapter())
    res = sessions.get(url=path_url, headers=headers, timeout=(60, 600))
    res_json_obj = json.loads(res.content)
    cmt_list = []
    if 'status' in res_json_obj:
        weibo_content = res_json_obj['status']
        if 'user' in weibo_content:
            storege['name'] = res_json_obj['status']['user']['name']
        if 'text' in weibo_content:
            storege['content'] = res_json_obj['status']['text']
    if 'datas' in res_json_obj:
        cmt_list = res_json_obj['datas']
    if 'root_comments' in res_json_obj:
        cmt_list = res_json_obj['root_comments']
    if len(cmt_list) == 0:
        print('无评论{data}'.format(data=str(cmt_list)))
        return storege
    for cmt in cmt_list:
        comment = {'user':'', 'text':'', 'cmts':[]}
        if 'type' in cmt and cmt['type'] != 0:
            print('无正常评论:{data}'.format(data=str(cmt)))
            continue
        if 'type' in cmt:
            # 无嵌套
            one = cmt['data']
            cmt_text = one['text']
            cmt_user = one['user']['name']
            comment['user'] = cmt_user
            comment['text'] = cmt_text
        else:
            cmt_text = cmt['text']
            cmt_user = cmt['user']['name']
            comment['user'] = cmt_user
            comment['text'] = cmt_text

            if 'comments' in cmt and len(cmt['comments']) > 0:
                for cmt_com in cmt['comments']:
                    com = {'user':'', 'text':''}
                    cmt_com_text = cmt_com['text']
                    cmt_com_user = cmt_com['user']['name']
                    com['user'] = cmt_com_user
                    com['text'] = cmt_com_text
                    comment['cmts'].append(com)

        comments.append(comment)
        print('评论:{cmt_content}'.format(cmt_content=str(comment)))
    storege['comments'].append(comments)
    return storege
    # print("评论:" + str(res_json_obj))

def get_cmt_header(query):
    headers = {
        "user-agent": "MuMu_6.0.1_weibo_9.8.4_android",
        ":authority": "api.weibo.cn",
        ":method": "GET",
        ":path": "/2/comments/build_comments?" + query,
        ":scheme": "https",
        "x-sessionid": "7750572e-7e1a-4061-8869-03206d260f95",
        "x-validator": "HiXYKIOi1ZL16SXFiV1aGBm98RtgZpEIRFGE4p+GHsU=",
        "x-log-uid": "1020312395856",
        "accept-encoding": "gzip, deflate"
    }
    return headers

def get_cmt_query_url(item_id,mid,checktoken, cum,count):
    query = '/2/comments/build_comments?networktype=wifi&sensors_device_id=none&is_mix=1&max_id=0&recommend_page=1&' \
            'orifid=231619%24%24100303type%3D1%26t%3D3%24%24100103type%3D1%26q%3D%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%26t%3D2&' \
            'is_show_bulletin=2&uicode=10000002&moduleID=700&' \
            'checktoken={checktoken}&trim_user=0&is_reload=1&featurecode=10000085&wb_version=4033&is_encoded=0&' \
            'refresh_type=1&' \
            'lcardid={lcardid}' \
            '&c=android&s=6d256569&ft=0&id={mid}&ua=Netease-MuMu__weibo__9.8.4__android__android6.0.1&wm=2468_1001&' \
            'aid=01A-rd9_CYQtWAm4wSiN4kbxspdxQZKn1D79d7GvCc5JkZIU0.&' \
            'did=ea134f63d2ebc546eff496ea78bbcb88e18b0cba&' \
            'ext=orifid%3A231619%24%24100303type%3D1%26t%3D3%24%24100103type%3D1%26q%3D%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%26t%3D2%7Coriuicode%3A10000512_10000003_10000003%7C{ext}&' \
            'v_f=2&v_p=76&from=1098495010&gsid=_2AkMXSotJf8NhqwJRmvgWzWnhZYh_zw7EieKhFnqSJRM3HRl-wT9kqhZctRV6PMh-AW9WGnZqcenZXS6030dwUBzB0iTD&lang=zh_CN&' \
            'lfid=100103type%3D1%26q%3D%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%26t%3D2&skin=default&count={count}&oldwm=2468_1001&sflag=1&' \
            'oriuicode=10000512_10000003_10000003&ignore_inturrpted_error=true&luicode=10000003&sensors_mark=0&android_id=9417726336afd1fa&' \
            'fetch_level=0&is_append_blogs=1&request_type=default&max_id_type=0&sensors_is_first_day=none' \
            '&cum={cum}'.format(lcardid=item_id, mid=mid, ext=item_id, checktoken=checktoken,count=count, cum=cum)
    return query


def get_cmt_count(host, item_id, mid, checktoken, cum):
    query = get_cmt_query_url(item_id, mid, checktoken, cum, 20)
    headers = get_cmt_header(query)
    path_url = host + "/2/comments/build_comments" + "?" + query
    sessions = requests.session()
    sessions.mount(host, HTTP20Adapter())
    res = sessions.get(url=path_url, headers=headers, timeout=(60, 600))
    res_json_obj = json.loads(res.content)
    return res_json_obj['current_cmt_count']


get_all_topic()

# get_comments(urllib.parse.quote('seqid:1310177437|type:1|t:2|pos:1-2-0|q:#环境保护#|ext:&cate=26&mid=4590772219026990&qri=576460752303423488&qrt=1&qtime=1612057172&'))
