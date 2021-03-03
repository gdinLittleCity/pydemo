# encoding=utf-8
import threading
import random
import time
from hyper.contrib import HTTP20Adapter
import requests
from urllib.parse import urlparse
import urllib
import json

page = 1
pos = 0

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
def get_all_topic(profile_uid:str, since_id: str):
    global page
    cum = get_cum()
    host = 'https://api.weibo.cn'
    query_pre = "//2/profile/statuses?"
    total_query_url = get_query_url(profile_uid, cum, since_id)
    path = query_pre + total_query_url
    res_json_obj = get_response(host + path, get_header(path))
    total = res_json_obj['cardlistInfo']['total']
    # 单页
    if 'since_id' not in res_json_obj['cardlistInfo']:
        print('微博总数:{total}， {con}'.format(total=str(total), con=str(res_json_obj)))
        parse_weibo_json(profile_uid, res_json_obj)
        return
    # 多页
    else:
        print('微博总数:{total}， {con}'.format(total=str(total), con=str(res_json_obj)))
        since_id_next =res_json_obj['cardlistInfo']['since_id']
        parse_weibo_json(profile_uid, res_json_obj)
        page = page + 1
        get_all_topic(profile_uid, since_id_next)



def parse_weibo_json(profile_uid, res_json_obj):
    global pos, page
    weibos = res_json_obj['cards']
    for weibo in weibos:
        card_type = weibo['card_type']
        # 普通微博card
        if card_type == 9:
            pos = pos + 1
            print('第{page}页微博,第{pos}条微博,card_type:9'.format(page=page, pos=pos))
            before_comment(weibo, pos, page, profile_uid)
        # 微博card list 更多热门微博、更多热门视频、实时微博、相关话题
        if card_type == 11:
            print('第{page}页微博,第{pos}条微博,,card_type:11 - 拆分'.format(page=page, pos=pos))
            if 'card_group' in weibo:
                card_group = weibo['card_group']
                for card in card_group:
                    if card['card_type'] == 9:
                        print('-------第{pos}条微博,实际使用card_type:9'.format(pos=pos))
                        before_comment(card, pos, page, profile_uid)
                        pos = pos + 1
        # 其他微博card不处理


def get_query_url(profile_uid, cum, since_id):
    # 重点在containerid
    # uid 已登录用户id
    since_id_str = ''
    if len(since_id) > 0:
        since_id_str = '&since_id=' + str(since_id)
    query_url = 'networktype=wifi&sensors_device_id=none' \
                '&uicode=10000198&moduleID=708&wb_version=4033' \
                '&c=android&s=08d12f15&ft=0&ua=Netease-MuMu__weibo__9.8.4__android__android6.0.1&wm=2468_1001' \
                '&aid=01A212u2E42R0FrTeYaODL9JPnzYBnf7yILsgPn4bkjDmlbKc.' \
                '&uid=7005540054&v_f=2&v_p=76' \
                '&from=1098495010' \
                '&gsid=_2A25NO1V3DeRxGeFO61cU9C7MzjiIHXVsUe-_rDV6PUJbkdAKLXXukWpNQYVgzSw1ebzUkvAAXMFBhuanTXNwM6E3' \
                '&imsi=&lang=zh_CN' \
                '&skin=default&count=20' \
                '&oldwm=2468_1001' \
                '&sflag=1&oriuicode=10000011' \
                '&containerid=107603{profile_uid}_-_WEIBO_SECOND_PROFILE_WEIBO' \
                '&ignore_inturrpted_error=true' \
                '&luicode=10000011&sensors_mark=0&android_id=82207eba77e0887a' \
                '&client_key=8941330ed508132eb3da9328a81bd520&need_new_pop=1&sensors_is_first_day=none&need_head_cards=0' \
                '{since_id}' \
                '&cum={cum}'.format( profile_uid=profile_uid, since_id=since_id_str, cum=cum)
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


def get_response(url, headers):
    sessions = requests.session()
    sessions.mount(url, HTTP20Adapter())
    res = sessions.get(url=url, headers=headers, timeout=(60, 600))
    sessions.keep_alive = False
    res_json_obj = json.loads(res.content)
    return res_json_obj


