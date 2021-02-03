# COEN 346 - Lab Assignment #1
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Merge-sort using multithreading

import threading
import logging
import time

# mergesort function which utilizes threading

def merge(left_arr, right_arr):
    left = right = 0
    result = []

    while left < len(left_arr) and right < len(right_arr):
        if left_arr[left] <= right_arr[right]:
            result.append(left_arr[left])
            left += 1
        else:
            result.append(right_arr[right])
            right += 1
    result += left_arr[left:]
    result += right_arr[right:]
    return result


def merge_sort(arr: list):
    if len(arr) <= 1:
        return arr
    else:
        mid = len(arr)//2
        left_arr, right_arr = merge_sort(arr[:mid]), merge_sort(arr[mid:])
        return merge(left_arr,right_arr)

class myThread(threading.Thread):
    def __init__(self, threadBin, val, count):
        threading.Thread.__init__(self)
        self.threadBin = threadBin
        self.val = val
        self.count = count

    def run(self):
        print("Thread {} started".format(self.threadBin))
        time.sleep(2)
        print("Thread {} finished: {}".format(self.threadBin, self.val))



def threading_output(val):
    print("Thread {} started".format(threading.current_thread().ident))
    print("Thread {} finished: {}".format(threading.current_thread().ident, val))

if __name__ == '__main__':
    # open input.txt and read the lines
    with open('input.txt', 'r') as file:
        lines = file.readlines()
    file.close()

    # create a list of integers
    values = []
    for i in range(len(lines)):
        values.append(int(lines[i].strip('\n')))

    # print(merge_sort(values))
    # create a thread for the mergesort function
    thread = threading.Thread(merge_sort, values)
    thread.start()
    thread.join()
    print(values)