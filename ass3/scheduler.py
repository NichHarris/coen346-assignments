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
    def __init__(self, manager, commands, clock, t_list, p_list, output_file, num_cores):
        # initialize scheduling thread
        super(Scheduler, self).__init__()
        # set thread _name
        self.name = "Scheduler"
        # set _terminate status
        self.terminate = False
        # initialize manager object
        self.manager_thread = manager
        # initialize clock object
        self.clock_thread = clock
        # initialize command object
        self._commands = commands
        # initialize list of threads
        self._thread_list = t_list
        # initialize list of processes
        self._proc_list = p_list
        # initialize output file
        self._output = output_file
        # number of cores
        self._cores = num_cores
        # number of active threads
        self._active_processes = []

    # run thread when thread.start() is called
    def run(self):
        # print thread status to console
        print("\nStarting " + self.name + " Thread")

        # run thread
        while not self.terminate:
            pass

        # print thread status to console
        print("\nExiting " + self.name + " Thread")

    # set thread to _terminate
    def set_terminate(self, state):
        self.terminate = state

    # create process threads
    def create_proc_thread(self):

        # start clock thread
        self.clock_thread.start()

        # generate processes
        while True:

            # update time and round to the second
            cur_time = self.clock_thread.get_time()

            if len(self._proc_list) != 0:
                # holds process data: id, ready time, service time
                proc_data = self._proc_list[0]

                # create process thread if ready time is now or has passed, and there is cores available
                if cur_time == proc_data[1]*1000 and len(self._active_processes) != self._cores:
                    t_proc = Process(self.clock_thread, self.manager_thread, self._commands, self._active_processes, self._output, proc_data[0], cur_time, proc_data[2]*1000)
                    t_proc.start()
                    self._thread_list.append(t_proc)
                    self._active_processes.append(t_proc)
                    self._proc_list.pop(0)

            # break out of process creation
            if len(self._active_processes) == 0 and len(self._proc_list) == 0:
                break
