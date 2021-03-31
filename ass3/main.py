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
    # process dict
    process_dict = {}

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

    # populate process_dict
    id = 1
    for process in proc_lines:
        # key of process ready time and value tuple of service time and process id
        process_dict[id] = (int(process.split(" ")[0]), int(process.split(" ")[1].rstrip()))
        id += 1

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

    # this will probably need to be done in the scheduler -> FIFO
    # process thread creation
    while True:
        # starting a process thread
        proc_id = 1
        temp = 1
        while len(process_dict) != 0:
            cur_time = int(t_clock.get_time()/1000)
            for i in process_dict.copy():
                tup = process_dict[i]
                if tup[0] == cur_time:
                    t_proc = Process(t_clock, output, i, tup[0], tup[1])
                    t_proc.start()
                    thread_list.append(t_proc)
                    proc_id = i
                    break
            process_dict.pop(proc_id)

        # using this to break right now, eventually we want to break when theres no commands left
        if len(thread_list) == num_processes + 2:
            break

    # # process thread creation
    # while True:
    #     cur_time = int(t_clock.get_time()/1000)
    #     # starting a process thread
    #     if cur_time in process_dict:
    #         tup = process_dict[cur_time]
    #         t_proc = Process(t_clock, output, tup[1], cur_time, tup[0])
    #         t_proc.start()
    #         thread_list.append(t_proc)
    #         process_dict.pop(cur_time)
    #
    #     # using this to break right now, eventually we want to break when theres no commands left
    #     if len(thread_list) == num_processes + 2:
    #         break


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
