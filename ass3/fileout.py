# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulator with Concurrency Control


# class used to handle the output file
class FileOut:

    def __init__(self, output_file):

        # queue to output file -> format: (time, string)
        self._output_queue = []
        # initialize output file
        self._output = output_file

    # isolate the clock time and add it and the output line to a tuple in the queue -> (time, msg)
    def write(self, line: str):
        components = line.split(",")
        clock = components[0].split(":")
        time = int(clock[1].strip(" "))
        self._output_queue.append((time, line))

    # sort the queue -> this ensures the start and stop process times are ordered correctly and not split up by command executions
    def sort(self):
        self._output_queue.sort(key=lambda time: time[0])

    # write to output.txt file
    def output(self):
        for line in self._output_queue:
            self._output.write(line[1])