def before_comment(weibo, pos, page, profile_uid):
    create_at = weibo['mblog']['created_at']
    weibo_year = get_weibo_create_year(create_at)
    if int(weibo_year) < 2013:
        print('skip.发布时间在2013年之后,发布时间:{create},微博:{content}'.format(create=create_at, content=str(weibo['mblog']['text'])))
        return
    item_id = weibo['itemid']
    mid = weibo['mblog']['mid']
    # 评论数
    cmt_count = weibo['mblog']['comments_count']
    print('第{page}页,第{pos}条微博,发布时间:{year},评论数:{cmt_count},内容:{content}'.format(page=page, pos=pos, year=create_at, cmt_count=cmt_count, content=str(weibo['mblog']['text'])))
    # 评论
    if len(item_id) != 0:
        storege = get_comments(profile_uid, weibo, urllib.parse.quote(item_id), mid, cmt_count)
        with open("weibo.txt", 'a', encoding="utf-8") as finish_file:
            finish_file.write(str(storege) + "\r\n")

def get_weibo_create_year(gmt_time_str:str): # 获取微博发布时间-年份
    return gmt_time_str[len(gmt_time_str)-4: len(gmt_time_str)]

def get_comments(profile_uid, weibo, item_id, mid, cmt_count):
    storege = {'name': '', 'content': '', 'create':'', 'reposts_count': 0, 'comments_count': 0, 'attitudes_count': 0, 'comments': []}
    cum = get_cum()
    create_at = weibo['mblog']['created_at']
    weibo_year = get_weibo_create_year(create_at)

    host = 'https://api.weibo.cn'
    # 总评论数
    cmt_count = cmt_count
    # 单页数据量
    count = 20
    path = get_cmt_query_url(profile_uid, weibo_year, item_id, mid, cum, count, False, 0, '')
    headers = get_header(path)
    path_url = host + path
    sessions = requests.session()
    sessions.mount(host, HTTP20Adapter())
    res = sessions.get(url=path_url, headers=headers, timeout=(60, 600))
    try:
        res_json_obj = json.loads(res.content)
        # 转发数, 评论数, 点赞数, 作者, 内容
        build_weibo_count(res_json_obj, storege)
        # 评论
        storege['comments'].extend(parse_cmt_res(profile_uid, weibo_year, res_json_obj, item_id, mid, count))
    except Exception:
        print(str(item_id) + "评论 解析异常")
        raise Exception
    return storege

def build_weibo_count(res_json_obj, storege):
    if 'status' in res_json_obj:
        weibo_content = res_json_obj['status']
        if 'created_at' in weibo_content:
            storege['create'] = get_weibo_create_year(weibo_content['created_at'])
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

def parse_cmt_res(profile_uid, weibo_year, res_json_obj, item_id, mid, count):
    comments = []
    cmt_list = []
    if 'datas' in res_json_obj:
        cmt_list = res_json_obj['datas']
    if 'root_comments' in res_json_obj:
        cmt_list = res_json_obj['root_comments']
    if 'comments' in res_json_obj:
        cmt_list = res_json_obj['comments']
    if len(cmt_list) == 0:
        print('无评论{data}'.format(data=str(cmt_list)))
        return comments
    for cmt in cmt_list:
        comment = {'user': '', 'text': '', 'cmts': []}
        # datas 结构中 type!=0 的数据为无效评论数据
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
            comment['cmts'] = cycle_cmt(profile_uid, one)
        # root_comments 结构评论
        else:
            cmt_text = cmt['text']
            cmt_user = cmt['user']['name']
            comment['user'] = cmt_user
            comment['text'] = cmt_text
            comment['cmts'] = cycle_cmt(profile_uid, cmt)

        comments.append(comment)
        print('评论:{cmt_content}'.format(cmt_content=str(comment)))
    # 分页评论
    if ('max_id' in res_json_obj and res_json_obj['max_id'] != 0) or ('top_hot_structs' in res_json_obj and any(res_json_obj['top_hot_structs'])):
        print('分页评论:')
        cum = get_cum()
        host = 'https://api.weibo.cn'
        path = get_cmt_query_url(profile_uid, weibo_year, item_id, mid, cum, count, True, res_json_obj['max_id'], '')
        if 'top_hot_structs' in res_json_obj and any(res_json_obj['top_hot_structs']):
            top_hot_structs = res_json_obj['top_hot_structs']
            path = get_cmt_query_url(weibo_year, item_id, mid, cum, count, True, top_hot_structs['call_back_struct']['max_id_str'], top_hot_structs['call_back_struct']['callback_ext_params'])

        headers = get_header(path)
        path_url = host + path
        sessions = requests.session()
        sessions.mount(host, HTTP20Adapter())
        res = sessions.get(url=path_url, headers=headers, timeout=(60, 600))
        try:
            res_json_obj_page = json.loads(res.content)
            comments.extend(parse_cmt_res(profile_uid, weibo_year, res_json_obj_page, item_id, mid, count))
        except Exception:
            print(str(item_id)+"评论 解析异常")
            raise Exception


    return comments

