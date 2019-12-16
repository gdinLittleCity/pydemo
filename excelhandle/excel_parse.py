import xlrd
import re
import datetime
import calendar
import os
from xlrd import xldate_as_datetime, xldate_as_tuple
from xlrd import sheet
import pandas as pd

pro_name = '产品名称'
pro_type = '型号'
pro_num = '台数'
pro_com_name = '公司名称'
pro_cal_type = '结算方式'
pro_gain_time = '预计交货时间'

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

def move_col(df: pd.DataFrame, col_name: str, position: int):
    col_ser = df.pop(col_name)
    df.insert(position, col_name, col_ser)

def sort_data_by_index(data_list):
    df = pd.DataFrame(data=data_list)
    col_sort_df = df.sort_index(ascending=True, axis=1)
    # pro_name = '产品名称'
    # pro_type = '型号'
    # pro_num = '台数'
    # pro_com_name = '公司名称'
    # pro_cal_type = '结算方式'
    move_col(col_sort_df, pro_name, 0)
    move_col(col_sort_df, pro_type, 1)
    move_col(col_sort_df, pro_num, 2)
    move_col(col_sort_df, pro_com_name, 3)
    move_col(col_sort_df, pro_cal_type, 4)
    move_col(col_sort_df, pro_gain_time, 5)
    return col_sort_df

def sort_data(data_list):
    df = pd.DataFrame(data=data_list)
    # col_sort_df = df.sort_index(ascending=True, axis=1)
    # pro_name = '产品名称'
    # pro_type = '型号'
    # pro_num = '台数'
    # pro_com_name = '公司名称'
    # pro_cal_type = '结算方式'
    # move_col(df, pro_name, 0)
    # move_col(df, pro_type, 1)
    # move_col(df, pro_num, 2)
    # move_col(df, pro_com_name, 3)
    # move_col(df, pro_cal_type, 4)
    # return col_sort_df
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

def get_month_first_day_and_last_day(year = None, month = None):
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year
    if month:
        month = int(month)
    else:
        month = datetime.date.today().month
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)
    fist_day = datetime.date(year=year, month = month, day=1).strftime('%Y%m%d')
    last_day = datetime.date(year, month, monthRange).strftime('%Y%m%d')
    return fist_day,last_day
def col_sum(x):
    num_array =  x.array
    sum_result = 0
    for num in num_array:
        if not num:
            num = 0
        sum_result = float(num) + sum_result
    return sum_result

def count_by_month(data_frame: pd.DataFrame):
    count_row = []
    column_name = pd.Series(data_frame.values.tolist()[0])
    data_frame.columns = column_name # 重命名列索引
    tran_2_row = data_frame.T
    # print(list(data_frame))
    tran_2_row.columns = pd.Series(tran_2_row.values.tolist()[0]) # 重命名 列索引
    # print(list(tran_2_row.columns))
    count_row.extend(tran_2_row.iloc[0:5,:].values.tolist())
    time_data = tran_2_row.iloc[5:,:]
    time_data.fillna(0, inplace=True)
    print(time_data)
    for t_year in range(2019, 2021):
        print('year:{}'.format(t_year))
        for t_moth in range(1, 13):
            s_date,e_date = get_month_first_day_and_last_day(year=t_year, month= t_moth)
            df = time_data[(time_data['产品名称'] >= s_date) & (time_data['产品名称'] <= e_date)]
            if df.shape[0] <= 0:
                continue
            cal_df = df.iloc[:, 1:]

            t_moth_str = str(t_moth) if  t_moth >= 10 else '0' + str(t_moth)
            year_month = str(t_year) + t_moth_str
            cal_df.loc[year_month] = cal_df.apply(col_sum)
            count_result = cal_df.values.tolist()[cal_df.shape[0] - 1]
            count_result.insert(0, year_month)
            count_row.append(count_result)

    print(count_row)
    write_df = pd.DataFrame(count_row)
    # write_df.T.to_excel(r'C:\Users\yamei\Desktop\output\付款汇总_1.xlsx', index=None, columns=None)
    return write_df.T

def filter_fun(time_list: list, s_date: str, e_date: str):
    return [x for x in time_list if s_date <= x and x <= e_date]

def count_by_month_NO_T(data_frame: pd.DataFrame):
    # 获取列索引
    col_index_list = list(data_frame)
    no_change_col_index = [pro_name,pro_type, pro_num, pro_com_name, pro_cal_type, pro_gain_time]
    month_df = data_frame[no_change_col_index]

    for t_year in range(2019, 2021):
        print('{}年开始月统计数据'.format(t_year))
        for t_moth in range(1, 13):
            s_date, e_date = get_month_first_day_and_last_day(year=t_year, month=t_moth)
            time_list = filter_fun(col_index_list,s_date, e_date)
            df = data_frame[time_list]
            # df的列数<=0 说明没有数据, 通过列索引获取到的df会有行索引,行数不变;如果列索引不存在,返回的df有行索引,没有列索引
            if df.shape[1] <= 0:
                continue
            df.fillna(0, inplace=True)
            t_moth_str = str(t_moth) if t_moth >= 10 else '0' + str(t_moth)
            year_month = str(t_year) + t_moth_str
            month_df[year_month] = df.apply(col_sum,axis=1)
            # print(month_df[year_month])
        print('{}年结束月统计数据,统计结果的列索引:{}'.format(t_year, list(month_df)))
    return month_df


def write_excel():
    excel_path = os.path.join(os.getcwd(), 'excel')
    all = handleExcel(excel_path)
    # print('数据量:{},所有数据:{}'.format(all.__len__(), all))
    print('数据量:{}'.format(all.__len__()))
    df_sort = sort_data_by_index(all)
    df_sort_count = count_by_month_NO_T(df_sort)
    # path = r'C:\Users\yamei\Desktop\output\付款汇总.xlsx'
    path = os.path.join(os.getcwd(), 'out/付款汇总.xlsx')
    writer = pd.ExcelWriter(path)
    df_sort.to_excel(writer,'日统计', index=False)
    df_sort_count.to_excel(writer,'月统计', index=False)
    writer.save()
    print('写入文件 完成.................')




def int_test():
    num = int('0819')
    print( os.path.join(os.getcwd(), 'out/付款汇总.xlsx'))


write_excel()
# int_test()
