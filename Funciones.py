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
import matplotlib.pyplot as plt
from graficaUso import *
from threading import Thread
import threading

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
        out = check_output("ps axo pmem,pcpu,user,pid,command", shell = True)
        log_Process(out)
        time.sleep(delay)
def sort(opcion):
    if(opcion == 1):
       # print("Sort CPU")
        log_Activity("Procesos ordenados por CPU\n")
        check_output("ps axo user,pcpu,command > /home/ingjaviersalgado23/CortarString.out ", shell=True)
        out = check_output("(head -n 1 /home/ingjaviersalgado23/CortarString.out && tail -n +3 /home/ingjaviersalgado23/CortarString.out | sort -nrk 2,2)",shell=True)
       # out = check_output("ps aux |sort -nrk 3,3", shell=True)
        log_Activity(out)
        print(out)
        return out
    elif (opcion == 2):
        #print("Sort Memory")
        log_Activity("Procesos ordenados por Memory\n")
        check_output("ps axo user,pmem,command > /home/ingjaviersalgado23/CortarString.out ", shell=True)
        out = check_output("(head -n 1 /home/ingjaviersalgado23/CortarString.out && tail -n +3  /home/ingjaviersalgado23/CortarString.out | sort -nrk 2,2)",shell = True)
        #out = check_output("ps aux --sort -rss", shell=True)
        log_Activity(out)
        print(out)
        return out
    elif (opcion == 3):
       # print("Sort by pid")
        log_Activity("Procesos ordenados por pid\n")
        check_output("ps axo command,pid,user > /home/ingjaviersalgado23/CortarString.out ", shell=True)
        out = check_output("(head -n 1 /home/ingjaviersalgado23/CortarString.out && tail -n +3  /home/ingjaviersalgado23/CortarString.out | sort -nrk 3,3)",shell = True)
        log_Activity(out)
        print(out)
        return out

def matar_proceso(opcion):

    try:

        os.kill(eval(opcion), signal.SIGKILL)
        matar_proceso = ("Se elimino exitosamente el proceso {0}").format(opcion)
        log_Activity(matar_proceso)
        print(matar_proceso)
    except:
        print("Error. No se pudo matar el proceso")
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
    f = open(log_full, 'a')
    f.write(definicion)
    f.close()
    ##Handler Salgado
    out = check_output(("du -h  '{0}' --block-size=mB | cut -d'M' -f1").format(log), shell= True)
    tam = eval(out)
    contador = eval(check_output("find /home/ingjaviersalgado23/crearLogs -type f | wc -l",shell = True))
    if(tam>(1*contador)):
        print("Rotating log")
        print(tam)
        check_output(("mv /home/ingjaviersalgado23/crearLogs/LogProcesos.log /home/ingjaviersalgado23/crearLogs/LogProcesos.log.{0}").format(contador),shell = True)
    # logger = logging.getLogger("Log Proyecto Final")
    # logger.setLevel(logging.INFO)
    # #handler = RotatingFileHandler(log_full, maxBytes=1073741824, backupCount=10)
    # handler = RotatingFileHandler(log_full, maxBytes=(1024*1024), backupCount=15)
    # logger.addHandler(handler)
    # logger.info(definicion)
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

    audioExt = [".3gp",".aa",".acc",".aax",".act",".aiff",".amr",".ape",".au",".awb",".dct",".dss",".dvf",".flac",".mp3",".msv",".raw",".wav"]
    videoExt = [".webm",".mkv", ".flv",".vob", ".ogv",".drc", ".gif",".gifv",".mng",".avi",".mov",".qt",".wmv",".yuv",".rm",".rmvb",".asf",".amv",".mp4"
                ,".m4p",".m4v",".mpg",".mp2",".mpeg",".m2v",".m4v",".svi",".3gp",".3g2",".mxf",".roq",".nsv",".f4p"]
    imageExt = [".jpeg",".jfif",".jpg",".gif",".bmp",".pgn",".svg"]
    for roots, dirs, files in os.walk("/home/ingjaviersalgado23"):
        for dir in dirs:
            # path= os.path.join(roots,dir)
            # out = (check_output(("du -h --max-depth=1 | sort -hr").format(path), shell=True))
            # print(path,out)
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
    map_por_folders()
    #grafica_de_memoria_usada(tamAudio,tamVideo,tamImage,tamApps)
