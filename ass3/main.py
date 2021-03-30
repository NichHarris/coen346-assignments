# COEN 346 - Lab Assignment #3
#
# Matthew Sklivas 40095150
# Nicholas Harris 40111093
# Benjamin Grant 40059608
#
# Virtual Memory Management Simulation

# import the necessary packages

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

    # dictionary containing the commands
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

    # populate list of commands
    for command in commands:
        temp_list = []
        for cmd in command.split(" "):
            if cmd.isalpha():
                temp_list.append(cmd)
            else:
                temp_list.append(int(cmd))

        command_list.append(temp_list)

    # populate process ready and service time lists
    for process in proc_lines:
        ready_time = int(process.split(" ")[0])
        service_time = int(process.split(" ")[1].rstrip())

    # close the files
    mem_config.close()
    proc_file.close()
    cmd_file.close()

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
