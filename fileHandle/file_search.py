import os
import shutil


def get_dir_file_path(dir_path):
    if dir_path is None or dir_path == '':
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


def main():
    file_path = input("请输入目录路径:")
    file_name = input("文件名关键字:")
    des_path = input("复制的目标目录:")

    all_file_path = get_dir_file_path(file_path)
    all_data = []
    for path in all_file_path:
        if path.find(file_name) != -1 :
            all_data.append(path)
    print("查找到的文件:", all_data)
    for file in all_data:
        shutil.copy(file, des_path)
main()


