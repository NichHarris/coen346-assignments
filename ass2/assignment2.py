# COEN 346 - Lab Assignment #2
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Fair-share Process Scheduling Simulator

# import the necessary packages
import threading
from concurrent.futures import ThreadPoolExecutor

# class used to handle the fair-share process scheduling and write to output.txt
class Scheduler:

    # initialize the output file for writing
    def __init__(self, quant: int):
        self.quantum = quant
        self.output = open("output.txt", "w")


# entrypoint of script execution
if __name__  == '__main__':

    # open input.txt and read contents
    with open('input.txt', 'r') as file:
        lines = file.readlines()

    # get the time quantum
    quant = int(lines.pop(0))

    # list containing the number of processes for each user
    num_processes = []

    # list containing the ready time for each process
    ready_time = []

    # list containing the service time for each process
    service_time = []

    # get the characteristics of each process for each user
    for line in lines:
        if line[0].isalpha():
            num_processes.append(int(line.split(" ")[1].rstrip()))
        else:
            ready_time.append(int(line.split(" ")[0]))
            service_time.append(int(line.split(" ")[1].rstrip()))

    # close the file
    file.close()

    print(num_processes)
    print(ready_time)
    print(service_time)