def cycle_cmt(profile_uid, cmt):
    cmt_list = []
    host = 'https://api.weibo.cn'
    # 有二级评论
    if 'more_info' in cmt:
        cmt_id = cmt['id']
        path = get_level2_query_url(profile_uid, cmt_id, False, '')
        headers = get_header(path)
        path_url = host + path
        sessions = requests.session()
        sessions.mount(host, HTTP20Adapter())
        res = sessions.get(url=path_url, headers=headers, timeout=(60, 600))
        res_json_obj_page = json.loads(res.content)
        cmt_list.extend(parse_syscle_cmt_res(res_json_obj_page, profile_uid, cmt_id))
    return cmt_list


def parse_syscle_cmt_res(res_json_obj, profile_uid, cmt_id):
    comments = []
    cmt_list = []
    if 'comments' in res_json_obj:
        cmt_list = res_json_obj['comments']
    if len(cmt_list) == 0:
        print('无评论{data}'.format(data=str(cmt_list)))
        return comments
    for cmt in cmt_list:
        comment = {'user': '', 'text': ''}
        cmt_text = cmt['text']
        cmt_user = cmt['user']['name']
        comment['user'] = cmt_user
        comment['text'] = cmt_text
        comments.append(comment)
        print('评论:{cmt_content}'.format(cmt_content=str(comment)))
    # 分页评论
    if ('max_id' in res_json_obj and res_json_obj['max_id'] != 0) or ('top_hot_structs' in res_json_obj and any(res_json_obj['top_hot_structs'])):
        print('二级分页评论:')
        cum = get_cum()
        host = 'https://api.weibo.cn'
        path = get_level2_query_url(profile_uid, cmt_id, True, res_json_obj['max_id_str'])
        headers = get_header(path)
        path_url = host + path
        sessions = requests.session()
        sessions.mount(host, HTTP20Adapter())
        res = sessions.get(url=path_url, headers=headers, timeout=(60, 600))
        try:
            res_json_obj_page = json.loads(res.content)
            comments.extend(parse_syscle_cmt_res(res_json_obj_page, profile_uid, cmt_id))
        except Exception:
            print("二级评论 解析异常")
            raise Exception
    return comments

