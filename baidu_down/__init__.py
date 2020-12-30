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

def content_test():
    content = ["https://v1.baidupcs.com/video/netdisk-videotran-xian/dc9ec6452f672632d5a554c43b11b14b_1074_1_ts/d01d0aa000a14db5c0a3cefb0e378755?ts_size=10913400&app_id=250528&csl=130&dp-logid=8458508279032417200&fn=%E7%AC%AC51%E8%AE%B2+%C2%A0%C2%A0+%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE%E7%8E%B0%E9%87%91%E6%B5%81%E5%88%86%E6%9E%90%EF%BC%883%EF%BC%89%E3%80%81%E6%9B%B4%E6%96%B0%E6%94%B9%E9%80%A0%E9%A1%B9%E7%9B%AE%EF%BC%881%EF%BC%89.mp4&fsid=753924998464901&iv=0&logid=8458508279032417200&ouk=1103088042081&r=255432036&size=264684330&sta_cs=19377&sta_dt=video&sta_dx=252&time=1609347198&to=hs01&tot=bxkWj&uo=ct&uva=1239406004&vuk=1103088042081&backhost=%5B%22qdct01.baidupcs.com%22%2C%22yqct07.baidupcs.com%22%2C%22xact07.baidupcs.com%22%2C%22testpoms.baidupcs.com%22%5D&etag=d01d0aa000a14db5c0a3cefb0e378755&fid=cb8a7ef5303c438e74713fa0a68fd1e5-1103088042081&len=398184&path=%2F02-%E5%9F%BA%E7%A1%80%E7%8F%AD-%E9%83%91%E6%99%93%E5%8D%9A%EF%BC%88%E6%9B%B4%E6%96%B0%E8%87%B3104%E8%AE%B2%EF%BC%89%2F%E8%A7%86%E9%A2%91%2F%E7%AC%AC51%E8%AE%B2+%C2%A0%C2%A0+%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE%E7%8E%B0%E9%87%91%E6%B5%81%E5%88%86%E6%9E%90%EF%BC%883%EF%BC%89%E3%80%81%E6%9B%B4%E6%96%B0%E6%94%B9%E9%80%A0%E9%A1%B9%E7%9B%AE%EF%BC%881%EF%BC%89.mp4&range=0-398183&region=xian&resv4=&sign=BOUTHNF-F3530edecde9cd71b79378b290804a96-sb4Oym9AqHzBXnu%252FRJsYFuh%252FucE%253D&xcode=ac27e10d79a8c410fd4c6d0da479c51baa9c547be9f684c1fda6a0d02c361fbd481ab301d6ac78132e0077e2b419f2529a7e3ac4ae9d7ad8&xv=6&need_suf=&pmk=1400d01d0aa000a14db5c0a3cefb0e37875550433df3000000a68678&by=my-streaming","56"]
    count = content.count("https://v1.baidupcs.com/video/netdisk-videotran-xian/dc9ec6452f672632d5a554c43b11b14b_1074_1_ts/d01d0aa000a14db5c0a3cefb0e378755?ts_size=10913400&app_id=250528&csl=130&dp-logid=8458508279032417200&fn=%E7%AC%AC51%E8%AE%B2+%C2%A0%C2%A0+%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE%E7%8E%B0%E9%87%91%E6%B5%81%E5%88%86%E6%9E%90%EF%BC%883%EF%BC%89%E3%80%81%E6%9B%B4%E6%96%B0%E6%94%B9%E9%80%A0%E9%A1%B9%E7%9B%AE%EF%BC%881%EF%BC%89.mp4&fsid=753924998464901&iv=0&logid=8458508279032417200&ouk=1103088042081&r=255432036&size=264684330&sta_cs=19377&sta_dt=video&sta_dx=252&time=1609347198&to=hs01&tot=bxkWj&uo=ct&uva=1239406004&vuk=1103088042081&backhost=%5B%22qdct01.baidupcs.com%22%2C%22yqct07.baidupcs.com%22%2C%22xact07.baidupcs.com%22%2C%22testpoms.baidupcs.com%22%5D&etag=d01d0aa000a14db5c0a3cefb0e378755&fid=cb8a7ef5303c438e74713fa0a68fd1e5-1103088042081&len=398184&path=%2F02-%E5%9F%BA%E7%A1%80%E7%8F%AD-%E9%83%91%E6%99%93%E5%8D%9A%EF%BC%88%E6%9B%B4%E6%96%B0%E8%87%B3104%E8%AE%B2%EF%BC%89%2F%E8%A7%86%E9%A2%91%2F%E7%AC%AC51%E8%AE%B2+%C2%A0%C2%A0+%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE%E7%8E%B0%E9%87%91%E6%B5%81%E5%88%86%E6%9E%90%EF%BC%883%EF%BC%89%E3%80%81%E6%9B%B4%E6%96%B0%E6%94%B9%E9%80%A0%E9%A1%B9%E7%9B%AE%EF%BC%881%EF%BC%89.mp4&range=0-398183&region=xian&resv4=&sign=BOUTHNF-F3530edecde9cd71b79378b290804a96-sb4Oym9AqHzBXnu%252FRJsYFuh%252FucE%253D&xcode=ac27e10d79a8c410fd4c6d0da479c51baa9c547be9f684c1fda6a0d02c361fbd481ab301d6ac78132e0077e2b419f2529a7e3ac4ae9d7ad8&xv=6&need_suf=&pmk=1400d01d0aa000a14db5c0a3cefb0e37875550433df3000000a68678&by=my-streaming")
    print("count:{count}".format(count=count))

content_test()