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
    def __init__(self, num_pages: int, t_clock):
        # list located in physical memory
        # memory format: [last access time, variableId, value]
        self._memory = [[] for i in range(num_pages)]
        self._num_pages = num_pages
        self.access_val = 0
        self.clock = t_clock

    # get a certain page from virtual memory
    # TODO: add clock for last access time
    def get_page(self, variableId: str):
        i = 0
        for page in self._memory:
            if page[1] == variableId:
                # need to update access time of page
                self._memory[i][0] = int(self.clock.get_time()/1000)
                return self._memory[i]
            i += 1
        return -1

    # set the page for a certain spot in virtual memory
    # TODO: add clock for last access time
    def set_page(self, pos: int, page: list):
        self._memory[pos] = page

    def get_num_pages(self):
        return self._num_pages

    def printy(self):
        return self._memory
    # set page should set empty space with page

    # is full should check if there's any empty space
