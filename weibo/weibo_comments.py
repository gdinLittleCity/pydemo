# encoding=utf-8
import random
from hyper.contrib import HTTP20Adapter
import requests
from urllib.parse import urlparse
import urllib
import json
import time

## 全网某个话题


def get_cum():
    range_char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                  'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    result_str = ''
    for i in range(7):
        random_index = random.randint(0, 35)
        result_str = result_str + range_char.__getitem__(random_index)
    return result_str


def get_all_topic(topic: str):
    cum = get_cum()
    host = 'https://api.weibo.cn'
    total_query_url = get_query_url(topic, 1, cum)
    total = get_total(host + "/2/searchall?" + total_query_url, get_header("/2/searchall?" +total_query_url))
    print('total:' + str(total))
    total_page = int(total/10) + 1
    pos = 0
    for page in range(total_page):
        if page == 0:
            page = page + 1
        query_str_url = get_query_url(topic, page, cum)
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
                before_comment(weibo, topic, pos, page)
            # 微博card list 更多热门微博、更多热门视频、实时微博、相关话题
            if card_type == 11:
                print('第{pos}条微博,card_type:11'.format(pos=pos))
                if 'card_group' in weibo:
                    card_group = weibo['card_group']
                    for card in card_group:
                        if card['card_type'] == 9:
                            before_comment(card, topic, pos, page)
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
        ":path": query_str_url,
        ":scheme": "https",
        "x-sessionid": "7fd91846-cf21-4a74-83e6-d7b817e4455b",
        "x-validator": "9q7W422S9D86SZyRcMld4v0d9vCkd9EHnQUftD+buP0=",
        "x-log-uid": "1020312395856",
        "accept-encoding": "gzip, deflate"
    }

    return headers


def get_query_url(topic, page, cum):
    fid = "100303type=1&q=#{topic}#&t=3".format(topic=topic)
    containerid = "100303type=1&q=#{topic}#&t=3".format(topic=topic)
    t = time.time()
    query_url = 'networktype=wifi&extparam=c_type%3D2%26extquery%3D%23%E7%8E%AF%E5%A2%83%E4%BF%9D%E6%8A%A4%23%26lxid%3D161205569629802854269%26phototab_style%3Dtrue&' \
                'sensors_device_id=none&orifid=231619%24%24100303type%3D1%26t%3D3&uicode=10000003&' \
                'moduleID=708&' \
                'featurecode=10000085&wb_version=4033&c=android&s=6d256569&ft=0&ua=Netease-MuMu__weibo__9.8.4__android__android6.0.1&wm=2468_1001&aid=01A-rd9_CYQtWAm4wSiN4kbxspdxQZKn1D79d7GvCc5JkZIU0.&did=ea134f63d2ebc546eff496ea78bbcb88e18b0cba&' \
                'ext=orifid%3A231619%24%24100303type%3D1%26t%3D3%7Coriuicode%3A10000512_10000003&' \
                'fid={fid}' \
                '&lat=39.90718833333334&lon=116.391075&uid=1020312395856&' \
                'v_f=2&v_p=76&from=1098495010' \
                '&gsid=_2AkMXSotJf8NhqwJRmvgWzWnhZYh_zw7EieKhFnqSJRM3HRl-wT9kqhZctRV6PMh-AW9WGnZqcenZXS6030dwUBzB0iTD&imsi=&' \
                'lang=zh_CN&lfid=100303type%3D1%26t%3D3&' \
                'page={page}&skin=default&count=10&oldwm=2468_1001&sflag=1&oriuicode=10000512_10000003&' \
                'containerid={containerid}&' \
                'ignore_inturrpted_error=true&luicode=10000003&sensors_mark=0&' \
                'android_id=9417726336afd1fa&client_key=8941330ed508132eb3da9328a81bd520&need_new_pop=1&sensors_is_first_day=none&' \
                'container_ext=newhistory%3A0%7Cnettype%3Awifi%7Cshow_topic%3A1%7Cgps_timestamp%3A{time}&need_head_cards=1&' \
                'cum={cum}'.format(fid=urllib.parse.quote(fid), containerid=urllib.parse.quote(containerid), page=page,
                                   time=int(round(t*1000)), cum=cum)

    return query_url

