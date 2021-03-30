# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Fair-share Process Scheduling Simulator

# import the necessary packages
import threading


# class used to handle the FIFO process scheduling
class Scheduler(threading.Thread):

    # default constructor
    def __init__(self):
        # initialize scheduling thread
        threading.Thread.__init__(self)
        # set thread name
        self.name = "Scheduler"
        self.terminate = False

    # run scheduler thread
    def run(self):
        print("Starting " + self.name + " Thread")
        while not self.terminate:
            pass
        print("Exiting " + self.name + " Thread")

    def set_terminate(self, state):
        self.terminate = state
