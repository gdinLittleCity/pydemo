import xlrd
import re
import datetime
import os
from xlrd import xldate_as_datetime, xldate_as_tuple


def handleExcel():
    # 在路径前面加r，即保持字符原始值的意思
    all_file_path = get_dir_file_path(r'C:\Users\yamei\Desktop\原材料\付款')
    print('文件数量:{},所有文件:{}'.format(all_file_path.__len__(), all_file_path))
    index = 0
    all_data = []
    for dir in all_file_path:
        if not dir.endswith('.xlsx'):
            continue
        file_name_arr = dir.split('\\')
        file_name = file_name_arr.__getitem__(file_name_arr.__len__()-1)
        index = index + 1
        # new_dir_str = ''.join(dir.split())
        # proName = new_dir_str[0:new_dir_str.index('V')]
        # proType = new_dir_str[new_dir_str.index('V'): new_dir_str.index('V') + 4]
        # proNum = new_dir_str[new_dir_str.index('V') + 4: new_dir_str.index('K')]
        # child = os.path.join('%s/%s' % (excel_path, dir))
        path_split = file_name.split('_')
        pro_name = path_split[0]
        pro_type = path_split[1]
        pro_num = path_split[2]
        print('the file index:', index, file_name)
        data_list = handleDate(dir, pro_name, pro_type, pro_num)
        all_data.extend(data_list)
    return all_data


def handleDate(path, proName, proType, proNum):
    data_arr = []
    # excel_path = r'C:/Users/yamei/Desktop/原材料/付款/A280/A280 V3.1 30K付款计划20190522.xlsx'
    excel_path = r'' + str(path)
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    print('sheet rows,cols:', rows, cols)
    # for i in range(8, cols)
    # time1 = time_formate(sheet.cell(1, 8))
    # time2 = time_formate(sheet.cell(1, 9))
    # time3 = time_formate(sheet.cell(1, 10))
    # time4 = time_formate(sheet.cell(1, 11))
    # time5 = time_formate(sheet.cell(1, 12))

    # print(time1)
    # print(time2)
    # print(time3)
    # print(time4)
    # print(time5)

    for i in range(1, sheet.nrows - 4):
        data = {}
        data['proName'] = proName
        data['proType'] = proType
        data['proNum'] = proNum
        data['companyName'] = sheet.row_values(i)[1]
        data['calType'] = sheet.row_values(i)[4]
        sub_time = sheet.cell(i, 7)
        if sub_time.ctype == 2 or sub_time.ctype == 3:
            sub_time_value = xldate_as_datetime(sub_time.value, 0).strftime('%Y%m%d')
            data['subTime'] = sub_time_value
        else:
            data['subTime'] = sheet.row_values(i)[7]
        for col in range(8, cols):
            # print('row, cols is:', i, col)
            if sheet.cell(1, col).value == '':
                continue
            time_result = time_formate(sheet.cell(1, col))
            if time_result == None:
                data[sheet.row_values(1)[col]] = sheet.row_values(i)[col]
            else:
                data[time_result] = sheet.row_values(i)[col]

        # data[time1] = sheet.row_values(i)[8]
        # data[time2] = sheet.row_values(i)[9]
        # data[time3] = sheet.row_values(i)[10]
        # data[time4] = sheet.row_values(i)[11]
        # if not time5 == None:
        #     data[time5] = sheet.row_values(i)[12]
        #     data['main'] = sheet.row_values(i)[13]
        # else:
        #     data['main'] = sheet.row_values(i)[12]
        data_arr.append(data)
        print(data)
    print('size:', data_arr.__len__(), data_arr)
    return data_arr


def time_formate(cell_data):
    # data_type = typeof(timeStr)
    if cell_data.ctype == 2 or cell_data.ctype == 3:
        # date = datetime(cell_data)
        cell = xldate_as_datetime(cell_data.value, 0).strftime('%m%d')
        return cell
    timeStr = cell_data.value
    time_arr = re.findall(r'\d{1,2}', timeStr)
    if time_arr.__len__() == 0:
        return None
    time_formate_str = ''
    if int(time_arr[0]) < 10:
        time_formate_str = time_formate_str + '0' + str(time_arr[0])
    else:
        time_formate_str = time_formate_str + str(time_arr[0])

    if int(time_arr[1]) < 10:
        time_formate_str = time_formate_str + '0' + str(time_arr[1])
    else:
        time_formate_str = time_formate_str + str(time_arr[1])

    return time_formate_str


def typeof(variate):
    type = None
    if isinstance(variate, int):
        type = "int"
    elif isinstance(variate, str):
        type = "str"
    elif isinstance(variate, float):
        type = "float"
    elif isinstance(variate, list):
        type = "list"
    elif isinstance(variate, tuple):
        type = "tuple"
    elif isinstance(variate, dict):
        type = "dict"
    elif isinstance(variate, set):
        type = "set"
    return type


def get_dir_file_path(dir_path):
    if dir_path == None or dir_path == '':
        return []
    file_path_list = []
    if os.path.isdir(dir_path):
        path_list = os.listdir(dir_path)
        for path in path_list:
            # 文件夹 - 递归获取文件
            if os.path.isdir(os.path.join(dir_path, path)):
                file_path_list.extend(get_dir_file_path(os.path.join(dir_path, path)))
            # 文件 - 路径加入结果集
            else:
                file_path_list.append(os.path.join(dir_path, path))
    else:
        file_path_list.append(dir_path)

    return file_path_list

all = handleExcel()
print('数据量:{},所有数据:{}'.format(all.__len__(), all))
