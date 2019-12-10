import xlrd
import re
import datetime
import os
from xlrd import xldate_as_datetime, xldate_as_tuple
from xlrd import sheet
import pandas as pd


def is_number(n):
    is_number = True
    try:
        num = float(n)
        # 检查 "nan"
        is_number = num == num  # 或者使用 `math.isnan(num)`
    except ValueError:
        is_number = False
    return is_number


def time_formate(cell_data: sheet.Cell):
    # 2 number, 3 date
    if cell_data.ctype == 2 or cell_data.ctype == 3:
        cell = xldate_as_datetime(cell_data.value, 0).strftime('%Y%m%d')
        return cell
    time_str = cell_data.value
    time_arr = re.findall(r'\d{1,2}', time_str)
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


def handle_date(path, pro_name, pro_type, pro_num):
    print('解析 excel:{} 开始......'.format(path))
    data_arr = []
    # excel_path = r'C:/Users/yamei/Desktop/原材料/付款/A280/A280 V3.1 30K付款计划20190522.xlsx'
    excel_path = r'' + str(path)
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    print('sheet rows,cols:', rows, cols)

    for i in range(2, sheet.nrows):
        first_cell = sheet.cell(i, 0)
        # 第一行非数字,则说明此行数据是不重要的
        if not is_number(first_cell.value) and first_cell.value != '':
            continue
        data = {
            '产品名称': pro_name, '型号': pro_type, '台数': pro_num, '公司名称': '',
            '结算方式': '', '预计交货时间': ''
        }
        data['公司名称'] = sheet.row_values(i-1)[1] if sheet.row_values(i)[1] == '' else sheet.row_values(i)[1]
        data['结算方式'] = sheet.row_values(i)[4]

        sub_time = sheet.cell(i, 7)
        if sub_time.ctype == 2 or sub_time.ctype == 3:
            sub_time_value = xldate_as_datetime(sub_time.value, 0).strftime('%Y-%m-%d')
            data['预计交货时间'] = sub_time_value
        else:
            data['预计交货时间'] = sheet.row_values(i)[7]
        for col in range(8, cols):
            # print('row, cols is:', i, col)
            # 空白列,跳过
            if sheet.cell(1, col).value == '':
                continue
            time_result = time_formate(sheet.cell(1, col))
            if time_result is None:
                # data[sheet.row_values(1)[col]] = sheet.row_values(i)[col]
                # 供应商主营业务,备注列 丢弃
                continue
            else:
                # 时间字符串在4位,6位时间字符串则表示该列的值类型为时间类型
                if col > 8 and time_result.__len__() <= 4:
                    before_time = time_formate(sheet.cell(1, col - 1))
                    # 时间列为递增序列,若果出现后一个时间比前一个时间小,则必然是过了一个年份
                    if not before_time is None and int(before_time) < int(time_result):
                        print(time_result + '转换为: 2019' + time_result)
                        time_result = '2019' + time_result
                    else:
                        if not before_time is None and int(before_time) > int(time_result):
                            print(time_result + '转换为: 2020' + time_result)
                            time_result = '2020' + time_result
                else:
                    # 第一列时间
                    if time_result.__len__() <= 4:
                        print(time_result + '转换为: 2019' + time_result)
                        time_result = '2019' + time_result
                data[time_result] = sheet.row_values(i)[col]
        data_arr.append(data)
        print(data)
    print('size:', data_arr.__len__(), data_arr)
    print('解析 excel:{} 结束......'.format(path))
    return data_arr


def handleExcel(excel_path):
    print('处理excel 数据开始.....................')
    # 在路径前面加r，即保持字符原始值的意思
    all_file_path = get_dir_file_path(excel_path)
    print('文件数量:{},所有文件:{}'.format(all_file_path.__len__(), all_file_path))
    index = 0
    all_data = []
    for file_path in all_file_path:
        print('the file index:', index, file_path)
        if not file_path.endswith('.xlsx'):
            continue
        file_name_arr = file_path.split('\\')
        file_name = file_name_arr.__getitem__(file_name_arr.__len__() - 1)
        index = index + 1
        path_split = file_name.split('_')
        pro_name = path_split[0]
        pro_type = path_split[1]
        pro_num = path_split[2]
        # 解析excel内容
        data_list = handle_date(file_path, pro_name, pro_type, pro_num)
        all_data.extend(data_list)
    return all_data

def sort_data(data_list):
    df = pd.DataFrame(data=data_list)
    # 表头
    header = list(df)
    row_data = df.values.tolist()
    row_data.insert(0, header)
    # 行列转置
    tran_row_col = list(zip(*row_data))
    # 不进行排序的数据
    no_sort_data = tran_row_col[0:5]
    # 进行排序的数据
    sort_data = tran_row_col[6:]

    df_new = pd.DataFrame(data=sort_data)
    col_sort_df = df_new.sort_index(by=[0], ascending=True) # 按第一列的值升序排序

    no_sort_data.extend(col_sort_df.values.tolist())
    df_sort = pd.DataFrame(data=list(zip(*no_sort_data)))
    return df_sort

def count_by_month(data_frame: pd.DataFrame):
    tran_2_row = data_frame.T
    print(tran_2_row.loc[0])
    # print(tran_2_row.head(5))
    return

def write_excel():
    excel_path = r'C:\MyJavaWorkspace\原材料-formate-v2\付款'
    all = handleExcel(excel_path)
    # print('数据量:{},所有数据:{}'.format(all.__len__(), all))
    print('数据量:{}'.format(all.__len__()))
    df_sort = sort_data(all)
    count_by_month(df_sort)
    # path = r'C:\Users\yamei\Desktop\output\付款汇总.xlsx'
    # writer = pd.ExcelWriter(path)
    # df_sort.to_excel(writer,'日统计', index=False)
    # df_sort.to_excel(writer,'月统计', index=False)
    # writer.save()
    print('写入文件 完成.................')




def int_test():
    num = int('0819')
    print(num)


write_excel()
# int_test()
