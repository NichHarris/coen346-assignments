# COEN 346 - Lab Assignment #1
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Merge-sort using multithreading

import threading
from concurrent.futures import ThreadPoolExecutor

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


def merge_sort(arr: list, futures, output):
    if len(arr) <= 1:
        return arr
    else:
        with ThreadPoolExecutor as executor:  # start multithreading
            mid = len(arr)//2
            left_arr = executor.submit(merge_sort, arr[:mid], futures, output)  # schedules a callable
            futures.append(left_arr)  # add result to list
            right_arr = executor.submit(merge_sort, arr[mid:], futures, output)  # schedules a callable
            futures.append(right_arr)  # add result to list
            return merge(left_arr,right_arr, futures, output)


def threading_output(self, val):
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
    
    # open the output file
    output = open("output.txt", "a")

    futures = []
    merge_sort(values, futures, output)

