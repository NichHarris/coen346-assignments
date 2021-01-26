import threading

def mergesort(arr: list):
    return None

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        lines = file.readlines()
    file.close()

    values = []
    for i in range(len(lines)):
        values.append(int(lines[i].strip('\n')))
    thread = threading.Thread(target=mergesort(values))
    thread.start()
    thread.join()