#encoding=utf-8
import requests
import argparse
from hyper.contrib import HTTP20Adapter
from urllib.parse import urlparse
import urllib
import os
import re
import getopt

def m3u8_down(url, cookie):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
               "Sec-Fetch-Site": "same-origin",
               "Referer": "https://pan.baidu.com/play/video",
               "Host": "pan.baidu.com",
               "Cookie": cookie
               }
    res = requests.get(url=url, headers=headers)
    with open('soure_url_list.txt', "wb") as code:
        code.write(res.content)
    v_down(cookie)

def parse_url_list():
    with open('soure_url_list.txt', "r") as code:
        soure_list = code.readlines()
    line_num = 0
    count = 0
    call_num =0
    for line in soure_list:
        count = count +1
        if line.find("EXT-X-DISCONTINUITY") > 0:
            continue
        if line_num < 3 or len(soure_list) - 3 < line_num or line_num % 2 == 0:
            line_num = line_num + 1
            continue
        else:
            print("行数:{num}, 内容:{content}".format(num=count, content= line))
            line_num = line_num + 1
            call_num = call_num + 1

def v_down(cookie):
    with open('soure_url_list.txt', "r") as code:
        soure_list = code.readlines()
    line_num = 0
    count = 0
    call_num = 0
    for line in soure_list:
        count = count +1
        if line.find("EXT-X-DISCONTINUITY") > 0:
            continue
        if line_num < 3 or len(soure_list) - 3 < line_num or line_num % 2 == 0:
            line_num = line_num + 1
            continue
        else:
            print("行数:{num}, 内容:{content}".format(num=count, content= line))
            line_num = line_num + 1
            call_num = call_num + 1
            parsed_result = urlparse(line)
            out_file_name = remove(urllib.parse.unquote(urllib.parse.parse_qs(parsed_result.query).get('fn')[0]))
            file_name = out_file_name.replace(".", "_"+str(call_num)+".")
            print('file_name:{fileName}'.format(fileName=file_name))
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
                ":authority": "v1.baidupcs.com",
                ":method": "GET",
                ":path": parsed_result.path + "?" + parsed_result.query,
                ":scheme": "https",
                "accept": "*/*",
                "accept-encoding": "gzip,deflate,br",
                "accept-language": "zh-CN,zh;q=0.9",
                "origin": "https://pan.baidu.com",
                "referer": "https://pan.baidu.com",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "Cookie": cookie
            }
            sessions = requests.session()
            sessions.mount('https://v1.baidupcs.com', HTTP20Adapter())
            res = sessions.get(url=line, headers=headers, timeout=None)
            print("status code:{status}".format(status = res.status_code))
            if res.status_code == 200:
                if not os.path.exists('input') :
                    os.mkdir('input')
                input_path = os.path.abspath('input')
                # 写入list文件
                with open(os.path.join(input_path, 'list.txt'), 'a', encoding="utf-8") as code:
                    code.write("file \'"+file_name+"\' \n")
                with open(os.path.join(input_path, file_name), "wb") as code:
                    code.write(res.content)
            else:
                print(res.content)

    ffmpeg_call(out_file_name)


def write_file_list(file_name):
    print(os.path.abspath(file_name))


def ffmpeg_call(out_file_name):
    list_path = os.path.abspath("list.txt")
    input_path = os.path.abspath('input')
    cmd = "ffmpeg -f concat -safe 0 -i "+os.path.join(input_path, "list.txt")+" -c copy " + os.path.join(input_path, out_file_name)
    print("合并 cmd :[{hcmd}]".format(hcmd=cmd))
    os.system(cmd)
    del_cmd = "del "+ os.path.join(input_path, "*_*.mp4")
    del_list_cmd = "del " + os.path.join(input_path, "list.txt")
    print("delete cmd :[{dele}]".format(dele=del_cmd))
    print("delete list cmd :[{del_list}]".format(del_list=del_list_cmd))
    # 删除视频分片, 视频列表文件
    # os.system(del_cmd)
    # os.system(del_list_cmd)

