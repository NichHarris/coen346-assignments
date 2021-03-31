# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulation

# import the necessary packages
import threading
import time


# class used to handle a threaded clock
class Clock(threading.Thread):
    def __init__(self):
        # initialize clock thread
        super(Clock, self).__init__()
        # set thread name
        self.name = "Clock"
        # start timer
        self._total_elapsed_time = time.perf_counter()
        # set terminate status
        self.terminate = False

    # run clock thread
    def run(self):
        # print thread status to console
        print("\nStarting " + self.name + " Thread")

        # run thread
        while not self.terminate:
            self.update_time()

        # print thread status to console
        print("\nExiting " + self.name + " Thread")

    # update and return the total elapsed time, rounded to nearest 10.
    def get_time(self):
        self.update_time()
        return round(int(self._total_elapsed_time*1000)/10)*10

    # update the total elapsed time
    def update_time(self):
        self._total_elapsed_time = time.perf_counter()

    # wait for a specified duration
    def wait(self, duration):
        time.sleep(duration)

    # set thread to terminate
    def set_terminate(self, state):
        self.terminate = state