def get_level2_query_url(profile_uid, cmt_id, is_page, max_id):
    orifid = '231093_-_selffollowed$$107603{profile_uid}_-_WEIBO_SECOND_PROFILE_WEIBO%24%240'.format(profile_uid=profile_uid)
    oriuicode = '10000011_10000198_10000002'
    ext = 'orifid%3A{orifid}|oriuicode%3A{oriuicode}'.format(orifid= orifid, oriuicode=oriuicode)
    max_id_param_str = 'max_id=0&recommend_page=1&'
    if is_page:
        max_id_param_str = 'max_id=' + str(max_id) + '&'
    url = '/2/comments/build_comments?networktype=wifi&sensors_device_id=none&is_mix=1&&{max_id_param_str}' \
          '&recommend_page=1' \
          '&orifid={orifid}' \
          '&is_show_bulletin=2' \
          '&uicode=10000408' \
          '&moduleID=700&trim_user=0&is_reload=1' \
          '&wb_version=4033&is_encoded=0&c=android&s=08d12f15&ft=0&id={cmt_id}' \
          '&ua=Netease-MuMu__weibo__9.8.4__android__android6.0.1' \
          '&wm=2468_1001&aid=01A212u2E42R0FrTeYaODL9JPnzYBnf7yILsgPn4bkjDmlbKc.' \
          '&ext={ext}&v_f=2&v_p=76&from=1098495010' \
          '&gsid=_2A25NO1V3DeRxGeFO61cU9C7MzjiIHXVsUe-_rDV6PUJbkdAKLXXukWpNQYVgzSw1ebzUkvAAXMFBhuanTXNwM6E3' \
          '&lang=zh_CN&skin=default&count=20' \
          '&oldwm=2468_1001&sflag=1' \
          '&oriuicode={oriuicode}&ignore_inturrpted_error=true' \
          '&luicode=10000002&sensors_mark=0&android_id=82207eba77e0887a' \
          '&fetch_level=1&is_append_blogs=1&request_type=default&max_id_type=0&sensors_is_first_day=none' \
          '&cum=8A58BFCA'.format(max_id_param_str=max_id_param_str,
                                 profile_uid=profile_uid, orifid=orifid, cmt_id=cmt_id, ext=ext, oriuicode=oriuicode)
    return url


def get_cmt_query_url(profile_uid, weibo_year, item_id, mid, cum, count, is_page ,max_id, callback_ext_params):
    max_id_param_str = 'max_id=0&recommend_page=1&'
    is_reload_str = 'is_reload=1&'
    refresh_type_str = 'refresh_type=1&'
    callback_ext_params_str = ''
    if is_page :
        max_id_param_str = 'max_id=' + str(max_id) + '&'
        callback_ext_params_str = str(callback_ext_params) + '&'
    orifid = '231093_-_selffollowed$$107603{profile_uid}_-_WEIBO_SECOND_PROFILE_WEIBO'.format(profile_uid=profile_uid)
    lcardid = '107603{profile_uid}_-_WEIBO_SECOND_PROFILE_WEIBO_-_{mid}'.format(profile_uid=profile_uid, mid=mid)
    ext = 'orifid:{orifid}|oriuicode:10000011_10000198'
    query = '/2/comments/build_comments?networktype=wifi&sensors_device_id=none&is_mix=1&{max_id_param_str}' \
            'is_show_bulletin=2&uicode=10000002&moduleID=700&' \
            '&trim_user=0&{is_reload_str}featurecode=10000085&wb_version=4033&is_encoded=0&' \
            '{refresh_type_str}' \
            '&c=android&s=08d12f15&ft=0&id={mid}&ua=Netease-MuMu__weibo__9.8.4__android__android6.0.1&wm=2468_1001&' \
            'aid=01A212u2E42R0FrTeYaODL9JPnzYBnf7yILsgPn4bkjDmlbKc.&' \
            'v_f=2&v_p=76&from=1098495010&gsid=_2A25NKxlMDeRxGeFO61cU9C7MzjiIHXVsYSuErDV6PUJbkdAKLXXukWpNQYVgzV_sm-sh-eWyo4KFeIQPmDlilkmt&lang=zh_CN&' \
            '&lfid=230283{profile_uid}' \
            '&skin=default&count={count}&oldwm=2468_1001&sflag=1&' \
            'oriuicode=10000011_10000198&' \
            'orifid={orifid}&lcardid={lcardid}&ext={ext}'\
            'ignore_inturrpted_error=true&luicode=10000003&sensors_mark=0&android_id=82207eba77e0887a&' \
            'fetch_level=0&is_append_blogs=1&{callback_ext_params_str}request_type=default&max_id_type=0&sensors_is_first_day=none' \
            '&cum={cum}'.format(max_id_param_str=max_id_param_str,is_reload_str = is_reload_str,
                                refresh_type_str=refresh_type_str,
                                profile_uid=profile_uid,
                                orifid=orifid, lcardid=lcardid, ext=ext,
                                mid=mid, count=count,
                                callback_ext_params_str=callback_ext_params_str,
                                cum=cum)
    return query


if __name__ == '__main__':
    get_all_topic('1875286971', '')
