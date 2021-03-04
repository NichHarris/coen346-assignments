# COEN 346 - Lab Assignment #2
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Fair-share Process Scheduling Simulator

# import the necessary packages
import threading
import time


# class used to handle the fair-share process scheduling and write to output.txt
class Scheduler:

    # default constructor
    def __init__(self, processes: list, quantum):
        # initialize the output file for writing
        self._output = open("output.txt", "w")
        # queue of processes which have not yet reached their ready time
        # enqueue: .append(), dequeue: .pop(0)
        self._new_processes = processes
        # queue of processes ready to be executed
        # enqueue: .append(), dequeue: .pop(0)
        self._ready_queue = []
        # holds the elapsed time of the program
        self._total_elapsed_time = time.perf_counter()
        # holds (key) current active user(s) and (value) the number of active process(es) of the user(s)
        self.users_dict = {}
        # holds quantum value
        self.quantum = quantum

        # check if a new process needs to be added to ready queue and/or execute a process in the ready queue
        while len(self._new_processes) or len(self._ready_queue):
            # update the elapsed time
            self._total_elapsed_time = time.perf_counter()
            # check if a new process is ready to be executed
            self.verify_if_ready()
            print(int(self._total_elapsed_time))
            # while there are processes waiting in the ready queue, dequeue a process and execute it using a single thread
            if len(self._ready_queue) != 0:
                t = threading.Thread(target=self.execute, args=(self._ready_queue.pop(0),))
                t.start()
                t.join()
                print("thread completed")

    # add a process to the ready queue if its ready to run
    def verify_if_ready(self):
        if len(self._new_processes) != 0:
            for process in self._new_processes:
                if process.ready_time <= int(self._total_elapsed_time):

                    # adds a new user to dict, and increments existing users with a new process
                    key = process.user_id
                    if key in self.users_dict.keys():
                        self.users_dict[key] += 1
                    else:
                        self.users_dict[key] = 1

                    self._ready_queue.append(process)
                    self._new_processes.pop(0)

            self.quantum_alloc()

        # if self._new_processes[i].ready_time <= int(self._total_elapsed_time):
        #
        #     # adds a new user to dict, and increments existing users with a new process
        #     key = self._new_processes[i].user_id
        #     if key in self.users_dict.keys():
        #         self.users_dict[key] += 1
        #     else:
        #         self.users_dict[key] = 1
        #
        #     self._ready_queue.append(self._new_processes.pop(0))
        #     self.quantum_alloc()

    def quantum_alloc(self):
        for process in self._ready_queue:
            new_quant = int(self.quantum // len(self.users_dict) // self.users_dict[process.user_id])
            process.set_quantum(new_quant)

    # execute a process
    def execute(self, process):
        print("thread started")
        # thread has started its execution
        if process.state is None:
            self._output.write(
                "Time {}, User {}, Process {}, {}\n".format(
                    int(self._total_elapsed_time), process.user_id,
                    process.process_id,
                    'Started'))
            self._output.write(
                "Time {}, User {}, Process {}, {}\n".format(
                    int(self._total_elapsed_time), process.user_id,
                    process.process_id,
                    'Resumed'))
        # paused thread has resumed execution
        elif process.state == 'Paused':
            process.state = 'Resumed'
            self._output.write(
                "Time {}, User {}, Process {}, {}\n".format(
                    int(self._total_elapsed_time), process.user_id,
                    process.process_id,
                    'Resumed'))

        # TODO: do we need to context switch if time left is 0 before sleep is completed?
        time.sleep(process.quantum)
        process.time_left = process.time_left - process.quantum
        # check if any other processes became ready
        self.verify_if_ready()
        self.quantum_alloc()
        # print(self._total_elapsed_time)
        print("User: " + process.user_id + " Process: " + str(process.process_id) + " Quantum: " + str(process.quantum) + " Time left: " + str(process.time_left))
        print("Q len: " + str(len(self._ready_queue)))
        
        # if the process is finished executing, report the finished status to output
        if process.time_left <= 0:
            self._output.write(
                "Time {}, User {}, Process {}, {}\n".format(
                     int(self._total_elapsed_time), process.user_id,
                     process.process_id,
                     'Paused'))
            self._output.write(
                "Time {}, User {}, Process {}, {}\n".format(
                    int(self._total_elapsed_time), process.user_id,
                    process.process_id,
                    'Finished'))
            # decrement the number of running processes for the user
            self.users_dict[process.user_id] -= 1
            if self.users_dict[process.user_id] == 0:
                self.users_dict.pop(process.user_id)
            self.quantum_alloc()
        # if the process needs more time to execute, set its state to 'Paused' and add it back to the ready queue
        else:
            process.state = 'Paused'
            self._output.write(
                "Time {}, User {}, Process {}, {}\n".format(
                    int(self._total_elapsed_time), process.user_id,
                    process.process_id,
                    'Paused'))
            self._ready_queue.append(process)


# class used to encapsulate the specifications of each process
class Process:

    # default constructor
    def __init__(self, user: str, pid: int, ready_t: int, service_t: int):
        # user the process belongs to
        self._user_id = user
        # process number
        self._process_id = pid
        # amount of quantum time allocated to process
        self._quantum = 0
        # time at which the process is ready to be executed
        self._ready_time = ready_t
        # time left until process completes its execution
        self._time_left = service_t
        # process state
        self._state = None

    """ Getters """

    @property
    def user_id(self):
        return self._user_id

    @property
    def process_id(self):
        return self._process_id

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

    def set_quantum(self, new_quant):
        self._quantum = new_quant


# entrypoint of script execution
if __name__ == '__main__':

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

    # list for the allocation of time quantum
    quant_alloc = []


    # # TODO: This is wrong, we can't assign the quantum automatically, we have to calculate it based on the processes that are READY
    # # find the amount of the time quantum allocated to each process
    # num_users = len(user_dict)  # number of users
    # for key in user_dict:
    #     num_user_processes = user_dict[key]
    #     for i in range(0, num_user_processes):
    #         quant_alloc.append(int(quant // num_users // num_user_processes))

    # array of Process objects to be executed
    processes = []

    # program_info = [quant, num_users, num_user_processes]
    # generate a Process object and add it to the list of processes
    counter = 0  # counter used to traverse each previously generated list for process specifications
    for user in user_dict:
        for i in range(0, user_dict[user]):
            processes.append(Process(user, i, ready_time[counter], service_time[counter]))
            counter += 1

    # sort the processes list by ready time in ascending order (to be used as a queue)
    processes.sort(key=lambda x: x.ready_time, reverse=False)

    # run the scheduler
    Scheduler(processes, quant)
