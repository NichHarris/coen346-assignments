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
        self.disk_mem = []

    # TODO: Implement queue in vm_manager to handle file I/O race conditions
    # write to disk page
    def add_page(self, pg_list: list):
        with open("vm.txt", "r") as disk:
            pages = disk.readlines()
        disk.close()
        for page in pages:
            print("Here: " + page)
            line = page.rstrip('\n').split(" ")
            if str(line[0]) == str(pg_list[0]):
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

    # # add or replace page to disk
    # def add_page(self, pg_list: list):
    #     if self.has_page(pg_list[0]):
    #         self.swap_page(pg_list)
    #     else:
    #         self.disk_mem.append(pg_list)
    #
    # # return page of given variableId
    # def read_from_pg(self, variableId: str):
    #     for page in self.disk_mem:
    #         if variableId == page[0]:
    #             return page
    #     return -1
    #
    # # replace a page
    # def swap_page(self, pg_list: list):
    #     for i in range(0, len(self.disk_mem)):
    #         if self.disk_mem[i][0] == pg_list[0]:
    #             self.disk_mem[i] = pg_list
    #
    # # find if variableId exists in disk page
    # def has_page(self, variableId: str):
    #     for page in self.disk_mem:
    #         if variableId == page[0]:
    #             return True
    #     return False
    #
    # # write to file
    # def write_to_file(self):
    #     self._output = open("vm.txt", "w")
    #     for page in self.disk_mem:
    #         string = ""
    #         for val in page:
    #             string += str(val)
    #             string += " "
    #         self._output.write("{}\n".format(string.rstrip()))
    #     self._output.close()

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
