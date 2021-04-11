# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulator with Concurrency Control


# class used to handle the virtual memory -> write/read
class VirtualMemory:

    # default constructor
    def __init__(self, num_pages: int):
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

    # set a specific page
    def set_page(self, index: int, page: list):
        self._memory[index] = page
        self.set_access_val(index)

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

    # set the access val for a page
    def set_access_val(self, pos):
        self.access_num = self.access_num + 1
        self.access_val[pos] = self.access_num + 1

    # get virtual memory
    def get_memory(self):
        return self._memory

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
