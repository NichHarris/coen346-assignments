# COEN 346 - Lab Assignment #1
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Merge-sort using multithreading

import threading

# mergesort function which utilizes threading
def mergesort(arr: list):
    return None

if __name__ == '__main__':
    # open input.txt and read the lines
    file = open('input.txt', mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()

    # create a list of integers
    values = list()
    for i in range(len(lines)):
        values.append(int(lines[i].strip('\n')))

    # create a thread for the mergesort function
    thread = threading.Thread(target=mergesort)
    thread.join()
