# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulator with Concurrency Control

# import the necessary packages
from clock import Clock
from scheduler import Scheduler
from vm_manager import Manager
from process import Process
from disc_pages import DiscPages
from virtual_memory import VirtualMemory

# entrypoint of script execution
if __name__ == '__main__':

    # open memconfig.txt and read file content
    with open('memconfig.txt', 'r') as mem_config:
        cfg = mem_config.readlines()
    # open processes.txt and read file content
    with open('processes.txt', 'r') as proc_file:
        proc_lines = proc_file.readlines()
    # open commands.txt and read file content
    with open('commands.txt', 'r') as cmd_file:
        commands = cmd_file.readlines()

    # list containing the commands
    command_list = []
    # contains number of cores to use
    num_cores = int(proc_lines.pop(0))
    # contains number of processes
    num_processes = int(proc_lines.pop(0))
    # contains number of memory pages
    num_pages = int(cfg.pop(0))
    # process dict
    process_list = []

    # populate list of commands
    for command in commands:
        temp_list = []
        for cmd in command.split(" "):
            if cmd.isalpha():
                temp_list.append(cmd)
            else:
                temp_list.append(int(cmd))
        command_list.append(temp_list)

    print(command_list)

    # populate process_list
    proc_id = 1
    for process in proc_lines:
        # append tuple of id, ready time, and service time
        process_list.append((proc_id, int(process.split(" ")[0]), int(process.split(" ")[1].rstrip())))
        proc_id += 1

    # sort by ready time
    process_list.sort(key=lambda ready: ready[1])

    # close the files
    mem_config.close()
    proc_file.close()
    cmd_file.close()

    # create virtual memory object
    memory = VirtualMemory(num_pages)
    # create disc page object
    disc_page = DiscPages()
    # create output file
    output = open("output.txt", "w")
    # create list containing all threads
    thread_list = []
    # create clock thread
    t_clock = Clock()
    # create clock thread
    t_manager = Manager(memory, disc_page)
    # create scheduling thread
    t_sched = Scheduler(t_clock, thread_list, process_list, output, num_processes, num_cores)

    # start clock thread
    t_clock.start()
    # start vm manager thread
    t_manager.start()
    # start scheduler thread
    t_sched.start()

    # append threads to thread_list
    thread_list.append(t_clock)
    thread_list.append(t_manager)
    thread_list.append(t_sched)

    # create process threads
    t_sched.create_proc_thread()

    # print list of threads
    print(thread_list)

    # below is the end of the program
    # signal for clock and scheduler to stop running
    # join all threads
    for t in thread_list:
        t.set_terminate(True)
        t.join()

    # close output file
    output.close()
