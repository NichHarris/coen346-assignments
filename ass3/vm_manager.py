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


# class used to created a threaded virtual memory manage
class Manager(threading.Thread):

    def __init__(self, memory, cmd_obj, clock, disk_page, output_file):
        # initialize manager thread
        super(Manager, self).__init__()
        # set thread _name
        self._name = "Memory Manager"
        # set _terminate status
        self._terminate = False
        # initialize virtual memory object
        self._v_mem = memory
        # initialize commands object
        self.commands = cmd_obj
        # initialize clock object
        self._clock_thread = clock
        # initialize disc page object
        self._disk_page = disk_page
        # initialize output file
        self._output = output_file
        # random number object
        self.rand = Random()
        # queue for I/O
        self.queue = []

    # run thread when thread.start() is called
    def run(self):
        # print thread status to console
        print("\nStarting " + self._name + " Thread")

        # run thread
        while not self._terminate:
            pass

        # print thread status to console
        print("\nExiting " + self._name + " Thread")

    # execute Store API
    def store(self, variableId: str, value: int):
        if self._v_mem.is_full():
            self._disk_page.add_page([variableId, value])
        else:
            self._v_mem.fill_memory(variableId, value)

    # execute Release API
    def release(self, variableId: str):
        self._v_mem.release_page(variableId)

    # execute Lookup API
    def look_up(self, variableId: str):
        value = self._v_mem.get_page(variableId)
        if value == -1:
            return self.swap(variableId)
        return value

    # execute Swap if lookup located in disk space
    def swap(self, variableId: str):

        # index of least recently used virtual memory page
        lru_index = self._v_mem.get_lru_index()
        # virtual memory copy
        mem_copy = self._v_mem.get_memory()[lru_index]
        # disk page copy
        disk_copy = self._disk_page.read_from_pg(variableId)

        # make sure there wasn't an error during swapping
        if disk_copy == -1:
            self._output.write(
                "Clock: {}, {}, {}: Variable {} with Variable {}\n".format(self._clock_thread.get_time(), self._name,
                                                                           "Swap ERROR", variableId, mem_copy[0]))
            return -1
        else:
            # set virtual memory to copy from disk
            self._v_mem.set_page(lru_index, disk_copy)

        # update disk page with former virtual memory page
        self._disk_page.add_page(mem_copy)

        # write to output file
        self._output.write(
            "Clock: {}, {}, {}: Variable {} with Variable {}\n".format(self._clock_thread.get_time(), self._name,
                                                                       "Swap", variableId, mem_copy[0]))
        # return value
        return disk_copy[1]

    # TODO: Debug api calls timing, this probably relates to synchronization
    def call_api(self, command: list, p_id, term_time):
        # add to queue
        # self.queue.append(command)

        # update index of next command
        self.commands.next_cmd()

        # simulate api call time
        time.sleep(min(term_time - self._clock_thread.get_time(), self.rand.randrange(10, 1000))/1000)

        # # wait for queue to clear up
        # while len(self.queue) > 1:
        #     print(len(self.queue))
        #     pass

        # determine command to run
        value = 0
        if command[0] == "Store" and len(command) == 3:
            self.store(command[1], command[2])
            value = command[2]
        elif command[0] == "Release":
            self.release(command[1])
            value = None
        elif command[0] == "Lookup":
            value = self.look_up(command[1])
            self._clock_thread.update_time(10)
        else:
            print("Invalid command")

        # self.queue.pop(0)
        # print to file status
        self.print_to_output(p_id, command[0], command[1], value)

    # set thread to _terminate
    def set_terminate(self, state):
        self._terminate = state

    # write to output file
    def print_to_output(self, process_id, cmd, variableId, value):
        # print process finished to output file
        if cmd == "Release":
            self._output.write(
                "Clock: {}, Process {}: {}: Variable {}\n".format(self._clock_thread.get_time(), process_id, cmd,                                                              variableId))
        else:
            self._output.write(
                "Clock: {}, Process {}: {}: Variable {}, Value: {}\n".format(self._clock_thread.get_time(), process_id,
                                                                             cmd, variableId, value))
