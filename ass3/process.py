# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulator with Concurrency Control

# import the necessary packages
import threading
import time
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
        self._clock_thread = clock
        # initialize manager object
        self.manager_thread = manager
        # initialize commands object
        self._commands = commands
        # initialize output file
        self._output = output_file
        # initialize start time  in ms
        self._start_time = start_time
        # initialize service time in ms
        self._service_time = service_time
        # terminate time in ms
        self._terminate_time = self._start_time + self._service_time
        # number of active threads
        self._active_proc = active_processes
        # random number object
        self.rand = Random()
        # synchronization
        self.lock = threading.Lock()

    # run thread when thread.start() is called
    def run(self):

        # print thread status to console
        print("\nStarting Process {} Thread".format(self._process_id))

        # print process started to output file
        self.print_to_file("Started", self._start_time)

        # TODO: Improve this
        # run thread for its service time
        while self._clock_thread.get_time() < self._terminate_time or self.terminate:

            self.run_command()
            # slow down execution of commands, so we don't have it run through the command list more than 2 times
            # time.sleep(0.5)

        # remove finished process from active process list (clears up a core)
        for i in range(0, len(self._active_proc)):
            if self._active_proc[i].get_id() == self._process_id:
                self._active_proc.pop(i)
                break

        # print thread status to console
        print("\nExiting Process {} Thread".format(self._process_id))

        # print process finished to output file
        self.print_to_file("Finished", self._terminate_time)

    # set thread to _terminate
    def set_terminate(self, state):
        self.terminate = state

    # print output message to file
    def print_to_file(self, state: str, _time):
        self._output.write(
            "Clock: {}, Process {}: {}.\n".format(
                _time, self._process_id,
                state))

    # get id number of a process
    def get_id(self):
        return self._process_id

    # run a command
    def run_command(self):
        # synchronization to prevent the same commands from being run
        self.lock.acquire()

        # get current command
        command = self._commands.get_cmd_list()[self._commands.current_cmd()]

        # call api
        self.manager_thread.call_api(command, self._process_id, self._terminate_time)

        time.sleep(min(self._terminate_time - self._clock_thread.get_time(), self.rand.randrange(10, 1000))/1000)
        # release lock
        self.lock.release()
