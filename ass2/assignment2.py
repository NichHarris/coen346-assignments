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
    def __init__(self, m_processes: list, m_quantum):
        # initialize the output file for writing
        self._output = open("output.txt", "w")
        # queue of processes which have not yet reached their ready time
        # enqueue: .append(), dequeue: .pop(0)
        self._new_processes = m_processes
        # queue of processes ready to be executed
        # enqueue: .append(), dequeue: .pop(0)
        self._ready_queue = []
        # holds the elapsed time of the program
        self._total_elapsed_time = time.perf_counter()
        # holds (key) current active user(s) and (value) the number of active process(es) of the user(s)
        self.users_dict = {}
        # holds quantum value
        self.quantum = m_quantum

        # check if a new process needs to be added to ready queue and/or execute a process in the ready queue
        while len(self._new_processes) or len(self._ready_queue):
            # update the elapsed time
            self._total_elapsed_time = time.perf_counter()
            # check if any new processes are ready to be executed
            self.verify_if_ready()
            print(int(self._total_elapsed_time))
            # while there are processes waiting in the ready queue, dequeue a process and execute it using a single thread
            if len(self._ready_queue) != 0:
                self._ready_queue[0].print_process()
                t = threading.Thread(target=self.execute, args=(self._ready_queue.pop(0),))
                t.start()
                t.join()
                print("thread completed")

    # add a process to the ready queue if its ready to run
    def verify_if_ready(self):
        if len(self._new_processes) != 0:
            for process in self._new_processes:
                if process.ready_time <= int(self._total_elapsed_time):
                    # adds a new user and process to dict, and increments existing users with a new process
                    key = process.user_id
                    if key in self.users_dict.keys():
                        self.users_dict[key] += 1
                    else:
                        self.users_dict[key] = 1
                    # add process to ready queue
                    self._ready_queue.append(process)
                    # remove process from new_processes queue
                    self._new_processes.pop(0)
        self.quantum_alloc()

    # update the quantum of each process remaining in the ready queue
    def quantum_alloc(self):
        for process in self._ready_queue:
            updated_quantum = int(self.quantum // len(self.users_dict) // self.users_dict[process.user_id])
            process.set_quantum(updated_quantum)

    # execute a process
    def execute(self, process):
        print("thread started")
        # thread has started its execution
        if process.state is None:
            self.print_to_file(process, 'Started')
            self.print_to_file(process, 'Resumed')
        # paused thread has resumed execution
        elif process.state == 'Paused':
            process.state = 'Resumed'
            self.print_to_file(process, 'Resumed')

        # sleep thread for the length of the process' quantum, or remaining time
        if process.quantum >= process.time_left:
            time.sleep(process.time_left)
        else:
            time.sleep(process.quantum)
        # update process' remaining time
        process.time_left = process.time_left - process.quantum

        # update the elapsed time
        self._total_elapsed_time = time.perf_counter()
        # check if any other processes became ready
        self.verify_if_ready()

        # if the process is finished executing, report the finished status to output
        if process.time_left <= 0:
            self.print_to_file(process, 'Paused')
            self.print_to_file(process, 'Finished')

            # decrement the number of running processes for the user
            self.users_dict[process.user_id] -= 1
            if self.users_dict[process.user_id] == 0:
                self.users_dict.pop(process.user_id)
            # update remaining processes quantum
            self.quantum_alloc()
        # if the process needs more time to execute, set its state to 'Paused' and add it back to the ready queue
        else:
            process.state = 'Paused'
            self.print_to_file(process, 'Paused')
            self._ready_queue.append(process)

    # print output message to file
    def print_to_file(self, process, state):
        self._output.write(
            "Time {}, User {}, Process {}, {}\n".format(
                int(self._total_elapsed_time), process.user_id,
                process.process_id,
                state))


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

    def set_quantum(self, new_quantum):
        self._quantum = new_quantum

    """ Testing Prints """

    def print_process(self):
        print("Process info: User: " + str(self.user_id) + " Process: " + str(self.process_id) + " Quantum: " + str(
            self.quantum) + " Ready Time: " + str(self.ready_time) + " Time Left: " + str(
            self.time_left) + " State: " + str(self.state))


# entrypoint of script execution
if __name__ == '__main__':

    # open input.txt and read file content
    with open('input.txt', 'r') as file:
        lines = file.readlines()

    # get the time quantum of the program
    quantum = int(lines.pop(0))

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

    # array of Process objects to be executed
    processes = []

    # generate a Process object and add it to the list of processes
    counter = 0  # counter used to traverse each previously generated list for process specifications
    for user in user_dict:
        for i in range(0, user_dict[user]):
            processes.append(Process(user, i, ready_time[counter], service_time[counter]))
            counter += 1

    # sort the processes list by ready time in ascending order (to be used as a queue)
    processes.sort(key=lambda x: x.ready_time, reverse=False)

    # run the scheduler
    Scheduler(processes, quantum)