def before_comment(weibo, topic, pos, page):
    item_id = weibo['itemid']
    mid = weibo['mblog']['mid']
    mblog = weibo['mblog']
    print('第{page}页,第{pos}条微博,评论数:{cmt_count},内容:{content}'.format(page=page, pos=pos, cmt_count=mblog['comments_count'], content=str(weibo['mblog']['text'])))
    storege = {'user':'', 'content':'', 'comments_count':'', 'attitudes_count':''}
    storege['user'] = mblog['user']['name']
    storege['content'] = mblog['text']
    storege['comments_count'] = mblog['comments_count']
    storege['attitudes_count'] = mblog['attitudes_count']
    # 长内容微博
    if mblog['isLongText']:
        get_long_text(mid)

    with open("weibo-{topic}.txt".format(topic=topic), 'a', encoding="utf-8") as weibo_file:
        weibo_file.write(json.dumps(storege, ensure_ascii=False) + "\n")
    # 评论
    # if len(item_id) != 0:
    #     storege = get_comments(item_id, topic, mid)
    #     with open("weibo-{topic}.txt".format(topic=topic), 'a', encoding="utf-8") as weibo_file:
    #         weibo_file.write(json.dumps(storege, ensure_ascii=False) + "\n")


def get_comments(item_id, topic, mid):
    storege = {'user': '', 'content': '', 'comments_count': 0, 'attitudes_count': 0}
    cum = get_cum()
    host = 'https://api.weibo.cn'
    query = get_cmt_query_url(item_id, mid, topic, cum)
    headers = get_header(query)
    path_url = host + query
    sessions = requests.session()
    sessions.mount(host, HTTP20Adapter())
    res = sessions.get(url=path_url, headers=headers, timeout=(60, 600))
    res_json_obj = json.loads(res.content)

    if 'status' in res_json_obj:
        weibo_content = res_json_obj['status']
        if 'user' in weibo_content:
            storege['user'] = weibo_content['user']['name']
        if 'text' in weibo_content:
            storege['content'] = weibo_content['text']
        storege['comments_count'] = weibo_content['comments_count']
        storege['attitudes_count'] = weibo_content['attitudes_count']
    return storege
    # print("评论:" + str(res_json_obj))

def cmt_parse(storege, res_json_obj):
    comments = []
    cmt_list = []
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

def get_long_text(weibo_id: str):
    host = 'https://api.weibo.cn'
    path_url = '/2/statuses/longtext_show_batch?networktype=wifi&sensors_device_id=none&moduleID=705&wb_version=4033&c=android&s=08d12f15&ft=0&ua=Netease-MuMu__weibo__9.8.4__android__android6.0.1&wm=2468_1001&aid=01A-rd9_CYQtWAm4wSiN4kbxspdxQZKn1D79d7GvCc5JkZIU0.&v_f=2&v_p=76&from=1098495010&gsid=_2A25NSAhGDeRxGeFO61cU9C7MzjiIHXVsXByOrDV6PUJbkdAfLUH8kWpNQYVgzVpvV-TokR2bee6tTAfmDuGe5a2r&lang=zh_CN&skin=default&oldwm=2468_1001&sflag=1&sensors_mark=0&android_id=9417726336afd1fa&sensors_is_first_day=none' \
               '&cum={cum}'.format(cum=get_cum())
    t = int(round(time.time() * 1000))
    headers = {
        "user-agent": "MuMu_6.0.1_weibo_9.8.4_android",
        ":authority": "api.weibo.cn",
        ":method": "GET",
        ":path": path_url,
        ":scheme": "https",
        "x-sessionid": "7750572e-7e1a-4061-8869-03206d260f95",
        "x-validator": "HiXYKIOi1ZL16SXFiV1aGBm98RtgZpEIRFGE4p+GHsU=",
        "content-type": "multipart/form-data;boundary=------------" + str(t),
        "x-log-uid": "1020312395856",
        "accept-encoding": "gzip, deflate"
    }
    data = {'is_encoded': 0, 'is_show_unvisible': 0,
          'preload_datas': json.dumps({"longtexts":["4614360418488899"]}), 'v_p': 76}

    mh = MultipartFormData.format(data, "------------" + str(t), headers)

    # m = MultipartEncoder(fields=data, boundary='------------1615646263503')
    sessions = requests.session()
    sessions.mount(host, HTTP20Adapter())
    res = sessions.post(url=host+path_url, headers=headers, data=mh)
    # res = sessions.get(url=path_url, headers=headers, timeout=(60, 600))
    res_json_obj = json.loads(res.content)
    print(json.dumps(res_json_obj, ensure_ascii=False))
    return headers


