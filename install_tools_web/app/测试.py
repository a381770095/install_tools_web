import threading
import time


def run(n):
    print("task",n)
    time.sleep(1)


if __name__ == '__main__':
    task_ls=[]
    for i in range(10):
        t = threading.Thread(target=run,args=(i,))
        t.setDaemon(True)
        task_ls.append(t)
    for task in task_ls:
        task.start()
        task.join()