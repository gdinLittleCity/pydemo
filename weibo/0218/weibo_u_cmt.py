# encoding=utf-8
import random
from hyper.contrib import HTTP20Adapter
import requests
from urllib.parse import urlparse
import urllib
import json

#获取cum
def get_cum():
    range_char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                  'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    result_str = ''
    for i in range(9):
        random_index = random.randint(0, 35)
        result_str = result_str + range_char.__getitem__(random_index)
    return result_str

#获取博主相关话题微博
def get_all_topic(topic, uid):
    cum = get_cum()
    host = 'https://api.weibo.cn'
    total_query_url = get_query_url(topic, uid, 1, cum)
    path = "/2/searchall?" + total_query_url
    total = get_total(host + path, get_header(path))
    print('topic:{topic}, 微博总数total:{total}'.format(topic=topic, total=str(total)))
    if total == 0:
        print('topic:{topic} 无微博'.format(topic=topic))
        return
    total_page = int(total/10) + 1
    pos = 0
    for page in range(total_page):
        if page == 0:
            page = page + 1
        query_str_url = get_query_url(topic, uid, page, cum)
        headers = get_header("/2/searchall?" +query_str_url)

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
                before_comment(weibo, pos, page)
            # 微博card list 更多热门微博、更多热门视频、实时微博、相关话题
            if card_type == 11:
                print('第{pos}条微博,card_type:11 - 拆分'.format(pos=pos))
                if 'card_group' in weibo:
                    card_group = weibo['card_group']
                    for card in card_group:
                        if card['card_type'] == 9:
                            print('-------第{pos}条微博,实际使用card_type:9'.format(pos=pos))
                            pos = pos + 1
                            before_comment(card, pos, page)
            # 其他微博card不处理


def get_query_url(topic, uid, page, cum):
    query_url = 'networktype=wifi&extparam=phototab_style%3Dtrue&sensors_device_id=none' \
                '&orifid=231093_-_selffollowed%24%24231093_-_selfgroup_-_mygroup' \
                '&uicode=10000003&moduleID=708&featurecode=10000085' \
                '&wb_version=4033&c=android&s=08d12f15&ft=0' \
                '&ua=Netease-MuMu__weibo__9.8.4__android__android6.0.1' \
                '&wm=2468_1001&aid=01A-rd9_CYQtWAm4wSiN4kbxspdxQZKn1D79d7GvCc5JkZIU0.' \
                '&ext=orifid%3A231093_-_selffollowed%24%24231093_-_selfgroup_-_mygroup%7Coriuicode%3A10000011_10000011' \
                '&fid=100303type%3D401%26q%3D{topic}%26t%3D0' \
                '&lat=39.90718833333334&lon=116.391075' \
                '&uid=7005540054&v_f=2&v_p=76&from=1098495010' \
                '&gsid=_2A25NKnwlDeRxGeFO61cU9C7MzjiIHXVsfojtrDV6PUJbkdAfLUH8kWpNQYVgzRCqgpg57i5Y5mk_6NWKzvsMzCqQ' \
                '&imsi=&lang=zh_CN&' \
                'lfid=230283{uid}&' \
                'page={page}&skin=default&count=10&oldwm=2468_1001&sflag=1&oriuicode=10000011_10000011' \
                '&containerid=100303type%3D401%26q%3D{topic}%26t%3D0' \
                '&ignore_inturrpted_error=true&luicode=10000198&sensors_mark=0&android_id=9417726336afd1fa' \
                '&client_key=8941330ed508132eb3da9328a81bd520&need_new_pop=1&sensors_is_first_day=none' \
                '&container_ext=newhistory%3A0%7Cnettype%3Awifi%7Cprofile_uid%3A{uid}%7Cshow_topic%3A1%7Cgps_timestamp%3A1613633977964' \
                '&need_head_cards=1' \
                '&cum={cum}'.format(topic=topic, uid=uid, page=page, cum=cum)
    return query_url


