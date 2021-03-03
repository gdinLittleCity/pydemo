# -*-coding:utf-8-*-
import csv
import json
import sys
import codecs


def trans(path):
    json_data = codecs.open(path + '.txt', 'r', encoding='utf-8')
    csv_file = open(path + '.csv', 'w', encoding='utf-8', newline='')  # python3下
    writer = csv.writer(csv_file, delimiter='\t', quoting=csv.QUOTE_ALL)
    flag = True
    for line in json_data:
        if len(line) == 0:
            continue
        dic = json.loads(line)
        if flag:
            # 获取属性列表
            keys = list(dic.keys())
            print(keys)
            writer.writerow(keys)  # 将属性列表写入csv中
            flag = False

        # 读取json数据的每一行，将values数据一次一行的写入csv中
        writer.writerow(list(dic.values()))
    json_data.close()
    csv_file.close()


if __name__ == '__main__':
    path = 'weibo-冬奥会-资生堂中国杯花样滑冰大奖赛'  # 获取path参数
    trans(path)