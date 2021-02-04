# COEN 346 - Lab Assignment #1
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Merge-sort using multithreading

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import perf_counter

class FileManager:

    def __init__(self):
        # open the output file
        self.output = open("output.txt", "w")
        self.futures = []

    def merge(self, left_arr, right_arr):
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


    def merge_sort(self, arr: list):
        print(threading.active_count())  # keep track of threads
        if len(arr) <= 1:
            return arr
        else:
            with ThreadPoolExecutor(max_workers = 15) as executor:
                mid = len(arr)//2
                left_arr = executor.submit(self.merge_sort, arr[:mid])
                self.futures.append(left_arr)
                right_arr = executor.submit(self.merge_sort, arr[mid:])
                self.futures.append(right_arr)
                #self.output.write("Thread {} started\n".format(threading.current_thread().ident))
                
            left = left_arr.result()
            #self.output.write("Thread {} finished: {}\n".format(threading.current_thread().ident, left))
            right = right_arr.result()
            #self.output.write("Thread {} finished: {}\n".format(threading.current_thread().ident, right))
            return self.merge(left, right)

if __name__ == '__main__':
    # open input.txt and read the lines
    with open('input.txt', 'r') as file:
        lines = file.readlines()
    file.close()

    # create a list of integers
    values = []
    for i in range(len(lines)):
        values.append(int(lines[i].strip('\n')))

    result = FileManager().merge_sort(values)
    print(result)
