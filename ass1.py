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
    with open('input.txt', 'r') as file:
        lines = file.readlines()
    file.close()

    # create a list of integers
    values = []
    for i in range(len(lines)):
        values.append(int(lines[i].strip('\n')))
    # create a thread for the mergesort function
    thread = threading.Thread(target=mergesort(values))
    thread.start()
    thread.join()