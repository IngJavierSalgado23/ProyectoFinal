
import multiprocessing,Queue
from multiprocessing import Process
import time
def worker():
    p = multiprocessing.current_process()
    print ("Emepezando a trabajar", p.name, p.pid)
    time.sleep(10)
    print("Termino de trabajar",p.name,p.pid)


def principal():
    procesosA = []
    for n in range(0, 5):
        nuevo_proceso = Process(target=worker)
        procesosA.append(nuevo_proceso)
    for proceso in procesosA:
        proceso.start()
    for proceso in procesosA:
        proceso.join()
principal()