def get_header(path):
    headers = {
        "user-agent": "MuMu_6.0.1_weibo_9.8.4_android",
        ":authority": "api.weibo.cn",
        ":method": "GET",
        ":path": path,
        ":scheme": "https",
        "x-sessionid": "386f126f-f571-42ec-8082-39b435deaa44",
        "x-validator": "DlF0xMah0uhe4UhyOWdMxkign5rCslQrwX84e8oYRm8=",
        "x-log-uid": "7005540054",
        "accept-encoding": "gzip, deflate"
    }
    return headers


def get_total(url, headers):
    sessions = requests.session()
    sessions.mount(url, HTTP20Adapter())
    res = sessions.get(url=url, headers=headers, timeout=(60, 600))
    sessions.keep_alive = False
    res_json_obj = json.loads(res.content)
    total = res_json_obj['cardlistInfo']['total']
    return total


def before_comment(weibo, pos, page):
    item_id = weibo['itemid']
    mid = weibo['mblog']['mid']
    # 评论数
    cmt_count = weibo['mblog']['comments_count']
    print('第{page}页,第{pos}条微博,平均数:{cmt_count},内容:{content}'.format(page=page, pos=pos, cmt_count=cmt_count, content=str(weibo['mblog']['text'])))
    # 评论
    if len(item_id) != 0 and cmt_count > 0:
        storege = get_comments(urllib.parse.quote(item_id), mid, cmt_count)
        with open("weibo.txt", 'a', encoding="utf-8") as finish_file:
            finish_file.write(str(storege) + "\r\n")


def get_comments(item_id, mid, cmt_count):
    storege = {'name': '', 'content': '', 'reposts_count': 0, 'comments_count': 0, 'attitudes_count': 0, 'comments': []}
    cum = get_cum()
    host = 'https://api.weibo.cn'
    # 总评论数
    cmt_count = cmt_count
    # 单页数据量
    count = (int(cmt_count / 10) + 1) * 10
    path = get_cmt_query_url(item_id, mid, cum, count, False, 0, '')
    headers = get_header(path)
    path_url = host + path
    sessions = requests.session()
    sessions.mount(host, HTTP20Adapter())
    res = sessions.get(url=path_url, headers=headers, timeout=(60, 600))
    res_json_obj = json.loads(res.content)
    # 转发数, 评论数, 点赞数, 作者, 内容
    build_weibo_count(res_json_obj, storege)
    # 评论
    storege['comments'].extend(parse_cmt_res(res_json_obj, item_id, mid, cum, count))
    return storege

def build_weibo_count(res_json_obj, storege):
    if 'status' in res_json_obj:
        weibo_content = res_json_obj['status']
        # 转发数
        if 'reposts_count' in weibo_content:
            storege['reposts_count'] = weibo_content['reposts_count']
        # 评论数
        if 'comments_count' in weibo_content:
            storege['comments_count'] = weibo_content['comments_count']
        # 点赞数
        if 'attitudes_count' in weibo_content:
            storege['attitudes_count'] = weibo_content['attitudes_count']
        if 'user' in weibo_content:
            storege['name'] = weibo_content['user']['name']
        if 'text' in weibo_content:
            storege['content'] = weibo_content['text']

def parse_cmt_res(res_json_obj, item_id, mid, count):
    comments = []
    cmt_list = []
    if 'datas' in res_json_obj:
        cmt_list = res_json_obj['datas']
    if 'root_comments' in res_json_obj:
        cmt_list = res_json_obj['root_comments']
    if len(cmt_list) == 0:
        print('无评论{data}'.format(data=str(cmt_list)))
        return comments
    for cmt in cmt_list:
        comment = {'user': '', 'text': '', 'cmts': []}
        if 'type' in cmt and cmt['type'] != 0:
            print('无正常评论:{data}'.format(data=str(cmt)))
            continue
        # datas 结构评论
        if 'type' in cmt:
            one = cmt['data']
            cmt_text = one['text']
            cmt_user = one['user']['name']
            comment['user'] = cmt_user
            comment['text'] = cmt_text
            comment['cmts'] = cycle_cmt(one)
        # root_comments 结构评论
        else:
            cmt_text = cmt['text']
            cmt_user = cmt['user']['name']
            comment['user'] = cmt_user
            comment['text'] = cmt_text
            comment['cmts'] = cycle_cmt(cmt)

        comments.append(comment)
        print('评论:{cmt_content}'.format(cmt_content=str(comment)))
    # 分页评论
    if ('max_id' in res_json_obj and res_json_obj['max_id'] != 0 ) or ('top_hot_structs' in res_json_obj and any(res_json_obj['max_id'])) :
        print('分页评论:')
        cum = get_cum()
        host = 'https://api.weibo.cn'
        path = get_cmt_query_url(item_id, mid, cum, count, False, res_json_obj['max_id'], '')
        headers = get_header(path)
        path_url = host + path
        sessions = requests.session()
        sessions.mount(host, HTTP20Adapter())
        res = sessions.get(url=path_url, headers=headers, timeout=(60, 600))
        res_json_obj_page = json.loads(res.content)
        comments.extend(parse_cmt_res(res_json_obj_page, item_id, mid, count))

    return comments

