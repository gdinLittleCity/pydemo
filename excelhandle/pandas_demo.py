import pandas as pd
import numpy as np
import os


def handleExcel():
    # 在路径前面加r，即保持字符原始值的意思
    excel_path = r'C:/Users/yamei/Desktop/原材料/付款/A280'
    pathDir = os.listdir(excel_path)
    index = 0
    for dir in pathDir:
        if not dir.endswith('.xlsx'):
            continue

        data_dict = {}
        new_dir_str = ''.join(dir.split())
        data_dict['proName'] = new_dir_str[0:new_dir_str.index('V')]
        data_dict['proType'] = new_dir_str[new_dir_str.index('V'): new_dir_str.index('V') + 4]
        data_dict['proNum'] = new_dir_str[new_dir_str.index('V') + 4: new_dir_str.index('K')]
        print('data dict :', data_dict)
        child = os.path.join('%s/%s' % (excel_path, dir))
        print('the file index:', index, child)

        # out_data = pd.DataFrame.from_dict({
        #     'total': df['供货总额']
        # })
        # print(out_data)
        # out_file_path = str('out/out' + str(index) + '.xlsx')
        # f = open(out_file_path, 'w')
        # f.close()
        # out_data.to_excel(out_file_path, index=False)
        index = index + 1

    return 0


def parseExcel(path):
    data_object = {}
    data_object['companyName'] = []
    data_object['calType'] = []
    data_object['time'] = []
    df = pd.read_excel(path)
    row_datas = df.get_values()
    # new_df = pd.DataFrame(row_datas)
    row_datas = df.values
    headerArr = row_datas[0]
    # data_object['companyName'].append(headerArr[1])
    # data_object['calType'].append(headerArr[2])
    # data_object['time'].append(headerArr[6])
    for j in range(7, headerArr.size - 1):
        data_object[headerArr] = []
    for i in range(1, row_datas.size):
        row = row_datas[i]
        data_object['companyName'].append(row[1])
        data_object['calType'].append(row[2])
        data_object['time'].append(row[6])
        for j in range(7, row.size-1):
            data_object
    # print(new_df.iloc[2:, :])
    return 1


# handleExcel()
parseExcel(r'C:/Users/yamei/Desktop/原材料/付款/A280/A280 V3.1 30K付款计划20190522.xlsx')
