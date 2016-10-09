#Notas. Faltan Graficas, con el metodo de memory-usage-dir puedo sacar cuanta memoria estan utilizando y utilizando una regla de 3 con el total de bytes de mi disco
#duro, obtenido por usage-disk, puedo sacar el porcentaje de memoria que agarrara cada path y graficarlos. Debo de saber que directorios hay en la computadora
# por lo cual estaba pensando en utilizar os.walk, guardar el string y cortarlo. Seguir intentando con esto en el segundo parcial.
#En el os.walk que ya tengo guardar los directorios en una lista. Despues correr un os.walk en cada directorio si quiero saber los archivos qu ehay en cada uno
#Teniendo los directorios or os.walk puedo usar la funcion del path de memoria en cada directorio y graficarlos.
import os
import signal
from multiprocessing import Queue
from multiprocessing import Process
import subprocess as sp
from subprocess import check_output
import time
from collections import namedtuple
import logging
import plotly.plotly as py
import plotly.graph_objs as go
from Tkinter import *

from logging.handlers import RotatingFileHandler
_ntuple_diskusage = namedtuple('usage', 'total used free')

def lista_de_Procesos(queue,queuePID,delay):
    queuePID.put(os.getpid())
    out = check_output("ps aux", shell= True)
    while(True):
        queue.put(out)
        time.sleep(delay)

def guarda_procesos(delay):
    while(True):
        log_Process("Nueva Lista de Procesos")
        out = check_output("ps axo command,pmem,pcpu,user", shell = True)
        log_Process(out)
        time.sleep(delay)
def sort(opcion):
    if(opcion == 1):
       # print("Sort CPU")
        log_Activity("Procesos ordenados por CPU\n")
        check_output("ps axo command,user,pcpu > /home/ingjaviersalgado23/CortarString.out ", shell=True)
        out = check_output("(head -n 1 /home/ingjaviersalgado23/CortarString.out && tail -n +3  /home/ingjaviersalgado23/CortarString.out | sort -nrk 2,2)",
        shell=True)
       # out = check_output("ps aux |sort -nrk 3,3", shell=True)
        log_Activity(out)
        return out
    elif (opcion == 2):
        #print("Sort Memory")
        log_Activity("Procesos ordenados por Memory\n")
        check_output("ps axo command,user,pmem > /home/ingjaviersalgado23/CortarString.out ", shell=True)
        out = check_output("(head -n 1 /home/ingjaviersalgado23/CortarString.out && tail -n +3  /home/ingjaviersalgado23/CortarString.out | sort -nrk 2,2)",shell = True)
        #out = check_output("ps aux --sort -rss", shell=True)
        log_Activity(out)
        return out
    elif (opcion == 3):
       # print("Sort by pid")
        log_Activity("Procesos ordenados por pid\n")
        #out = check_output("ps axo user,pcpu | sort -nrk 2,2", shell=True)
        check_output("ps axo command,pid,user > /home/ingjaviersalgado23/CortarString.out ", shell=True)
        out = check_output("(head -n 1 /home/ingjaviersalgado23/CortarString.out && tail -n +3  /home/ingjaviersalgado23/CortarString.out | sort -nrk 2,2)",shell = True)
        #out = check_output("ps axo user,pcpu, | sort -nrk 1,2", shell=True)
        log_Activity(out)
        return out


def log_Activity(definicion):
    log = "/home/ingjaviersalgado23/crearLogs"
    log_full = "/home/ingjaviersalgado23/crearLogs/LogProyecto.log"
    if(os.path.exists(log)):
        #print ("Existe el archivo")
        pass
    else:
        os.makedirs(log)
        file = open(log_full,'a')
        file.close()
        print("creando archivo")

    logger = logging.getLogger("Log Proyecto Final")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(log_full, maxBytes=1000000000,backupCount=1)
    logger.addHandler(handler)
    logger.info(definicion)
def log_Process(definicion):
    log = "/home/ingjaviersalgado23/crearLogs"
    log_full = "/home/ingjaviersalgado23/crearLogs/LogProcesos.log"
    if (os.path.exists(log)):
        # print ("Existe el archivo")
        pass
    else:
        os.makedirs(log)
        file = open(log_full, 'a')
        file.close()
        print("creando archivo")

    logger = logging.getLogger("Log Proyecto Final")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(log_full, maxBytes=1000000, backupCount=100)
    logger.addHandler(handler)
    logger.info(definicion)