def remove(string):
    pattern = re.compile(r'\s+')
    return re.sub(pattern,'', string)

def main(argv):
    try:
        options, args = getopt.getopt(argv, "u:c:", ["help", "ip=", "port="])
    except getopt.GetoptError:
        os.sys.exit()
    url = ""
    cookie = ""
    for option, value in options:
        if option in ("-u", "--url"):
            print("url is: {0}".format(value))
            url = value
        if option in ("-c", "--cookie"):
            print("cookie is: {0}".format(value))
            cookie = value
    m3u8_down(url, cookie)
    print("error args: {0}".format(args))

# if __name__ == '__main__':
#     main(os.sys.argv[1:])
# ffmpeg_call("out.mp4")
# url = "https://pan.baidu.com/api/streaming?path=%2F02-%E5%9F%BA%E7%A1%80%E7%8F%AD-%E9%83%91%E6%99%93%E5%8D%9A%EF%BC%88%E6%9B%B4%E6%96%B0%E8%87%B3104%E8%AE%B2%EF%BC%89%2F%E8%A7%86%E9%A2%91%2F%E7%AC%AC36%E8%AE%B2%20%C2%A0%C2%A0%20%E5%A4%9A%E9%A1%B9%E8%B5%84%E4%BA%A7%E7%9A%84%E7%BB%84%E5%90%88%E3%80%81%E8%B5%84%E6%9C%AC%E5%B8%82%E5%9C%BA%E7%BA%BF.mp4&app_id=250528&clienttype=0&type=M3U8_FLV_264_480&vip=0&adToken=UlWRIsUUtFdAOvXZ8HktPMfn9joa2hS1VzSqsbo6GdiO%2FyIkgi5EnXo84vyxEn2Ur%2B8O49KiY8GaEKHwzyA7Wz0G4jFjjYX9fg7ywkLyXmZU4LxGWA8%2F%2BvbT8iNB1sbP45lTSNaxAmGhFLhdk9wNLZzZAvTs%2BxOzcrOyy70RuPE%3D"
# cookie = "PSTM=1565077563; BIDUPSID=0891F37C2E76F2C004C27154D48C7BD8; pan_login_way=1; BAIDUID=000A294E42D801E8F1D8C7EE7642989A:SL=0:NR=10:FG=1; PANWEB=1; MCITY=-%3A; BAIDUID_BFESS=000A294E42D801E8F1D8C7EE7642989A:SL=0:NR=10:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; __yjs_duid=1_063f543b3f8f5fb2223ffa124f056c971609117862039; delPer=0; PSINO=6; H_PS_PSSID=1449_33225_33306_32974_33286_33351_33313_33312_33311_33310_33309_33308_33307_33389_33372_33370; csrfToken=FIlno1UeBDZnRlED7atDgPnQ; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1608636529,1608637685,1609203364,1609207287; BDUSS=3lIUEg2YXZtYjdWRW9QMnJZU21BeGR6em5Od3laZzhpM0w5N1g2WjdRSlNHeEpnSVFBQUFBJCQAAAAAAQAAAAEAAACO1b4vva3Ez9Chs8cwNTE1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFKO6l9SjupfZ; BDUSS_BFESS=3lIUEg2YXZtYjdWRW9QMnJZU21BeGR6em5Od3laZzhpM0w5N1g2WjdRSlNHeEpnSVFBQUFBJCQAAAAAAQAAAAEAAACO1b4vva3Ez9Chs8cwNTE1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFKO6l9SjupfZ; SCRC=cb2660f8b2eb14705f0bdf421179a346; STOKEN=6ab305af548b93681ac02324354ab9da932df08562b7e8bce2570abcecf05d34; BDCLND=Y8gUtVPquPHVWrNCBxUFpEdxTSftRB85vHvW68nkIos%3D; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1609208260; PANPSC=11043555505473275570%3AKkwrx6t0uHCtza0ZY%2Fm4hBUdqzE5qOrzN7dOlg4IbW2z9Le326YitQPZN16gvceAVaSXcDBdXtjPzW21GgvS0EpDgNqxv39mVgbdZf2zwPuyyezoC8D9eCHshfz3IZqPyIUHUDWcQM3ibxER0vwJhdHhJ5aZPptoX0r3JWTW68DiLaLUl0KD5CiPeEEq9nKY%2BBPsSDpTJNs%3D"
# m3u8_down(url= url,cookie=cookie)
# parse_url_list()
# url = "https://v1.baidupcs.com/video/netdisk-videotran-xian/316502d8efa87d6c87a7d6ddfeec1119_8242_1_ts/2a6901d147590edb4683ab4763301c08?ts_size=8187811&app_id=250528&csl=130&dp-logid=8433990713488795238&fn=%E7%AC%AC36%E8%AE%B2+%C2%A0%C2%A0+%E5%A4%9A%E9%A1%B9%E8%B5%84%E4%BA%A7%E7%9A%84%E7%BB%84%E5%90%88%E3%80%81%E8%B5%84%E6%9C%AC%E5%B8%82%E5%9C%BA%E7%BA%BF.mp4&fsid=3917982770924&iv=0&logid=8433990713488795238&ouk=1103088042081&r=405443569&size=362196489&sta_cs=26062&sta_dt=video&sta_dx=345&time=1609255863&to=hs01&tot=cmZQ6&uo=ct&uva=1239406004&vuk=1103088042081&backhost=%5B%22qdct01.baidupcs.com%22%2C%22yqct07.baidupcs.com%22%2C%22xact07.baidupcs.com%22%2C%22testpoms.baidupcs.com%22%5D&etag=2a6901d147590edb4683ab4763301c08&fid=0b0d3e83911ae7db6b764ddca166913f-1103088042081&len=337174&path=%2F02-%E5%9F%BA%E7%A1%80%E7%8F%AD-%E9%83%91%E6%99%93%E5%8D%9A%EF%BC%88%E6%9B%B4%E6%96%B0%E8%87%B3104%E8%AE%B2%EF%BC%89%2F%E8%A7%86%E9%A2%91%2F%E7%AC%AC36%E8%AE%B2+%C2%A0%C2%A0+%E5%A4%9A%E9%A1%B9%E8%B5%84%E4%BA%A7%E7%9A%84%E7%BB%84%E5%90%88%E3%80%81%E8%B5%84%E6%9C%AC%E5%B8%82%E5%9C%BA%E7%BA%BF.mp4&range=0-337173&region=xian&resv4=&sign=BOUTHNF-F3530edecde9cd71b79378b290804a96-r%252Fwvrwdxhgu924t%252FNJYyYNBN6aE%253D&xcode=ec5e2107922a937041365bbdb73f0284b3ce9cd03f99158e06c7e7a8e03db97dad65723da38f81552e0077e2b419f2529a7e3ac4ae9d7ad8&xv=6&need_suf=&pmk=14002a6901d147590edb4683ab4763301c0821a07a940000007cefa3&by=my-streaming"
# v_down('https://v1.baidupcs.com/video/netdisk-videotran-xian/316502d8efa87d6c87a7d6ddfeec1119_8242_1_ts/2a6901d147590edb4683ab4763301c08?ts_size=8187811&app_id=250528&csl=130&dp-logid=8434463528979835598&fn=%E7%AC%AC36%E8%AE%B2+%C2%A0%C2%A0+%E5%A4%9A%E9%A1%B9%E8%B5%84%E4%BA%A7%E7%9A%84%E7%BB%84%E5%90%88%E3%80%81%E8%B5%84%E6%9C%AC%E5%B8%82%E5%9C%BA%E7%BA%BF.mp4&fsid=3917982770924&iv=0&logid=8434463528979835598&ouk=1103088042081&r=389260644&size=362196489&sta_cs=26074&sta_dt=video&sta_dx=345&time=1609257625&to=hs01&tot=c1wgi&uo=ct&uva=1239406004&vuk=1103088042081&etag=2a6901d147590edb4683ab4763301c08&fid=0b0d3e83911ae7db6b764ddca166913f-1103088042081&len=316740&range=337174-653913&region=xian&resv4=&sign=BOUTHNF-F3530edecde9cd71b79378b290804a96-JNvrJ5bcQCUjl%252F54cWxJ3niiblE%253D&xcode=b277657af7923fd36a5e2a8b21b61f05b3ce9cd03f99158eab42da8a938de4e3db8e144410b99cad2e0077e2b419f2529a7e3ac4ae9d7ad8&xv=6&need_suf=&pmk=14002a6901d147590edb4683ab4763301c0821a07a940000007cefa3&by=my-streaming')
# write_file_list('ffmpeg_test')
# print(remove("第36讲  多项资产的组合、资本市场线.mp4"))

