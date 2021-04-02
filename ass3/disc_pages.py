# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulator with Concurrency Control

# class used to handle the disc pages -> write/read to a file
class DiscPages:

    # default constructor
    def __init__(self):
        self._output = open("vm.txt", "w")
        self._output.close()

    # write to disk page
    def write_to_page(self, pg_list: list):
        self._output = open("vm.txt", "a")
        string = ""
        for val in pg_list:
            string += str(val)
            string += " "
        self._output.write("{}\n".format(string))
        self._output.close()

    # find variableId in disk page
    def read_from_page(self, variableId: str):
        with open('vm.txt', 'r') as disk_pg:
            disk = disk_pg.readlines()
        for line in disk:
            page = line.rstrip('\n').split(" ")
            if variableId == str(page[0]):
                disk_pg.close()
                return page
        disk_pg.close()
        # TODO: Think of something better to do in this case
        return -1

    # find if variableId exists in disk page
    def has_page(self, variableId):
        with open('vm.txt', 'r') as disk_pg:
            pages = disk_pg.readlines()
        for line in pages:
            page = line.strip(" ")
            if variableId == page[0]:
                return True
        return False
