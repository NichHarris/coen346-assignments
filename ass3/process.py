# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Fair-share Process Scheduling Simulator

# import the necessary packages
import threading


# class used to encapsulate the specifications of each process
class Process(threading.Thread):

    # default constructor
    def __init__(self, clock, output_file, proc_id, start_time, service_time):
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
        # initialize output file
        self._output = output_file
        # initialize start time
        self._start_time = start_time
        # initialize service time
        self._service_time = service_time

    # run process thread
    def run(self):
        # print process started to output file
        self._output.write(
            "Clock: {}, Process {}: {}\n".format(self.clock_thread.get_time(), self._process_id, "Started"))

        # run thread for its time
        while int(self.clock_thread.get_time()/1000) - self._start_time < self._service_time:
            pass

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
