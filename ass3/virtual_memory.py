# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulator with Concurrency Control
import threading
from clock import Clock


# class used to handle the virtual memory -> write/read
class VirtualMemory:

    # default constructor
    def __init__(self, num_pages: int, t_clock):
        # list located in physical memory
        # memory format: [variableId, value]
        self._memory = []
        # number of memory pages available
        self._num_pages = num_pages
        # initialize virtual memory
        self.init_memory()
        # access value for each page
        self.access_val = [0] * num_pages
        # access num
        self.access_num = 0
        # initialize the clock thread
        self.clock = t_clock

    # get a certain page from virtual memory
    def get_page(self, variableId: str):
        i = 0
        for page in self._memory:
            if page[0] == variableId:
                self.set_access_val(i)
                return page[1]
            i += 1
        return -1

    # return index of least recently used virtual memory page
    def get_lru_index(self):
        return self.access_val.index(min(self.access_val))

    def set_page_i(self, index: int, page: list):
        self._memory[index] = page
        self.set_access_val(index)

    def set_page(self, variable: str):
        pass

    # fill memory if it has open spots
    def fill_memory(self, variableId, value):
        for i in range(0, self._num_pages):
            if not self._memory[i]:
                self._memory[i] = [variableId, value]
                # update access value for that item
                self.set_access_val(i)
                break

    # release page from virtual memory
    def release_page(self, variableId):
        for i in range(0, self._num_pages):
            if self._memory[i]:
                if self._memory[i][0] == variableId:
                    self._memory[i] = []
                    break

    # return number of memory pages
    def get_num_pages(self):
        return self._num_pages

    # return access val of given page number
    def get_access_val(self, pos):
        return self.access_val[pos]

    # set the access val for a page
    def set_access_val(self, pos):
        self.access_num = self.access_num + 1
        self.access_val[pos] = self.access_num + 1


    # get virtual memory
    def get_memory(self):
        return self._memory

    # get list of access values
    def get_access_list(self):
        return self.access_val

    # checks if memory is full
    def is_full(self):
        for page in self._memory:
            if not page:
                return False
        return True

    # initialize virtual memory to empty
    def init_memory(self):
        for j in range(0, self._num_pages):
            self._memory.append([])


# if __name__ == '__main__':
#     cock = Clock()
#     cock.start()
#     vm = VirtualMemory(2, cock)
#
#     for i in range(0, 2):
#         vm.fill_memory(i + 1, i * 3 + 5)
#         cock.wait(1)
#
#     print(vm.get_memory())
#     print(vm.get_access_list())
#     cock.set_terminate(True)
#     cock.join()
