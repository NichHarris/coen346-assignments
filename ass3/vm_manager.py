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

    def __init__(self, memory, disc_page):
        # initialize manager thread
        super(Manager, self).__init__()
        # set thread name
        self.name = "VM Manager"
        # set terminate status
        self.terminate = False
        # initialize virtual memory object
        self._memory = memory
        # initialize disc page object
        self._disc_page = disc_page

    def run(self):
        # print thread status to console
        print("\nStarting " + self.name + " Thread")

        # run thread
        while not self.terminate:
            pass

        # print thread status to console
        print("\nExiting " + self.name + " Thread")

    def store(self, variableId, value):
        if self._memory.is_full():
            self._disc_page.write_to_page()
        else:
            for i in range(0, self._memory.get_num_pages() - 1):
                if self._memory[i] is None:
                    self._memory.set_page(i, [variableId, value])

    def release(self, variableId: str):
        pass

    def look_up(self, variableId: str):
        value = self._memory.get_page(variableId)
        if value == -1:
            self.swap()

    # swap
    def swap(self):
        pass

    # set thread to terminate
    def set_terminate(self, state):
        self.terminate = state
