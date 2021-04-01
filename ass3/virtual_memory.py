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
        # number of memory pages available
        self._num_pages = num_pages
        # access value for each page
        self.access_val = [num_pages]
        # initialize the clock thread
        self.clock = t_clock

    # get a certain page from virtual memory
    def get_page(self, variableId: str):
        # improved logic, uses access vaL list to set each memory pages access val
        # this way we don't have to strip the access val from the data in memory
        for i in range(0, self._num_pages - 1):
            if self._memory[i][0] == variableId:
                self.set_access_val(i)
                return self._memory[i]
        return -1

        # i = 0
        # for page in self._memory:
        #     if page[1] == variableId:
        #         # need to update access time of page
        #         self._memory[i][0] = int(self.clock.get_time() / 1000)
        #         return self._memory[i]
        #     i += 1
        # return -1

    # set the page for a certain spot in virtual memory
    def set_page(self, pos: int, page: list):
        self._memory[pos] = page
        self.set_access_val(pos)

    # return number of memory pages
    def get_num_pages(self):
        return self._num_pages

    # return access val of given page number
    def get_access_val(self, pos):
        return self.access_val[pos]

    # set the access val for a page
    def set_access_val(self, pos):
        self.access_val[pos] = int(self.clock.get_time() / 1000)

    # checks for empty spot in memory
    def is_full(self):
        for page in self._memory:
            if page is None:
                return False
        return True
