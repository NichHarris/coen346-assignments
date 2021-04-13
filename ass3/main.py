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
from disk_pages import DiskPages
from virtual_memory import VirtualMemory
from command import Commands

# entrypoint of script execution
if __name__ == '__main__':

    # open memconfig.txt and read file content
    with open('memconfig.txt', 'r') as mem_config:
        m_cfg = mem_config.readlines()
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
    num_pages = int(m_cfg.pop(0))
    # process dict
    process_list = []

    # populate list of commands
    for command in commands:
        temp_list = []
        for cmd in command.split(" "):
            # if its a word else its a number
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

    # sort process list by ready time
    process_list.sort(key=lambda ready: ready[1])

    # close the input files
    mem_config.close()
    proc_file.close()
    cmd_file.close()

    # create disk page object
    disk_page = DiskPages()

    # create commands object
    cmd_obj = Commands(command_list)

    # create output file
    output = open("output.txt", "w")

    # create list containing all threads
    thread_list = []

    # create clock thread -> wait to start in the scheduler
    t_clock = Clock()

    # create virtual memory object
    memory = VirtualMemory(num_pages)

    # create a vm manager
    t_manager = Manager(memory, cmd_obj, t_clock, disk_page, output)
    # start vm manager thread
    t_manager.start()

    # create scheduling thread
    t_scheduler = Scheduler(t_manager, cmd_obj, t_clock, thread_list, process_list, output, num_cores)
    # start scheduler thread
    t_scheduler.start()

    # append threads to thread_list
    thread_list.append(t_clock)
    thread_list.append(t_manager)
    thread_list.append(t_scheduler)

    # create process threads
    t_scheduler.create_proc_thread()

    # below is the end of the program
    # print list of threads
    print(thread_list)

    # signal for clock and scheduler to stop running
    # join all threads
    for t in thread_list:
        t.set_terminate(True)
        t.join()

    # print virtual memory at end of execution
    print("Virtual Memory: ")
    print(memory.get_memory())

    # close output file
    output.close()
