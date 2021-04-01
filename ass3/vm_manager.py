# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulator with Concurrency Control

# import the necessary packages
import threading


# class used to created a threaded virtual memory manage
class Manager(threading.Thread):

    def __init__(self, memory, clock, disc_page, output_file):
        # initialize manager thread
        super(Manager, self).__init__()
        # set thread name
        self.name = "Memory Manager"
        # set terminate status
        self.terminate = False
        # initialize virtual memory object
        self.v_mem = memory
        # initialize clock object
        self.clock_thread = clock
        # initialize disc page object
        self._disc_page = disc_page
        # initialize output file
        self._output = output_file

    def run(self):
        # print thread status to console
        print("\nStarting " + self.name + " Thread")

        # run thread
        while not self.terminate:
            pass

        # print thread status to console
        print("\nExiting " + self.name + " Thread")

    def store(self, variableId: str, value):
        if self.v_mem.is_full():
            self._disc_page.write_to_page()
        else:
            self.v_mem.set_page([variableId, value])

    def release(self, variableId: str):
        pass

    def look_up(self, variableId: str):
        value = self.v_mem.get_page(variableId)
        if value == -1:
            self.swap(variableId)

    # swap
    def swap(self, variableId):

        min_index = self.v_mem.get_lru_index()
        other_variable_id = self.v_mem.get_memory()[min_index][0]
        # get v_men page
        mem_page = self.v_mem.get_memory()[min_index]
        # read from disc
        disc = self._disc_page.read_from_page(variableId)
        # set v_men page
        self.v_mem.set_page(disc)
        # set disc page
        self._disc_page.write_to_page(mem_page)

        self._output.write(
            "Clock: {}, {}, {}: Variable {} with Variable {}\n".format(self.clock_thread.get_time(), self.name, "Swap", variableId, other_variable_id))

    def call_api(self, command: list, p_id):
        # TODO: This is should be done in manager
        if command[0] == "Store" and len(command) == 3:
            self.store(command[1], command[2])
            self.print_to_output(p_id, command[0], command[1], command[2])
        elif command[0] == "Release":
            self.release(command[1])
            self.print_to_output(p_id, command[0], command[1], None)
        elif command[0] == "Lookup":
            self.look_up(command[1])
            self.print_to_output(p_id, command[0], command[1], None)
        else:
            print("Invalid command")

    # set thread to terminate
    def set_terminate(self, state):
        self.terminate = state

    def print_to_output(self, process_id, cmd, variableId, value):
        # print process finished to output file
        self._output.write(
            "Clock: {}, Process {}: {}: Variable {}, Value: {}\n".format(self.clock_thread.get_time(), process_id, cmd, variableId, value))
