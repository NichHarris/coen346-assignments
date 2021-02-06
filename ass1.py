# COEN 346 - Lab Assignment #1
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Merge-sort using recursive multithreading

# import the necessarily packages
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# FileManager class used to write to output.txt without having to pass it as an argument to merge() and merge_sort()
class FileManager:

    def __init__(self):
        # initialize the output file for writing
        self.output = open("output.txt", "w")

    def merge_sort(self, left_arr, right_arr):
        # keep track of active threads in merge_sort()
        # print("in merge_sort: {}".format(threading.active_count()))

        # pointers for traversing the two sublists (left_arr and right_arr)
        left = right = 0
        # list to store sorted result
        result = []
        
        # terminate the active threads and return the resulting sublists
        left_arr = left_arr.result()
        right_arr = right_arr.result()

        # begin merging the two sublists in ascending order using the left and right pointers
        while left < len(left_arr) and right < len(right_arr):
            # if the element in left_arr currently indexed is smaller than that of right_arr,
            # append the element to result and increment the left pointer
            if left_arr[left] <= right_arr[right]:
                result.append(left_arr[left])
                left += 1
            # if the element in right_arr currently indexed is smaller,
            # append the element to result and increment the right pointer
            else:
                result.append(right_arr[right])
                right += 1

        # append the remaining elements in result if they are already ordered
        result += left_arr[left:]
        result += right_arr[right:]

        # write the status of the currently running thread (finished after exiting merge_sort()) to output.txt
        self.output.write("Thread {} finished: {}\n".format(threading.current_thread().ident, result))
        # return the resulting sorted list
        return result

    # recursively divide the list into sublists
    def splitting(self, arr: list):
        # write the status of the currently running thread (started after entering the 
        # splitting function) to output.txt
        self.output.write("Thread {} started\n".format(threading.current_thread().ident))
        # keep track of active threads in splitting()
        # print(threading.active_count())s
        # if the sublist contains more than one element, continue splitting recursively
        if len(arr) > 1:
            # get the mid pointer for splitting lists
            mid = len(arr)//2
            # instantiate a ThreadPoolExecutor to submit threads and terminate threads upon completion
            with ThreadPoolExecutor(max_workers = 15) as executor:
                # execute a thread for both the left and right portion of the split list
                # NOTE: arr[:mid] will only return the sublist from index 0 to mid-1
                left_arr = executor.submit(self.splitting, arr[:mid])
                right_arr = executor.submit(self.splitting, arr[mid:])
            # exit the list to allow result collection and begin merging the sub lists
            return self.merge_sort(left_arr, right_arr)
        # base case for the recursive algorithm
        # return the list containing a single element
        else:
            # write the status of the currently running thread (finished after returning from base case) to output.txt
            self.output.write("Thread {} finished: {}\n".format(threading.current_thread().ident, arr))
            return arr

# main point of script execution
if __name__ == '__main__':

    # open input.txt and read each line
    with open('input.txt', 'r') as file:
        lines = file.readlines()

    # close the file
    file.close()
    # create a list of integers from the lines read
    values = []

    for line in lines:
        values.append(int(line.strip('\n')))

    # sort the list of integers using recursive multithreading
    result = FileManager().splitting(values)
    # print the sorted list to console
    print(result)