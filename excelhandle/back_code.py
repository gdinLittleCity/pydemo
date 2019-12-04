import re
import datetime
import os

def rename_file():
    # 查找文件
    path = r"C:\Users\yamei\Desktop\原材料\付款"
    # os.listdir()方法，列出来所有文件
    # 返回path指定的文件夹包含的文件或文件夹的名字的列表
    files = os.listdir(path)
    # 主逻辑
    # 对于批量的操作，使用FOR循环
    # 调试代码的方法：关键地方打上print语句，判断这一步是不是执行成功
    for f in files:
        print(f)
        # 找到老的文件所在的位置
        old_file = os.path.join(path, f)
        if os.path.isdir(old_file):
            old_files = os.listdir(old_file)
            for file in old_files:
                old_file_path = os.path.join(path, old_file, file)
                print("old_file is {}".format(old_file_path))
        # 指定新文件的位置，如果没有使用这个方法，则新文件名生成在本项目的目录中
        # new_file_name = f.replace(' ', '_')
        # new_file = os.path.join(path, new_file_name)
        # print("File will be renamed as:{}".format(new_file))
        # os.rename(old_file, new_file)
        # print("修改后的文件名是:{}".format(f))