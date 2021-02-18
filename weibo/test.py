import re

import copy
def test(input_str):
    # 元音开头
    str_list = input_str.split(" ")
    return_str_1 = ""
    return_str_2 = ""
    replace_list1 = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y",
                     "Z"]
    replace_list2 = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y",
                     "z"]
    replace_list3 = ["Bub", "Cash", "Dud", "Fud", "Gug", "Hash", "Jay", "Kuck", "Lul", "Mum", "Nun", "Pub", "Quack",
                     "Rug", "Sus", "Tut", "Vuv", "Wack", "Ex", "Yub",
                     "Zub"]
    for data in str_list:

        if data.startswith("a") or \
                data.startswith("e") or \
                data.startswith("i") or \
                data.startswith("o") or \
                data.startswith("u"):
            data = data + "key"
        else:
            result = re.match("[0-9]*", data)
            # 字母开头
            if len(result.group()) < 1:
                # 辅音开头
                for s in data:
                    if not data.startswith("a") and \
                            not data.startswith("e") and \
                            not data.startswith("i") and \
                            not data.startswith("o") and \
                            not data.startswith("u"):
                        data = data[1:] + data[0:1]
                data = data + "ey"
        return_str_1 = return_str_1 + data + " "

    for replace_str in input_str:
        b = copy.deepcopy(replace_str)
        array = []
        for c in b:
            array.append(str(c))
        for index, r in enumerate(replace_list1):
            if b.find(str(replace_list1[index])) >= 0:
                find_index = b.find(str(replace_list1[index]))
                array[find_index] = array[find_index].replace(replace_list1[index], replace_list3[index])
                continue
            if b.find(str(replace_list2[index])) >= 0:
                find_index_low = b.find(str(replace_list2[index]))
                array[find_index_low] = array[find_index_low].replace(replace_list2[index], replace_list3[index])
                continue
        return_str_2 = return_str_2 + ''.join(array)
    return_str_1 = return_str_1[:-1]
    # print(return_str_1)
    # print(return_str_2)


    return return_str_1,return_str_2


if __name__ == '__main__':
    inputStr = "apple is a fruit"
    test_str_1,test_str_2 = test(inputStr)
    print("Enter input string:{inputStr}".format(inputStr = inputStr))
    print("('{str1}', '{str2}')".format(str1=test_str_1, str2=test_str_2))

    inputStr = "Purple is a fruit"
    test_str_1,test_str_2 = test(inputStr)
    print("Enter input string:{inputStr}".format(inputStr=inputStr))
    print("('{str1}', '{str2}')".format(str1=test_str_1, str2=test_str_2))

    inputStr = "2 is greater than 1"
    test_str_1,test_str_2 = test(inputStr)
    print("Enter input string:{inputStr}".format(inputStr=inputStr))
    print("('{str1}', '{str2}')".format(str1=test_str_1, str2=test_str_2))

    inputStr = "xyz"
    test_str_1,test_str_2 = test(inputStr)
    print("Enter input string:{inputStr}".format(inputStr=inputStr))
    print("('{str1}', '{str2}')".format(str1=test_str_1, str2=test_str_2))

    inputStr = "123abc"
    test_str_1,test_str_2 = test(inputStr)
    print("Enter input string:{inputStr}".format(inputStr=inputStr))
    print("('{str1}', '{str2}')".format(str1=test_str_1, str2=test_str_2))

    inputStr = "???what"
    test_str_1,test_str_2 = test(inputStr)
    print("Enter input string:{inputStr}".format(inputStr=inputStr))
    print("('{str1}', '{str2}')".format(str1=test_str_1, str2=test_str_2))

    inputStr = "123abc"
    test_str_1, test_str_2 = test(inputStr)
    print("Enter input string:{inputStr}".format(inputStr=inputStr))
    print("('{str1}', '{str2}')".format(str1=test_str_1, str2=test_str_2))