def disk_usage(path):
    st = os.statvfs(path)
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    free = total - used
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
def tipo_de_archivos():
    #Idea brindada por el Equipo de Raul, Allan y Jorge
    #Usar el comando find ocupa permiso de administrador y no encuentra los archivos ocultos.
    res = ("Mapeando el disco duro. Por favor espere.\n")
    print(res)
    log_Activity(res)
    contAudioF= 0
    contImageF = 0
    contVideoF = 0
    contShellF = 0
    contFiles = 0
    tamOther = 0
    contDirs = 0
    tamAudio = 0
    tamImage = 0
    tamVideo = 0
    tamApps = 0
    contApps = 0
    ja = "Hola"
    sa = "Hola"

    audioExt = [".3gp",".aa",".acc",".aax",".act",".aiff",".amr",".ape",".au",".awb",".dct",".dss",".dvf",".flac",".mp3",".msv",".raw",".wav"]
    videoExt = [".webm",".mkv", ".flv",".vob", ".ogv",".drc", ".gif",".gifv",".mng",".avi",".mov",".qt",".wmv",".yuv",".rm",".rmvb",".asf",".amv",".mp4"
                ,".m4p",".m4v",".mpg",".mp2",".mpeg",".m2v",".m4v",".svi",".3gp",".3g2",".mxf",".roq",".nsv",".f4p"]
    imageExt = [".jpeg",".jfif",".jpg",".gif",".bmp",".pgn",".svg"]
    for roots, dirs, files in os.walk("/"):
        for dir in dirs:
            contDirs +=1
        for name in files:
            if (name.endswith(tuple(audioExt))):
                path = os.path.join(roots, name)
                contAudioF+=1
                tamAudio += eval(check_output(("du -h  '{0}' --block-size=kB | cut -d'k' -f1").format(path),shell=True))
            elif (name.endswith(tuple(videoExt))):
                path = os.path.join(roots, name)
                contVideoF +=1
                tamVideo += eval(check_output(("du -h  '{0}' --block-size=kB | cut -d'k' -f1").format(path),shell=True))
            elif(name.endswith(tuple(imageExt))):
                path = os.path.join(roots, name)
                contImageF+=1
                tamImage += eval(check_output(("du -h  '{0}' --block-size=kB | cut -d'k' -f1").format(path),shell=True))
            elif(name.endswith(tuple(".sh"))):
                path = os.path.join(roots, name)
                contShellF +=1
            elif(roots=="/usr/share/applications"):
                path = os.path.join(roots, name)
                contApps+=1
                tamApps += eval(check_output(("du -h  '{0}' --block-size=kB | cut -d'k' -f1").format(path),shell=True))
            contFiles +=1

    res = ("Total de directorios =  {0}\n").format(contDirs)
    print(res)
    log_Activity(res)
    res= ("Total de archivos de video = {0}, Tamano total de archivos de video {1}kB\n").format( contVideoF,tamVideo)
    print(res)
    log_Activity(res)
    res =("Total de archivos de imagen = {0}, Tamano total de archivos de imagen {1}kB\n").format( contImageF,tamImage)
    print(res)
    log_Activity(res)
    res = ("Total de archivos de audio = {0}, Tamano total de archivos de audio {1}kB\n").format(contAudioF,tamAudio)
    print(res)
    log_Activity(res)
    res = ("Total de apps = {0}, Tamano total de las apps {1}kB\n").format(contApps,tamApps)
    print(res)
    log_Activity(res)
    res = ("Total de archivos de shell = {0}\n").format(contShellF)
    print(res)
    log_Activity(res)
    res = ("Total de archivos = {0}\n").format(contFiles)
    print(res)
    log_Activity(res)
    st = os.statvfs("/")
    total = (st.f_blocks * st.f_frsize)/1000
    used = ((st.f_blocks - st.f_bfree) * st.f_frsize)/1000
    free = total-used
    porceAudio = float(tamAudio*100)/total
    porceVideo = float(tamVideo*100)/total
    porceImage = float(tamImage*100)/total
    porceFree = float(free*100)/total
    porceUsed = float(used*100)/total
    porceApps = float(tamApps*100)/ total
    porceOther = float(porceUsed-(porceAudio+porceVideo+porceImage+porceApps))
    tamOther = float(used-(tamVideo+tamAudio+tamImage+tamApps))
    print(porceAudio)
    print(porceVideo)
    print(porceImage)
    print(porceApps)
    print(porceFree)
    print(porceOther)
    print(tamApps)
    grafica_memoria(porceAudio,porceVideo,porceImage,porceApps,porceFree,porceOther,tamAudio,tamVideo,tamImage,tamApps,tamOther,free,total)
    #grafica_de_memoria_usada(tamAudio,tamVideo,tamImage,tamApps)
