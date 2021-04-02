# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulator with Concurrency Control

# import the necessary packages
import threading
from random import Random


# class used to encapsulate the specifications of each process
class Process(threading.Thread):

    # default constructor
    def __init__(self, clock, manager, commands, active_processes, output_file, proc_id, start_time, service_time):
        # initialize process thread
        super(Process, self).__init__()
        # set thread _name
        self.name = "Process"
        # set process id
        self._process_id = proc_id
        # set _terminate status
        self.terminate = False
        # initialize clock object
        self.clock_thread = clock
        # initialize manager object
        self.manager_thread = manager
        # initialize commands object
        self._commands = commands
        # initialize output file
        self._output = output_file
        # initialize start time
        self._start_time = start_time
        # initialize service time
        self._service_time = service_time
        # terminate time
        self._terminate_time = self._start_time + self._service_time
        # number of active threads
        self.proc_list = active_processes
        self.rand = Random()
        # lock
        self.lock = threading.Lock()

    # run process thread
    def run(self):
        # print thread status to console
        print("\nStarting {} {} Thread".format(self.name, self._process_id))

        # print process started to output file
        self._output.write(
            "Clock: {}, Process {}: {}\n".format(self.clock_thread.get_time(), self._process_id, "Started"))

        remaining_time = self._terminate_time - self.clock_thread.get_time()/1000

        # run thread for its service time
        while remaining_time >= 0:
            # TODO: Debug synchronization
            # get current command
            command = self._commands.get_cmd_list()[self._commands.current_cmd()]

            self.lock.acquire()
            # print info
            print("Command: {} Running on Process: {} at time {}".format(command, self._process_id,
                                                                         self.clock_thread.get_time()))
            # block access to critical section

            # call api
            self.manager_thread.call_api(command, self._process_id)

            # # increment to next command
            # self._commands.next_cmd()

            # wait for a random amount of time
            self.lock.release()

            # release access to critical section
            if self._terminate_time - self.clock_thread.get_time()/1000 > 0:
                self.clock_thread.wait(
                    min(self.clock_thread.get_time() - self._start_time, self.rand.randrange(10, 1000)))

            remaining_time = self._terminate_time - self.clock_thread.get_time()/1000

        # pop a process from terminated process (clears up a core)
        self.proc_list.pop(0) if self.proc_list[0].get_id() == self._process_id else self.proc_list.pop(1)

        # print thread status to console
        print("\nExiting {} {} Thread".format(self.name, self._process_id))
        # TODO: Debug clock printout and update time, sometimes we get far from the required timeout time
        # TODO: Timing off probably again due to synchronization
        # TODO: Maybe improve clock accuracy
        # print process finished to output file
        self._output.write(
            "Clock: {}, Process {}: {}\n".format(self.clock_thread.get_time(), self._process_id, "Finished"))

    # set thread to _terminate
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
