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

# global dict used to get the name of each event state corresponding to a certain integer
event_dict = {0: "Started", 1: "Resumed", 2: "Paused", 3: "Finished"}

# class used to handle the fair-share process scheduling and write to output.txt
class Scheduler:

    # initialize the output file for writing
    def __init__(self, quant: int):
        self.output = open("output.txt", "w")

# class used to represent processes
class Process:

    # default cosntructor
    def __init__(self, user: str, quant: int, ready_t: int, service_t: int):
        self._user_id = user
        # amount of quantum time allocated to process
        self._quantum = quant
        # time at which the process is ready to be executed
        self._ready_time = ready_t
        # time left until process completes its execution
        self._time_left = service_t
        # type of event state -> 1: started, 2: resumed, 3: paused, 4: finished
        self._state = None
    
    """ Getters """
    @property
    def user_id(self):
        return self._user_id

    @property
    def quantum(self):
        return self._quantum

    @property
    def ready_time(self):
        return self._ready_time

    @property
    def time_left(self):
        return self._time_left

    @property
    def state(self):
        return self._state

    """ Setters """
    @time_left.setter
    def time_left(self, time):
        self._time_left = time

    @state.setter
    def state(self, new_state):
        self._state = new_state

# entrypoint of script execution
if __name__  == '__main__':

    # open input.txt and read file content
    with open('input.txt', 'r') as file:
        lines = file.readlines()

    # get the time quantum of the program
    quant = int(lines.pop(0))

    # dictionary containing the user names and number of processes under each user
    user_dict = {}
    # list containing the ready time for each process
    ready_time = []
    # list containing the service time for each process
    service_time = []

    # store the user name and number of processes as well as each process' ready time and service time in their respective variables
    for line in lines:
        if line[0].isalpha():
            user_dict[line.split(" ")[0]] = int(line.split(" ")[1].rstrip())
        else:
            ready_time.append(int(line.split(" ")[0]))
            service_time.append(int(line.split(" ")[1].rstrip()))

    # close the file
    file.close()

    # list for the allocation of time quantums
    quant_alloc = []

    # find the amount of the time quantum allocated to each process
    num_users = len(user_dict) # number of users
    for key in user_dict:
        num_user_processes = user_dict[key]
        for i in range(0, num_user_processes):
            quant_alloc.append(int(quant//num_users//num_user_processes))

    # array of Process objects to be executed
    processes = []

    # generate a Process object and add it to the list of processes
    counter = 0  # counter used to traverse each previously generated list for process specifications
    for user in user_dict:
        for i in range(0, user_dict[user]):
            processes.append(Process(user,quant_alloc[counter],ready_time[counter],service_time[counter]))
            counter += 1
