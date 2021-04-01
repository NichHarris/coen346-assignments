# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulator with Concurrency Control

# import the necessary packages
import threading


# class used to encapsulate the specifications of each process
class Process(threading.Thread):

    # default constructor
    def __init__(self, clock, manager, c_list, active_processes, output_file, proc_id, start_time, service_time):
        # initialize process thread
        super(Process, self).__init__()
        # set thread name
        self.name = "Process"
        # set process id
        self._process_id = proc_id
        # set terminate status
        self.terminate = False
        # initialize clock object
        self.clock_thread = clock
        # initialize manager object
        self.manager_thread = manager
        # initialize list of commands
        self._cmd_list = c_list
        # initialize output file
        self._output = output_file
        # initialize start time
        self._start_time = start_time
        # initialize service time
        self._service_time = service_time
        # number of active threads
        self.proc_list = active_processes

    # run process thread
    def run(self):

        # print thread status to console
        print("\nStarting {} {} Thread".format(self.name, self._process_id))

        # print process started to output file
        self._output.write(
            "Clock: {}, Process {}: {}\n".format(self.clock_thread.get_time(), self._process_id, "Started"))

        # run thread for its service time
        while int(self.clock_thread.get_time()/1000) - self._start_time < self._service_time:
            # TODO: This is where we should handle commands
            pass

        # pop a process from terminated process (clears up a core)
        self.proc_list.pop(0) if self.proc_list[0].get_id() == self._process_id else self.proc_list.pop(1)

        # print thread status to console
        print("\nExiting {} {} Thread".format(self.name, self._process_id))

        # print process finished to output file
        self._output.write(
            "Clock: {}, Process {}: {}\n".format(self.clock_thread.get_time(), self._process_id, "Finished"))

    # set thread to terminate
    def set_terminate(self, state):
        self.terminate = state

    # print output message to file
    def print_to_file(self, process, state):
        self._output.write(
            "Clock: {}, Process {}: {}\n".format(
                self.clock_thread.get_time(), self._process_id,
                state))

    def get_start_time(self):
        return self._start_time

    def get_id(self):
        return self._process_id
