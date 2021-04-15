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
    def __init__(self, clock, manager, commands, active_processes, file_out, proc_id, start_time, service_time):
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
        # initialize file out object
        self._file_out = file_out
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

        # run thread for its service time
        while self._clock_thread.get_time() < self._terminate_time or self.terminate:
            
            # run a command
            self.run_command()

        # print process finished to output file
        self.print_to_file("Finished", self._terminate_time)

        # remove finished process from active process list (clears up a core)
        for i in range(0, len(self._active_proc)):
            if self._active_proc[i].get_id() == self._process_id:
                self._active_proc.pop(i)
                break

        # print thread status to console
        print("\nExiting Process {} Thread".format(self._process_id))

    # set thread to _terminate
    def set_terminate(self, state):
        self.terminate = state

    # print output message to file
    def print_to_file(self, state: str, _time):
        self._file_out.write(
            "Clock: {}, Process {}: {}.\n".format(
                round(_time/100)*100, self._process_id,
                state))

    # get id number of a process
    def get_id(self):
        return self._process_id

    # run a command
    def run_command(self):

        # synchronization to prevent the same commands from being run
        self.lock.acquire()

        # simulate api call time
        wait_time = min(self._terminate_time - self._clock_thread.get_time(), self.rand.randrange(10, 1000))/1000
        if wait_time <= 0:
            self.set_terminate(True)
        else:
            # simulate call time
            time.sleep(wait_time)
            # ensure we aren't running a long command (one that needs to swap or write to disk_pages) too close to terminate time
            if self._terminate_time - self._clock_thread.get_time() > 600:
                # get current command
                command = self._commands.get_cmd_list()[self._commands.current_cmd()]
                # increment to next command
                self._commands.next_cmd()
                # call api
                self.manager_thread.call_api(command, self._process_id, self._terminate_time)

        # release lock
        self.lock.release()

