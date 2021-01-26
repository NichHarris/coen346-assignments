# COEN 346 - Lab Assignment #1
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Merge-sort using multithreading

import threading

# mergesort function which utilizes threading

def merge(leftArr, rightArr):
    left = right = 0
    result = []

    while left < len(leftArr) and right < len(rightArr):
        if leftArr[left] <= rightArr[right]:
            result.append(leftArr[left])
            left += 1
        else:
            result.append(rightArr[right])
            right += 1
    result += leftArr[left:]
    result += rightArr[right:]
    return result


def mergesort(arr: list):
    if len(arr) <= 1:
        return arr
    else:
        mid = len(arr)//2
        left, right = mergesort(arr[:mid]), mergesort(arr[mid:])
        return merge(left,right)

if __name__ == '__main__':
    # open input.txt and read the lines
    with open('input.txt', 'r') as file:
        lines = file.readlines()
    file.close()

    # create a list of integers
    values = []
    for i in range(len(lines)):
        values.append(int(lines[i].strip('\n')))

    print(mergesort(values))
    # create a thread for the mergesort function
    # thread = threading.Thread(target=mergesort(values))
    # thread.start()
    # thread.join()