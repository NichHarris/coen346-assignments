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
        threading.Thread.__init__(self)
        # set thread name
        self.name = "Clock"
        # start timer
        self._total_elapsed_time = time.perf_counter()

        self.terminate = False

    # run clock thread
    def run(self):
        print("Starting " + self.name + " Thread")
        while not self.terminate:
            self.update_time()
        print("Exiting " + self.name + " Thread")

    # update and return the total elapsed time
    def get_time(self):
        self.update_time()
        return self._total_elapsed_time

    # update the total elapsed time
    def update_time(self):
        self._total_elapsed_time = time.perf_counter()

    def wait(self):
        time.sleep(3)

    def get_count(self):
        return threading.activeCount()

    def set_terminate(self, state):
        self.terminate = state
