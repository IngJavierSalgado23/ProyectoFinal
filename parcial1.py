#Notas. Faltan Graficas, con el metodo de memory-usage-dir puedo sacar cuanta memoria estan utilizando y utilizando una regla de 3 con el total de bytes de mi disco
#duro, obtenido por usage-disk, puedo sacar el porcentaje de memoria que agarrara cada path y graficarlos. Debo de saber que directorios hay en la computadora
# por lo cual estaba pensando en utilizar os.walk, guardar el string y cortarlo. Seguir intentando con esto en el segundo parcial.
import os
import signal
from multiprocessing import Queue
from multiprocessing import Process
import subprocess as sp
from subprocess import check_output
import time
from collections import namedtuple
_ntuple_diskusage = namedtuple('usage', 'total used free')

def lista_de_Procesos(queue,queuePID,delay):
    queuePID.put(os.getpid())
    out = check_output("ps aux", shell= True)
    while(True):
        queue.put(out)
        time.sleep(delay)

def sort(opcion):
    if(opcion == 1):
       # print("Sort CPU")
        log_Activity("Procesos ordenados por CPU\n")
        out = check_output("ps aux |sort -nrk 3,3", shell=True)
        log_Activity(out)
        return out
    elif (opcion == 2):
        #print("Sort Memory")
        log_Activity("Procesos ordenados por Memory\n")
        out = check_output("ps aux --sort -rss", shell=True)
        log_Activity(out)
        return out
    elif (opcion == 3):
       # print("Sort by pid")
        log_Activity("Procesos ordenados por pid\n")
        out = check_output("ps aux --sort -pid", shell=True)
        log_Activity(out)
        return out


def log_Activity(definicion):
    log = "/home/ingjaviersalgado23/crearLogs"
    log_full = "/home/ingjaviersalgado23/crearLogs/LogProyecto.txt"
    if(os.path.exists(log) and os.path.isfile("LogProyecto.txt")): #La segunda validacion no esta sirviendo como esperaba. Si existe directorio pero no archivo no entra aqui
        #print ("Existe el archivo")
        pass
    else:
        os.makedirs(log)
        file = open(log_full,'a')
        file.close()
        print("creando archivo")
    f = open(log_full, 'a')
    f.write(definicion)
    f.close()
def disk_usage(path):
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    res = ("Memoria consumida por el path {0}, total = {1}, used = {2}, free{3}").format(path,total,used,free)
    log_Activity(res)
    return _ntuple_diskusage(total, used, free)

def disk_usage_general():
    out = check_output("df -h", shell=True)
    res = ("Estado General del disco duro\n {0}").format(out)
    log_Activity(res)
    print(out)
def memory_usage_of_directories(path):
    nuevo_path = ("du -h {0}").format(path)
    out = check_output(nuevo_path, shell=True)
    res = ("Consumo de memoria por el directorio {0}\n {1}").format(path,out)
    print(res)
    log_Activity(res)
def main():
    procesos_corriendo_PID = Queue()
    procesos_corriendo = Queue()
    delay = 3
    consigue_Procesos = Process(target = lista_de_Procesos,args = (procesos_corriendo,procesos_corriendo_PID,delay))
    consigue_Procesos.daemon = True
    consigue_Procesos.start()
    if(not procesos_corriendo.empty()):
        print("Por lo menos entre aqui?")
        procesos = procesos_corriendo.get()
    PID_procesos = procesos_corriendo_PID.get()
    print("Pid del proceso que consigue de manera continua los procesos del ordenador  = {0}").format(PID_procesos)
    print("Pid del proceso del programa = {0}").format(os.getpid())
    pregunta = str(raw_input("Desea ver los procesos corriendo?, Y para mostrar o N para continuar")).upper()
    if( pregunta =="Y" ):
        while(True):
            opcion = eval(raw_input("De que forma quiere visualizarlos?. 1 = Uso de CPU. 2= Uso de memoria 3 = PID. 4 = Continuar"))
            if(opcion == 1):
                print(sort(1))
            elif (opcion == 2):
                print(sort(2))
            elif (opcion == 3):
                print(sort(3))
            elif(opcion == 4):
                print("Entro en 4")
                break
            else:
                print("Entrada no valida")

    pregunta = str(raw_input("Desea matar un proceso?, Y para matar o N para continuar")).upper()
    if(pregunta == "Y"):
        while(True):
            opcion = eval(raw_input("Introduzca el pid del proceso que quiere matar"))
            try:
                os.kill(opcion,signal.SIGKILL)
                matar_proceso = ("Se elimino exitosamente el proceso {0}").format(opcion)
                log_Activity(matar_proceso)
                print(matar_proceso)
                pregunta = str(raw_input("Desea matar otro proceso?, Y para matar o N para continuar")).upper()
                if(pregunta != "Y"):
                    break
            except:
                print("Error. No se pudo matar el proceso")
                break
    pregunta = str(raw_input("Desea ver el estado del disco duro?, Y para ver estado del disco duro o N para continuar")).upper()
    if (pregunta == "Y"):
        disk_usage_general()
        print(disk_usage("/"))

        pregunta = str(raw_input("Desea ver la memoria dedicada a un path en especifico?, Y para visualizar o N para continuar")).upper()
        if(pregunta == "Y"):
            while (True):
                path = str(raw_input("Introduzca el path que quiera visualizar"))
                try:
                    memory_usage_of_directories(path)
                except:
                    print("Error. El path que introdujo no existe")
                pregunta = str(raw_input("Desea visualizar otro path? Y para visualizar o N para continuar")).upper()
                if(pregunta != "Y"):
                    break
main()