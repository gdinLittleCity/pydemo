
def rangeFunction():
    print("rangeFunction run........")
    arr = []
    arr.append(2)
    for i in range(3, 100, 2):
        for j in range(3, i, 2):
            if i % j == 0:
                break
        else:
            arr.append(i)
    sum = 0
    for arrIndex in range(0, len(arr)):
        sum = sum + arr[arrIndex]

    print("所有质数:", arr)
    print("质数个数:", len(arr))
    print("质数和:", sum)

def selectFunction():
    total = 100
    prime = []
    # 初始化筛选结果数组, 0-素数, 1-合数
    selectResult = [0 for _ in range(total)]

    for i in range(2, total):
        if selectResult[i] == 0:
            prime.append(i)
            for j in range(2 * i, total, i):
                selectResult[j] = 1

    # sum = 0
    # for i in range(0, len(prime)):
    #     sum += prime[i]

    print("所有质数:", prime)
    print("质数个数:", len(prime))
    print("质数和:", sum(prime))


rangeFunction()
selectFunction()









