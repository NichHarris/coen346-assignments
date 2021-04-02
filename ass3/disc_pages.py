# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulator with Concurrency Control
import time
import threading
# class used to handle the disc pages -> write/read to a file
class DiscPages:

    # default constructor
    def __init__(self):
        self._output = open("vm.txt", "w")
        self._output.close()
        self.lock = threading.Lock()

    # write to disk page
    def write_to_page(self, pg_list: list):
        with open("vm.txt", "r") as disk:
            pages = disk.readlines()
        disk.close()
        for page in pages:
            line = page.rstrip('\n').split(" ")
            if line[0] == pg_list[0]:
                self.replace(pages, pg_list)
                return
        self.append_to_page(pg_list)

    def append_to_page(self, pg_list: list):
        self._output = open("vm.txt", "a")
        string = ""
        for val in pg_list:
            string += str(val)
            string += " "
        self._output.write("{}\n".format(string.rstrip()))
        self._output.close()

    def replace(self, disk_pages, pg_list):
        with open("vm.txt", "w") as disk:
            for page in disk_pages:
                line = page.rstrip('\n').split(" ")
                string = ""
                if line[0] != pg_list[0]:
                    for val in line:
                        string += str(val)
                        string += " "
                        print("here1: " + string)
                    disk.write("{}\n".format(string.rstrip()))
                else:
                    for val in pg_list:
                        string += str(val)
                        string += " "
                        print("here2: " + string)
                    disk.write("{}\n".format(string.rstrip()))
        disk.close()

    # find variableId in disk page
    def read_from_page(self, variableId: str):
        # self.lock.acquire()
        with open('vm.txt', 'r') as disk_pg:
            disk = disk_pg.readlines()

        for page in disk:
            line = page.rstrip('\n').split(" ")
            if variableId == line[0]:
                disk_pg.close()
                # self.lock.release()
                return line
        disk_pg.close()
        print("here")
        # self.lock.release()
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

# if __name__ == '__main__':
#
#     disk = DiscPages()
#     memory = [["2", "7"], ["5", "6"]]
#
#     disk.write_to_page(["1", "3"])
#     disk.write_to_page(["1", "4"])
#     disk.write_to_page(["2", "6"])
#
#     for i in range(0, len(memory)):
#         if disk.has_page(memory[i][0]):
#             temp = memory[i]
#             disk.write_to_page(["2", "6"])
#             temp_disc = disk.read_from_page(temp[0])
#             print("Disk temp: {}".format(temp_disc))
#             memory[i] = temp_disc
#             disk.write_to_page(temp)
#     print(memory)
