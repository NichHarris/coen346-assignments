# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Fair-share Process Scheduling Simulator

# import the necessary packages
import threading
from process import Process


# class used to handle the FIFO process scheduling
class Scheduler(threading.Thread):

    # default constructor
    def __init__(self, clock, t_list, p_list, num_processes):
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
        self._output = open("output.txt", "w")
        # num of processes
        self.num_proc = num_processes

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

    def create_proc_thread(self):
        while True:
            # process thread creation
            cur_time = int(self.clock_thread.get_time()/1000)
            tuple = self._proc_list[0]
            if cur_time == tuple[1]:
                t_proc = Process(self.clock_thread, self._output, tuple[0], tuple[1], tuple[2])
                t_proc.start()
                self._thread_list.append(t_proc)
                self._proc_list.pop(0)
            # using this to break right now, eventually we want to break when theres no commands left
            if len(self._thread_list) == self.num_proc + 2:
                break