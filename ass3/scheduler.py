# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulator with Concurrency Control

# import the necessary packages
import threading
from process import Process


# class used to handle the FIFO process scheduling
class Scheduler(threading.Thread):

    # default constructor
    def __init__(self, clock, t_list, p_list, output_file, num_processes , num_cores):
        # initialize scheduling thread
        super(Scheduler, self).__init__()
        # set thread name
        self.name = "Scheduler"
        # set terminate status
        self.terminate = False
        # initialize clock object
        self.clock_thread = clock
        # initialize list of threads
        self._thread_list = t_list
        # initialize list of processes
        self._proc_list = p_list
        # initialize output file
        self._output = output_file
        # number of processes
        self.num_proc = num_processes
        # number of cores
        self._cores = num_cores
        # number of active threads
        self._active_processes = []

    # run scheduler thread
    def run(self):
        # print thread status to console
        print("\nStarting " + self.name + " Thread")

        # run thread
        while not self.terminate:
            pass

        # print thread status to console
        print("\nExiting " + self.name + " Thread")

    # set thread to terminate
    def set_terminate(self, state):
        self.terminate = state

    # create process threads
    def create_proc_thread(self):
        while True:
            # process thread creation
            cur_time = int(self.clock_thread.get_time()/1000)
            # holds process data: id, ready time, service time
            proc_data = self._proc_list[0]

            # don't create more threads if cores are full
            while len(self._active_processes) == self._cores:
                continue

            # create process thread if ready time is now or has passed, and there is cores available
            if cur_time >= proc_data[1]:
                t_proc = Process(self.clock_thread, self._active_processes, self._output, proc_data[0], proc_data[1], proc_data[2])
                t_proc.start()
                t_proc.setName(proc_data[0])
                self._thread_list.append(t_proc)
                self._active_processes.append(t_proc)
                self._proc_list.pop(0)
            # break out of process creation
            if len(self._thread_list) == self.num_proc + 2:
                break
