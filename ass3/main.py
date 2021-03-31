# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulation

# import the necessary packages
from clock import Clock
from scheduler import Scheduler
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
    # list containing start time of each process
    ready_time = []
    # list containing the service time for each process
    service_time = []
    # process list
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

    # alternative approach below
    # # populate process ready and service time lists
    # for process in proc_lines:
    #     ready_time = int(process.split(" ")[0])
    #     service_time = int(process.split(" ")[1].rstrip())

    # populate process_list
    for process in proc_lines:
        # append tuple of ready time and service time
        process_list.append((int(process.split(" ")[0]), int(process.split(" ")[1].rstrip())))

    # sort the processes list by ready time in ascending order
    process_list.sort(key=lambda ready: ready[0])

    # close the files
    mem_config.close()
    proc_file.close()
    cmd_file.close()

    # create output file
    output = open("output.txt", "w")
    # create list containing all threads
    thread_list = []
    # create clock thread
    t_clock = Clock()
    # create scheduling thread
    t_sched = Scheduler()

    t_proc = None
    # start clock thread
    t_clock.start()
    # start scheduler thread
    t_sched.start()

    # append threads to thread_list
    thread_list.append(t_clock)
    thread_list.append(t_sched)

    # process_list index
    i = 0
    while True:
        times = process_list[i]
        r_time = times[0]
        serv_time = times[1]
        cur_time = int(t_clock.get_time())/1000
        if cur_time >= r_time:
            t_proc = Process(t_clock, output, i, r_time)
            t_proc.start()
            thread_list.append(t_proc)
            i += 1
        if len(process_list)-1 < i:
            break
        # current logic for terminating threads -> iz trash needs improvement
        # if len(thread_list) > 2:
        #     if serv_time >= cur_time - thread_list[i+1].get_start_time():
        #         t_proc.set_terminate(True)

    print(thread_list)
    # testing clock rounding
    print("\n{}".format(t_clock.get_time()))
    t_clock.wait(2)
    print("\n{}".format(t_clock.get_time()))

    # testing process thread
    # t_proc = Process(t_clock, output, 2, 0)
    # t_proc.start()
    # t_proc.print_to_file(2, "Poop")

    # below is the end of the program
    # signal for clock and scheduler to stop running
    # join all threads
    for t in thread_list:
        t.set_terminate(True)
        t.join()

    # close output file
    output.close()

    # # counter used to traverse each previously generated list for process specifications
    # counter = 0
    # # generate a Process object and add it to the list of processes
    # for user in user_dict:
    #     for i in range(0, user_dict[user]):
    #         processes.append(Process(user, i, ready_time[counter], service_time[counter]))
    #         counter += 1
    #
    # # sort the processes list by ready time in ascending order (to be used as a queue)
    # processes.sort(key=lambda x: x.ready_time, reverse=False)
    #
    # # run the scheduler
    # Scheduler(processes, quantum)