def get_cmt_query_url(item_id, mid, topic, cum):
    orifid = '231619$$100303type=1&q=#&t=3$$100303type=1&q=#{topic}#&t=3'.format(topic=topic)
    lfid = '100303type=1&q=#{topic}#&t=3'.format(topic=topic)
    query = '/2/comments/build_comments?networktype=wifi&sensors_device_id=none&is_mix=1' \
            '&max_id=0&recommend_page=1' \
            '&orifid={orifid}' \
            '&is_show_bulletin=2&uicode=10000002&moduleID=700&trim_user=0&is_reload=1&featurecode=10000085' \
            '&wb_version=4033&is_encoded=0&refresh_type=1' \
            '&lcardid={lcardid}' \
            '&c=android&s=08d12f15&ft=0&id={id}&ua=Netease-MuMu__weibo__9.8.4__android__android6.0.1' \
            '&wm=2468_1001&aid=01A-rd9_CYQtWAm4wSiN4kbxspdxQZKn1D79d7GvCc5JkZIU0.' \
            '&ext=orifid%3A231619%24%24100303type%3D1%26q%3D%23%26t%3D3%24%24100303type%3D1%26q%3D%23%E7%B2%BE%E7%A5%9E%E5%87%BA%E8%BD%A8%E8%AF%A5%E4%B8%8D%E8%AF%A5%E9%80%89%E6%8B%A9%E5%8E%9F%E8%B0%85%23%26t%3D3%7Coriuicode%3A10000010_10000003_10000003%7Cseqid%3A60971487%7Ctype%3A1%7Ct%3A2%7Cpos%3A1-2-0%7Cq%3A%23%E7%B2%BE%E7%A5%9E%E5%87%BA%E8%BD%A8%E8%AF%A5%E4%B8%8D%E8%AF%A5%E9%80%89%E6%8B%A9%E5%8E%9F%E8%B0%85%23%7Cext%3A%26cate%3D306%26mid%3D4614018691498205%26qri%3D8796193685504%26qrt%3D3%26qtime%3D1615624395%26&v_f=2&v_p=76&from=1098495010&gsid=_2A25NSAhGDeRxGeFO61cU9C7MzjiIHXVsXByOrDV6PUJbkdAfLUH8kWpNQYVgzVpvV-TokR2bee6tTAfmDuGe5a2r&lang=zh_CN' \
            '&lfid={lfid}' \
            '&skin=default&count=20&oldwm=2468_1001&sflag=1&oriuicode=10000010_10000003_10000003&ignore_inturrpted_error=true' \
            '&luicode=10000003&sensors_mark=0&android_id=9417726336afd1fa&fetch_level=0' \
            '&is_append_blogs=1&request_type=default&max_id_type=0&sensors_is_first_day=none' \
            '&cum={cum}'.format(orifid=urllib.parse.quote(orifid), lcardid=urllib.parse.quote(item_id), id=mid,
                                ext=urllib.parse.quote(item_id), lfid=urllib.parse.quote(lfid),  cum=cum)
    return query


def get_cmt_count(host, item_id, mid, checktoken, cum):
    query = get_cmt_query_url(item_id, mid, checktoken, cum, 20)
    headers = get_header(query)
    path_url = host + query
    sessions = requests.session()
    sessions.mount(host, HTTP20Adapter())
    res = sessions.get(url=path_url, headers=headers, timeout=(60, 600))
    res_json_obj = json.loads(res.content)
    return res_json_obj['current_cmt_count']

# multipart/form-data
class MultipartFormData(object):
    """multipart/form-data格式转化"""

    @staticmethod
    def format(data, boundary="----WebKitFormBoundary7MA4YWxkTrZu0gW", headers={}):
        """
        form data
        :param: data:  {"req":{"cno":"18990876","flag":"Y"},"ts":1,"sig":1,"v": 2.0}
        :param: boundary: "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        :param: headers: 包含boundary的头信息；如果boundary与headers同时存在以headers为准
        :return: str
        :rtype: str
        """
        # 从headers中提取boundary信息
        if "content-type" in headers:
            fd_val = str(headers["content-type"])
            if "boundary" in fd_val:
                fd_val = fd_val.split(";")[1].strip()
                boundary = fd_val.split("=")[1].strip()
            else:
                raise Exception("multipart/form-data头信息错误，请检查content-type key是否包含boundary")
        # form-data格式定式
        jion_str = '--{}\r\nContent-Disposition: form-data; name="{}"\r\nContent-Type: text/plain;charset:"UTF-8"\r\nContent-Transfer-Encoding: 8bit\r\n\r\n{}\r\n'
        end_str = "--{}--".format(boundary)
        args_str = ""

        if not isinstance(data, dict):
            raise Exception("multipart/form-data参数错误，data参数应为dict类型")
        for key, value in data.items():
            args_str = args_str + jion_str.format(boundary, key, value)

        args_str = args_str + end_str.format(boundary)
        args_str = args_str.replace("\'", "\"")
        return args_str

if __name__ == '__main__':
    get_long_text('')

# get_comments(urllib.parse.quote('seqid:1310177437|type:1|t:2|pos:1-2-0|q:#环境保护#|ext:&cate=26&mid=4590772219026990&qri=576460752303423488&qrt=1&qtime=1612057172&'))