def grafica_directorios():
    trace1 = go.Area(
        r=[77.5, 72.5, 70.0, 45.0, 22.5, 42.5, 40.0, 62.5],
        t=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'],
        name='11-14 m/s',
        marker=dict(
            color='rgb(106,81,163)'
        )
    )
    trace2 = go.Area(
        r=[57.49999999999999, 50.0, 45.0, 35.0, 20.0, 22.5, 37.5, 55.00000000000001],
        t=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'],
        name='8-11 m/s',
        marker=dict(
            color='rgb(158,154,200)'
        )
    )
    trace3 = go.Area(
        r=[40.0, 30.0, 30.0, 35.0, 7.5, 7.5, 32.5, 40.0],
        t=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'],
        name='5-8 m/s',
        marker=dict(
            color='rgb(203,201,226)'
        )
    )
    trace4 = go.Area(
        r=[20.0, 7.5, 15.0, 22.5, 2.5, 2.5, 12.5, 22.5],
        t=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'],
        name='< 5 m/s',
        marker=dict(
            color='rgb(242,240,247)'
        )
    )
    data = [trace1, trace2, trace3, trace4]
    layout = go.Layout(
        title='Wind Speed Distribution in Laurel, NE',
        font=dict(
            size=16
        ),
        legend=dict(
            font=dict(
                size=16
            )
        ),
        radialaxis=dict(
            ticksuffix='%'
        ),
        orientation=270
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='polar-area-chart')
def map_por_folders():
    lista = os.listdir("/home/ingjaviersalgado23/")
    listaPadre = []
    listaHijos = []
    diccionarioHijos = {}
    folders = {}
    for padre in lista:
        padreC = os.path.join("/home/ingjaviersalgado23/",padre)
        #print (padreC)
        if(os.path.isdir(padreC)):
            listaPadre.append(padreC)
    #print(listaPadre)
    print("Hijos y padres")
    for padre in listaPadre:
        out = check_output(("du -h  '{0}' --block-size=kB ").format(padre), shell = True) #Me imprime los hijos #Aqui puedo evaluar si son hijos
        tempoOut = out.splitlines()
        for i in range (len(tempoOut)-2):
            listaHijos2Generacion = []
            listaHijos2Generacion.append(tempoOut[i])
            #print("Hijo") #crear nodo de hijos, la ref de papa es el ultimo en la lista tempoOut=
            diccionarioHijos[tempoOut[len(tempoOut)-1]] = listaHijos2Generacion
        for archivo in tempoOut:
            #print(archivo)
            #time.sleep(5)
            listaHijos.append(archivo)
    print(listaHijos)
    for hijo in listaHijos:
        tempo = hijo.split()
        folders[tempo[1]] = tempo[0]
    print(folders)
    print(len(folders))
    print(diccionarioHijos)
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

def map_disk():
    mapea = Process(target=tipo_de_archivos)
    mapea.daemon = True
    mapea.start()
def grafica(opcion,qPid):

    datos = []
    if(opcion == 0):
        grafica = Thread(target=grafica_cpu, args=(datos,1,qPid))
        grafica.start()
    elif(opcion==1):
        grafica = Thread(target=grafica_cpu,args=(datos,2,qPid))
        grafica.start()

def grafica_cpu(datos,opcion,qPid):
    qPid.put(os.getpid())
    print("Graficando CPU")
    total = len(datos)
    while (True):
        for i in range(20):
            if(opcion == 1):
                check_output("ps axo pmem,pcpu> /home/ingjaviersalgado23/grafica.log", shell=True)
                check_output("tail -n +2 /home/ingjaviersalgado23/grafica.log > /home/ingjaviersalgado23/grafica2.log", shell=True)
                out = check_output("awk '{print $2}' /home/ingjaviersalgado23/grafica2.log ", shell=True)
                cpu = (out.splitlines())
            else:
                check_output("ps axo pmem,pcpu> /home/ingjaviersalgado23/grafica.log", shell=True)
                check_output("tail -n +2 /home/ingjaviersalgado23/grafica.log > /home/ingjaviersalgado23/grafica2.log", shell=True)
                out = check_output("awk '{print $1}' /home/ingjaviersalgado23/grafica2.log ", shell=True)
                cpu = (out.splitlines())
            for procesos in cpu:
                total+= eval(procesos)
            print(len(datos))
            datos.append(total)
            total = 0
        if(len(datos)>=100):
            # countdown= Process(target=refreshGraficaCPU, args=(os.getpid(),datos,opcion))
            # countdown.start()
            plt.plot(datos)
            if(opcion == 1):
                log_Activity("Datos por CPU")
                plt.ylabel("Uso de CPU")
            else:
                log_Activity("Datos por Memoria ")
                plt.ylabel("Uso de Memoria")
            for dato in datos:
                log_Activity(str(dato))
            plt.show()
            check_output("rm /home/ingjaviersalgado23/grafica.log ", shell=True)
            check_output("rm /home/ingjaviersalgado23/grafica2.log ", shell=True)
            time.sleep(10)
def refreshGraficaCPU(pid,datos,opcion):
    grafica_c = Process(target=grafica_cpu,args = (datos,opcion))
    print("Start Countdown")
    time.sleep(5)
    try:
        grafica_c.start()
        os.kill(pid, signal.SIGKILL)
        matar_proceso = ("Se elimino exitosamente el proceso {0}").format(pid)
        print(matar_proceso)
    except:
        print("Error. No se pudo matar el proceso")

