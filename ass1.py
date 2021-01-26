import threading

def mergesort(arr: list):
    return None

if __name__ == '__main__':
    file = open('input.txt', mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    values = list()
    for i in range(len(lines)):
        values.append(int(lines[i].strip('\n')))
    thread = threading.Thread(target=mergesort)
    thread.join()