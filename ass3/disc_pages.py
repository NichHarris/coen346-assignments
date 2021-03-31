# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Fair-share Process Scheduling Simulator

# import the necessary packages


# class used to handle the disc pages -> write/read to a file
class DiscPages:

    # default constructor
    def __init__(self):
        self._output = open("vm.txt", "w")
        self._output.close()

    def write_to_page(self, pg_list: list):
        self._output = open("vm.txt", "a")
        self._output.write("{}\n".format(pg_list))
        self._output.close()

    def read_from_page(self, line):
        with open('vm.txt', 'r') as disc_pg:
            pages = disc_pg.readlines()
            return pages[line]
