# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulator with Concurrency Control

# import the necessary packages
import threading
import time


# class used to handle a threaded clock
class Clock(threading.Thread):
    def __init__(self):
        # initialize clock thread
        super(Clock, self).__init__()
        # set thread _name
        self.name = "Clock"
        # start timer
        self._total_elapsed_time = 0
        # set _terminate status
        self.terminate = False

    # run thread when thread.start() is called
    def run(self):
        # print thread status to console
        print("\nStarting " + self.name + " Thread")

        # give time for processes to come online
        time.sleep(0.1)

        # run thread
        while not self.terminate:
            time.sleep(0.1)
            self._total_elapsed_time += 100

        # print thread status to console
        print("\nExiting " + self.name + " Thread")

    # update and return the total elapsed time, rounded to nearest 10.
    def get_time(self):
        return int(round(self._total_elapsed_time)/10)*10

    # update the total elapsed time
    def update_time(self, _time):
        self._total_elapsed_time += _time
        time.sleep(_time/1000)

    # set thread to _terminate
    def set_terminate(self, state):
        self.terminate = state