#python D:\pythonWorkspace\pydemo\baidu_down\baidu_v_resource_down.py -u "https://pan.baidu.com/api/streaming?path=%2F02-%E5%9F%BA%E7%A1%80%E7%8F%AD-%E9%83%91%E6%99%93%E5%8D%9A%EF%BC%88%E6%9B%B4%E6%96%B0%E8%87%B3104%E8%AE%B2%EF%BC%89%2F%E8%A7%86%E9%A2%91%2F%E7%AC%AC03%E8%AE%B2%20%C2%A0%C2%A0%20%E5%A7%94%E6%89%98%E4%BB%A3%E7%90%86%E7%90%86%E8%AE%BA%E3%80%81%E5%88%A9%E7%9B%8A%E7%9B%B8%E5%85%B3%E8%80%85%E7%90%86%E8%AE%BA.mp4&app_id=250528&clienttype=0&type=M3U8_FLV_264_480&vip=0&adToken=1Z7hbrnIyGP9efzcOGCVutm8zxLHPmC%2FiP5BVVv%2F4qs3gJbzYA3LCxyyqcnkEI8qzmo5slbazOSonm5cWtYCEDd%2FBUR0O4sSCZiCdyo5KQFV1gKtpynDLfoFpeNbMdMoTLSm0B6YA3pertrG02AESarWoOaB1r8TO5evoVIoiD0%3D" -c "BIDUPSID=2B4481A90B7308A21559A72D30BA6A82; PSTM=1605936976; BAIDUID=2B4481A90B7308A2CC7B927FE4FAC444:FG=1; BAIDUID_BFESS=2B4481A90B7308A2CC7B927FE4FAC444:FG=1; BDUSS=JzdXdKQzdLLTFOV2VUQmJ-fmlLMFZFdVQ4bU9UNkoybn5MSFZMYkRscll0UkpnSVFBQUFBJCQAAAAAAQAAAAEAAACO1b4vva3Ez9Chs8cwNTE1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANgo61~YKOtfQj; BDUSS_BFESS=JzdXdKQzdLLTFOV2VUQmJ-fmlLMFZFdVQ4bU9UNkoybn5MSFZMYkRscll0UkpnSVFBQUFBJCQAAAAAAQAAAAEAAACO1b4vva3Ez9Chs8cwNTE1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANgo61~YKOtfQj; pan_login_way=1; csrfToken=mXW2WA8rBR4u0sFb73n0mfjx; STOKEN=c3b200fdbd7843c8da4cae179d58074e4ed7d2f4c9c9102584f3d65eb2cc3449; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1609246903; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1609246923; PANPSC=10368664029439535906%3AKkwrx6t0uHCtza0ZY%2Fm4hBUdqzE5qOrzN7dOlg4IbW2z9Le326YitQPZN16gvceAVaSXcDBdXtjPzW21GgvS0EpDgNqxv39mZSclIEThWpmyyezoC8D9eCHshfz3IZqPyIUHUDWcQM3ibxER0vwJhdHhJ5aZPptoX0r3JWTW68DiLaLUl0KD5CiPeEEq9nKY%2BBPsSDpTJNs%3D"


