# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Fair-share Process Scheduling Simulator

# import the necessary packages


# class used to handle the virtual memory -> write/read
class VirtualMemory:

    # default constructor
    def __init__(self):
        # list located in physical memory
        self._memory = []