def grafica_memoria(porceAudio,porceVideo,porceImage,porceApps,porceFree,porceOther,tamAudio,tamVideo,tamImage,tamApps,tamOther,free,total):
    # tamAudio = kilobyte_a_GigaByte(tamAudio)
    # tamVideo = kilobyte_a_GigaByte(tamVideo)
    # tamImage = kilobyte_a_GigaByte(tamImage)
    # tamApps = kilobyte_a_GigaByte(tamApps)
    # tamOther = kilobyte_a_GigaByte(tamOther)
    # free = kilobyte_a_GigaByte(free)

    trace1 = go.Bar(
        y=[('Disco = {0}kB').format(total)],
        x=[porceAudio],
        name=('Archivos de Audio {0}kB').format(tamAudio),
        orientation='h',
        marker=dict(
            color='rgba(153, 153, 0, 1)',
            line=dict(
                color='rgba(246, 78, 139, 1.0)',
                width=3)
        )
    )
    trace2 = go.Bar(
        y=[('Disco = {0}kB').format(total)],
        x=[porceVideo],
        name=('Archivos de Video {0}kB').format(tamVideo),
        orientation='h',
        marker=dict(
            color='rgba(0, 255, 0, 0.8)',
            line=dict(
                color='rgba(58, 71, 80, 1.0)',
                width=3)
        )
    )
    trace3 = go.Bar(
        y=[('Disco = {0}kB').format(total)],
        x=[porceImage],
        name=('Imagenes {0}kB').format(tamImage),
        orientation='h',
        marker=dict(
            color='rgba(0, 255, 255, 0.8)',
            line=dict(
                color='rgba(58, 71, 80, 1.0)',
                width=3)
        )
    )
    trace4 = go.Bar(
        y=[('Disco = {0}kB').format(total)],
        x=[porceApps],
        name=('Applicaciones {0}kB').format(tamApps),
        orientation='h',
        marker=dict(
            color='rgba(0, 0, 255, 0.8)',
            line=dict(
                color='rgba(58, 71, 80, 1.0)',
                width=3)
        )
    )
    trace5 = go.Bar(
        y=[('Disco = {0}kB').format(total)],
        x=[porceOther],
        name=('Otros Archivos {0}kB').format(tamOther),
        orientation='h',
        marker=dict(
            color='rgba(255, 153, 51, 0.8)',
            line=dict(
                color='rgba(58, 71, 80, 1.0)',
                width=3)
        )
    )
    trace6 = go.Bar(
        y=[('Disco = {0}kB').format(total)],
        x=[porceFree],
        name=('Espacio Libre {0}kB').format(free),
        orientation='h',
        marker=dict(
            color='rgba(224, 224, 224, 0.8)',
            line=dict(
                color='rgba(58, 71, 80, 1.0)',
                width=3)
        )
    )

    data = [trace1, trace2, trace3, trace4,trace5,trace6]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='marker-h-bar')
def kilobyte_a_GigaByte(num):
    num = float(num/1000000)
    return num



def grafica_de_memoria_usada(tamAudio,tamVideo,tamImage,tamApps):
    trace1 = go.Bar(
        y=['Mapeo del disco'],
        x=[tamAudio],
        name=('Archivos de Audio {0}kB').format(tamAudio),
        orientation='h',
        marker=dict(
            color='rgba(153, 153, 0, 1)',
            line=dict(
                color='rgba(246, 78, 139, 1.0)',
                width=3)
        )
    )
    trace2 = go.Bar(
        y=['Mapeo del disco'],
        x=[tamVideo],
        name=('Archivos de Video{0}kB').format(tamVideo),
        orientation='h',
        marker=dict(
            color='rgba(0, 255, 0, 0.8)',
            line=dict(
                color='rgba(58, 71, 80, 1.0)',
                width=3)
        )
    )
    trace3 = go.Bar(
        y=['Mapeo del disco'],
        x=[tamImage],
        name=('Imagenes {0}kB').format(tamImage),
        orientation='h',
        marker=dict(
            color='rgba(0, 255, 255, 0.8)',
            line=dict(
                color='rgba(58, 71, 80, 1.0)',
                width=3)
        )
    )
    trace4 = go.Bar(
        y=['Mapeo del disco'],
        x=[tamApps],
        name=('Applicaciones {0}kB').format(tamApps),
        orientation='h',
        marker=dict(
            color='rgba(0, 0, 255, 0.8)',
            line=dict(
                color='rgba(58, 71, 80, 1.0)',
                width=3)
        )
    )

    data = [trace1, trace2,trace3,trace4]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='marker-h-bar')

root = Tk()                             #main window
root.title("Salgado")
btnMap = Button(root, text = 'Mapea al disco duro', command = tipo_de_archivos)
btnMap.pack(pady=20, padx = 20)
root.mainloop()
delay = 1
consigue_Procesos = Process(target =guarda_procesos,args = (delay,))
consigue_Procesos.daemon = True
consigue_Procesos.start()

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
    tipo_de_archivos()
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