def cycle_cmt(cmt):
    cmt_list = []
    if 'comments' in cmt and len(cmt['comments']) > 0:
        for cmt_com in cmt['comments']:
            com = {'user': '', 'text': ''}
            cmt_com_text = cmt_com['text']
            cmt_com_user = cmt_com['user']['name']
            com['user'] = cmt_com_user
            com['text'] = cmt_com_text
            cmt_list.append(com)

def get_cmt_query_url(item_id, mid, cum, count, is_page ,max_id, callback_ext_params):
    max_id_param_str = 'max_id=0&recommend_page=1&'
    is_reload_str = 'is_reload=1&'
    refresh_type_str = 'refresh_type=1&'
    callback_ext_params_str = ''
    if is_page :
        max_id_param_str = 'max_id=' + str(max_id) + '&'
        callback_ext_params_str = str(callback_ext_params) + '&'

    query = '/2/comments/build_comments?networktype=wifi&sensors_device_id=none&is_mix=1&{max_id_param_str}' \
            'orifid=231619%24%24100303type%3D1%26t%3D3%24%24100103type%3D1%26q%3D%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%26t%3D2&' \
            'is_show_bulletin=2&uicode=10000002&moduleID=700&' \
            '&trim_user=0&{is_reload_str}featurecode=10000085&wb_version=4033&is_encoded=0&' \
            '{refresh_type_str}' \
            'lcardid={lcardid}' \
            '&c=android&s=6d256569&ft=0&id={mid}&ua=Netease-MuMu__weibo__9.8.4__android__android6.0.1&wm=2468_1001&' \
            'aid=01A-rd9_CYQtWAm4wSiN4kbxspdxQZKn1D79d7GvCc5JkZIU0.&' \
            'did=ea134f63d2ebc546eff496ea78bbcb88e18b0cba&' \
            'ext=orifid%3A231619%24%24100303type%3D1%26t%3D3%24%24100103type%3D1%26q%3D%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%26t%3D2%7Coriuicode%3A10000512_10000003_10000003%7C{ext}&' \
            'v_f=2&v_p=76&from=1098495010&gsid=_2AkMXSotJf8NhqwJRmvgWzWnhZYh_zw7EieKhFnqSJRM3HRl-wT9kqhZctRV6PMh-AW9WGnZqcenZXS6030dwUBzB0iTD&lang=zh_CN&' \
            'lfid=100103type%3D1%26q%3D%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%26t%3D2&skin=default&count={count}&oldwm=2468_1001&sflag=1&' \
            'oriuicode=10000512_10000003_10000003&ignore_inturrpted_error=true&luicode=10000003&sensors_mark=0&android_id=9417726336afd1fa&' \
            'fetch_level=0&is_append_blogs=1&{callback_ext_params_str}request_type=default&max_id_type=0&sensors_is_first_day=none' \
            '&cum={cum}'.format(max_id_param_str=max_id_param_str,is_reload_str = is_reload_str,
                                refresh_type_str=refresh_type_str,
                                lcardid=item_id,
                                mid=mid, ext=item_id, count=count,
                                callback_ext_params_str=callback_ext_params_str,
                                cum=cum)
    return query


# print(get_query_url(urllib.parse.quote('#花样滑冰'),'1819318401', 1 , get_cum()))
# 1819318401 - 央视网体育

get_all_topic(urllib.parse.quote('#冬奥会'), '1819318401')