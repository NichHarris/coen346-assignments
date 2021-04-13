# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulator with Concurrency Control


# class used to handle the disk pages -> write/read to a file
class DiskPages:

    # default constructor
    def __init__(self):
        self._output = open("vm.txt", "w")
        self._output.close()
        self.disk_mem = []

    # write to disk page
    def add_page(self, pg_list: list):
        with open("vm.txt", "r") as disk:
            pages = disk.readlines()
        disk.close()
        for page in pages:
            line = page.rstrip('\n').split(" ")
            if str(line[0]) == str(pg_list[0]):
                self.replace(pages, pg_list)
                return
        self.append_to_page(pg_list)

    # append a page to disk page
    def append_to_page(self, pg_list: list):
        self._output = open("vm.txt", "a")
        string = ""
        for val in pg_list:
            string += str(val)
            string += " "
        self._output.write("{}\n".format(string.rstrip()))
        self._output.close()

    # replace a page in disk page
    def replace(self, disk_pages, pg_list):
        with open("vm.txt", "w") as disk:
            for page in disk_pages:
                line = page.rstrip('\n').split(" ")
                string = ""
                if str(line[0]) != str(pg_list[0]):
                    for val in line:
                        string += str(val)
                        string += " "
                    disk.write("{}\n".format(string.rstrip()))
                else:
                    for val in pg_list:
                        string += str(val)
                        string += " "
                    disk.write("{}\n".format(string.rstrip()))
        disk.close()

    # find variableId in disk page
    def read_from_pg(self, variableId: str):
        with open('vm.txt', 'r') as disk_pg:
            disk = disk_pg.readlines()

        for page in disk:
            line = page.rstrip('\n').split(" ")
            if str(variableId) == str(line[0]):
                disk_pg.close()
                return line
        disk_pg.close()
        return -1

    # find if variableId exists in disk page
    def has_page(self, variableId):
        with open('vm.txt', 'r') as disk_pg:
            pages = disk_pg.readlines()
        for line in pages:
            page = line.strip(" ")
            if str(variableId) == str(page[0]):
                return True
        return False
