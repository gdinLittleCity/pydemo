# encoding=utf-8
import os


def file_sub(dir:str):

    mb = (1024 - 10) * 1024
    for root,dirs, files in os.walk(dir):
        for name in files:
            file_size = os.path.getsize(os.path.join(root, name))
            path = str(os.path.join(root, name)).split(".").__getitem__(0)
            if file_size > mb:
                with open(path + ".txt", 'r', encoding="utf-8") as fr:
                    seq = 0
                    new_path = path+"-"+str(seq)+".txt"
                    for text in fr.readlines():
                        if text.split():
                            fd = open(new_path, 'a', encoding="utf-8")
                            new_file_size = os.path.getsize(new_path)
                            if new_file_size < mb:
                                fd.write(text)
                            else:
                                seq = seq + 1
                                new_path = path+"-"+str(seq)+".txt"
                                fd = open(new_path, 'w', encoding="utf-8")
                                fd.write(text)



if __name__ == '__main__':

    file_sub('C:\\MyJavaWorkspace\\pydemo\\weibo\\0218')
