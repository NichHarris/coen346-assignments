# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulator with Concurrency Control


# class used to handle the virtual memory -> write/read
class Commands:

    # default constructor
    def __init__(self, c_list):
        # initialize list of commands
        self._cmd_list = c_list
        # cmd index
        self._cmd_index = 0

    # return position in command list
    def current_cmd(self):
        return self._cmd_index

    # increment cmd index
    def next_cmd(self):
        self._cmd_index = (self._cmd_index + 1) % len(self._cmd_list)

    # return list of commands
    def get_cmd_list(self):
        return self._cmd_list


