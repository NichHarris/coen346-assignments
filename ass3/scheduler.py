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
        super(Scheduler, self).__init__()
        # set thread name
        self.name = "Scheduler"
        # set terminate status
        self.terminate = False

    # run scheduler thread
    def run(self):
        # print thread status to console
        print("\nStarting " + self.name + " Thread")

        # run thread
        while not self.terminate:
            pass

        # print thread status to console
        print("\nExiting " + self.name + " Thread")

    # set thread to terminate
    def set_terminate(self, state):
        self.terminate = state
