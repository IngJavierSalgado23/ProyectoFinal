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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from logging.handlers import RotatingFileHandler
_ntuple_diskusage = namedtuple('usage', 'total used free')
import matplotlib
from matplotlib.figure import Figure
from psutil import virtual_memory
from psutil import swap_memory
matplotlib.use('TkAgg')
from drawnow import drawnow
import Proceso
import cPickle
import pickle

def lista_de_Procesos(queue,queuePID,delay):
    queuePID.put(os.getpid())
    out = check_output("ps aux", shell= True)
    while(True):
        queue.put(out)
        time.sleep(delay)

def guarda_procesos(delay):
    while(True):
        out = check_output("date -u",shell = True)
        log_Process(out)
        out = check_output("ps axo pmem,pcpu,user,pid,command,nlwp", shell = True)
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
def crearProceso():
    run_Proceso = Process(target=procesoBasura)
    run_Proceso.daemon = True
    run_Proceso.start()
    print('Pid del programa', os.getpid())
def procesoBasura():
    print(('Pid del proceso creado {0}').format(os.getpid()))
    while(True):
        x = 0
        time.sleep(3600)

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
    # print(contador)
    # print(tam)
    if(tam>(500000000*contador)):
        print("Rotating log")
        print(tam)
        time.sleep(3600)
       # check_output(("mv /home/ingjaviersalgado23/crearLogs/LogProcesos.log /home/ingjaviersalgado23/crearLogs/LogProcesos.log.{0}").format(contador),shell = True)
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
    grafica_memoria2(porceAudio,porceVideo,porceImage,porceApps,porceFree,porceOther,tamAudio,tamVideo,tamImage,tamApps,tamOther,free,total)
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
def grafica_memoria2(porceAudio,porceVideo,porceImage,porceApps,porceFree,porceOther,tamAudio,tamVideo,tamImage,tamApps,tamOther,free,total):
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

def grafica(canvas_cpu,canvas_mem):
        grafica = Thread(target=grafica_salgado, args=(canvas_cpu,canvas_mem,))
        grafica.start()
        consigue_datos_Graficar = Thread(target=consigue_datos)
        consigue_datos_Graficar.start()




def grafica_salgado(canvascpu,canvasmem):
    x_cpu = []
    x_mem = []
    y_cpu=[]
    y_mem = []
    cont_cpu = 0
    cont_mem = 0
    global grafica_cpu
    global grafica_mem
    while True:
        canvas_cpu = FigureCanvasTkAgg(f_cpu, master=canvascpu)
        canvas_mem = FigureCanvasTkAgg(f_mem, master=canvasmem)
        total =0
        while(datos_grafica_cpu.empty() == False):
            total = datos_grafica_cpu.get()
        if (total != 0):
            grafica_cpu.axis((0, 360, 0, 200))
            grafica_cpu.set_title('Grafica de uso de cpu')
            grafica_cpu.set_xlabel('Tiempo')
            grafica_cpu.set_ylabel('Uso de CPU')
            y_cpu.append(total)
            cont_cpu+=1
            x_cpu.append(cont_cpu)
            grafica_cpu.plot(x_cpu,y_cpu)
            canvas_cpu.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            canvas_cpu._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
            total = 0
        while(datos_grafica_mem.empty() == False):
            total = datos_grafica_mem.get()
        if (total != 0):
            grafica_mem.axis((0, 360, 0, 100))
            grafica_mem.set_title('Grafica de uso de Memoria')
            grafica_mem.set_xlabel('Tiempo')
            grafica_mem.set_ylabel('Uso de Memoria')
            y_mem.append(total)
            cont_mem+=1
            x_mem.append(cont_mem)
            grafica_mem.plot(x_mem, y_mem)
            canvas_mem.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            canvas_mem._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        canvas_cpu.show()
        canvas_mem.show()
        time.sleep(5)
        canvas_mem.get_tk_widget().destroy()
        canvas_cpu.get_tk_widget().destroy()

        # canvas_cpu = FigureCanvasTkAgg(f_cpu, master=canvascpu)
        # canvas_mem = FigureCanvasTkAgg(f_mem, master=canvasmem)
        #canvas_mem.get_tk_widget().destroy()
        #canvas_cpu.get_tk_widget().destroy()
        if(len(y_cpu)>=360):
            print(y_cpu)
            #f_cpu.clear()
            grafica_cpu = f_cpu.add_subplot(111)
           # x_cpu.pop(0)
            #y_cpu.pop(0)
            del x_cpu[:]
            del y_cpu[:]
        if(len(y_mem)>=360):
            #f_mem.clear()
            grafica_mem = f_mem.add_subplot(111)
            #y_mem.pop(0)
            del x_mem[:]
            del y_mem[:]
            #x_mem.pop(0)

datos_grafica_cpu = Queue()
datos_grafica_mem = Queue()
f_cpu = Figure(figsize=(3, 3))
grafica_cpu = f_cpu.add_subplot(111)
f_mem = Figure(figsize=(3, 3))
grafica_mem = f_mem.add_subplot(111)

def consigue_datos():
    while (True):
        total = 0
        check_output("ps axo pmem,pcpu> /home/ingjaviersalgado23/grafica.log", shell=True)
        check_output("tail -n +2 /home/ingjaviersalgado23/grafica.log > /home/ingjaviersalgado23/grafica2.log", shell=True)
        out = check_output("awk '{print $2}' /home/ingjaviersalgado23/grafica2.log ", shell=True)
        cpu = (out.splitlines())
        for procesos in cpu:
            total += eval(procesos)
        if(total!=0):
            datos_grafica_cpu.put(total)
            total = 0
        check_output("ps axo pmem,pcpu> /home/ingjaviersalgado23/grafica.log", shell=True)
        check_output("tail -n +2 /home/ingjaviersalgado23/grafica.log > /home/ingjaviersalgado23/grafica2.log",
                     shell=True)
        out = check_output("awk '{print $1}' /home/ingjaviersalgado23/grafica2.log ", shell=True)
        mem = (out.splitlines())
        for procesos in mem:
            total += eval(procesos)
        if(total!=0):
            datos_grafica_mem.put(total)

def limpia_memoria():
    out = check_output("free -m", shell=True)
    print(out)
    clean_swap_memory()

def clean_swap_memory():
    #Necesito sudo

    check_output("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'", shell= True)
    check_output("swapoff -a", shell = True)
    check_output("swapon - a", shell = True)
    out = check_output("free -m", shell=True)
    print(out)
def grafica_memoria(opcion):
    memoria_fisica = virtual_memory()
    swap = swap_memory()
    memoria_virtual = swap.total + memoria_fisica.total;
    if(opcion == 1):
        labels = 'Memoria Usada', 'Memoria Libre'
        sizes = [memoria_fisica.used, memoria_fisica.free]
        plt.title('Memoria Fisica')
    else:
        labels = 'Memoria Usada', 'Memoria Libre'
        sizes = [swap.used, swap.free]
        plt.title('Memoria Swap')
    colors = ['yellowgreen', 'gold']
    explode = (0, 0.1, )  # only "explode" the 2nd slice (i.e. 'Hogs')
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.show()

def carlosGrafica(canvascpu,canvasmem):
    plt.ion()
    plt.figure("grafica",figsize =(10,10))
    x_cpu = []
    x_mem = []
    y_cpu=[]
    y_mem = []
    total= 0
    i=0
    while True:
        while i< 60:
            x_cpu.append(i)
            x_mem.append(i)
            check_output("ps axo pmem,pcpu> /home/ingjaviersalgado23/grafica.log", shell=True)
            check_output("tail -n +2 /home/ingjaviersalgado23/grafica.log > /home/ingjaviersalgado23/grafica2.log", shell=True)
            out = check_output("awk '{print $2}' /home/ingjaviersalgado23/grafica2.log ", shell=True)
            cpu = (out.splitlines())
            print("Cpu")
            for procesos in cpu:
                total += eval(procesos)
            y_cpu.append(total)
            check_output("ps axo pmem,pcpu> /home/ingjaviersalgado23/grafica.log", shell=True)
            check_output("tail -n +2 /home/ingjaviersalgado23/grafica.log > /home/ingjaviersalgado23/grafica2.log",
                         shell=True)
            out = check_output("awk '{print $1}' /home/ingjaviersalgado23/grafica2.log ", shell=True)
            mem = (out.splitlines())
            print("mem")
            for procesos in mem:
                total += eval(procesos)
            y_mem.append(total)
            total =0
            drawnow(lambda:muestra_grafica(x_cpu,y_cpu,1))
            plt.pause(1)
            i+=1
        i = 59 #Solo recorre un dato
        x_cpu.pop(59) #Saco el 59 porque x siempre va estar al final porque solo recorre de 1 en 1
        y_cpu.pop(0) #Saca el ultimo dato para volver a tener espacio de graficar
        x_mem.pop(59) #Saco el 59 porque x siempre va estar al final porque solo recorre de 1 en 1
        y_mem.pop(0) #Saca el ultimo dato para volver a tener espacio de graficar

def muestra_grafica (x,y,opcion):
    if(opcion ==1):
        plt.axis((0,60,0,200))
        plt.ylabel("Uso de cpu")
        plt.title("Grafica de cpu")
    else:
        plt.axis((0,60,0,100))
        plt.ylabel("Uso de memoria")
        plt.title("Grafica de memoria")
    plt.plot(x,y)
def intento(x,y,canvascpu):
    canvas_cpu = FigureCanvasTkAgg(f_cpu, master=canvascpu)
    grafica_cpu.axis((0, 60, 0, 200))
    grafica_cpu.set_title('Grafica de uso de cpu')
    grafica_cpu.set_xlabel('Tiempo')
    grafica_cpu.set_ylabel('Uso de CPU')
    grafica_cpu.plot(x, y)
    canvas_cpu.draw()
    pass
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
def leer_logs():
    log_full = "/home/ingjaviersalgado23/crearLogs/LogProcesos1000.log"
    contador = eval(check_output("find /home/ingjaviersalgado23/crearLogs -type f | wc -l",shell = True))
    out = check_output("awk '{print $1}' /home/ingjaviersalgado23/crearLogs/LogProcesos1000.log ", shell=True)
    mem = (out.splitlines())
    out = check_output("awk '{print $2}' /home/ingjaviersalgado23/crearLogs/LogProcesos1000.log ", shell=True)
    cpu = (out.splitlines())
    out = check_output("awk '{print $3}' /home/ingjaviersalgado23/crearLogs/LogProcesos1000.log", shell=True)
    user = (out.splitlines())
    out = check_output("awk '{print $4}' /home/ingjaviersalgado23/crearLogs/LogProcesos1000.log ", shell=True)
    pid = (out.splitlines())
    out = check_output("awk '{print $6}' /home/ingjaviersalgado23/crearLogs/LogProcesos1000.log ", shell=True)
    procesos = (out.splitlines())
    out = check_output("awk '{print $5}' /home/ingjaviersalgado23/crearLogs/LogProcesos1000.log ", shell=True)
    thread_count = (out.splitlines())
    for i in range(0,len(mem)):
        if(is_number(pid[i])):
            lista_procesos.append(Proceso(mem[i], cpu[i], user[i], pid[i], procesos[i], thread_count[i]))
    for process in lista_procesos:
        for dirProcess in dir_procesos:
            if(process.getComand() == dirProcess):
                tempo_proceso = dir_procesos[dirProcess]
                tempo_proceso.setMem(process.getMem())
                tempo_proceso.setCPU(process.getCPU())
                tempo_proceso.setThread(process.getThread())
                tempo_proceso.incCounter()
            else:
                dir_procesos[str(process.getCommand())] = process
dir_procesos = {}

lista_procesos = list()
def mapBoabab():
    thread_map_folders = Thread(target = runMapeo)
    thread_map_folders.start()
def runMapeo():
    check_output('baobab /home', shell = True)
def analizandoLogs():
    hacer_analisis()
    leer_analisis()
def hacer_analisis():
    url_log = "/home/ingjaviersalgado23/readLogs/"
    lista = os.listdir(url_log)
    for url in lista:
        url = ('{0}{1}').format(url_log,url)
        print(url)
        divide_and_conquer(url)
        break
def leer_analisis():
    global new_dir_procesos
    url_log = "/home/ingjaviersalgado23/Analisis/"
    lista = os.listdir(url_log)
    for url in lista:
        url = ('{0}{1}').format(url_log,url)
        load_file(url)
        print(url)
    for proceso in new_dir_procesos:
        proceso = new_dir_procesos[proceso]
        mem = (proceso.getMem() / proceso.getCounter())
        cpu = (proceso.getCPU() / proceso.getCounter())
        thread = (proceso.getThread() / proceso.getCounter())
        log_Process2(('{0}\t\t{1}\t\t{2}\t\t{3}\t\t{4}\t\t{6}\t\t{5}\n').format(proceso.getPID(), mem, cpu,
                                                                               proceso.getUser(), thread,
                                                                               proceso.getCommand(),
                                                                               proceso.getCounter()))
def log_Process2(definicion):
    global countF
    log = "/home/ingjaviersalgado23/crearLogs"
    log_full = ("/home/ingjaviersalgado23/crearLogs/AnalisisFinal{0}.log").format(countF)
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
def leer_logs(url):
    global countF
    lista_procesos = list()
    out = check_output(("awk '{print $1}' %s") % url, shell=True)
    mem = (out.splitlines())
    out = check_output(("awk '{print $2}' %s") % url, shell=True)
    cpu = (out.splitlines())
    out = check_output(("awk '{print $3}' %s") % url, shell=True)
    user = (out.splitlines())
    out = check_output(("awk '{print $4}' %s") % url, shell=True)
    pid = (out.splitlines())
    out = check_output(("awk '{print $5}' %s") % url, shell=True)
    procesos = (out.splitlines())
    out = check_output(("awk '{print $6}' %s") % url, shell=True)
    thread_count = (out.splitlines())
    print(len(mem))
    for i in range(0,len(mem)):
        if (is_number(mem[i]) == True and is_number(cpu[i]) == True and is_number(thread_count[i]) == True):
            new_proceso = Proceso(float(mem[i]),float(cpu[i]),user[i],pid[i],procesos[i],float(thread_count[i]))
            lista_procesos.append(new_proceso)
    print(len(lista_procesos))
    existe = False
    for process in lista_procesos:
        if(len(dir_procesos) ==0):
            dir_procesos[str(process.getCommand())] = process
        for dirProcess in dir_procesos:
            #print(process.getCommand(), dirProcess)
            if(process.getCommand() == dirProcess):

                mem = (process.getMem())
                cpu = (process.getCPU())
                thread = (process.getThread())
                #print(mem,cpu,thread)
                tempo_proceso = dir_procesos[dirProcess]
                tempo_proceso.setMem(float(mem))
                tempo_proceso.setCPU(float(cpu))
                tempo_proceso.setThread(float(thread))
                tempo_proceso.incCounter(1)
                existe= True
                break
            else:
                existe = False
        if(existe == False):
            dir_procesos[str(process.getCommand())] = process
    print(len(dir_procesos))
    for proceso in dir_procesos:
        proceso = dir_procesos[proceso]
        # mem = int(proceso.getMem())
        # cpu = int(proceso.getCPU())
        # thread = int(proceso.getThread())
        mem = (proceso.getMem()/proceso.getCounter())
        cpu = (proceso.getCPU()/proceso.getCounter())
        thread = (proceso.getThread()/proceso.getCounter())
        log_Process2(('{0}\t\t{1}\t\t{2}\t\t{3}\t\t{4}\t\t{6}\t\t{5}\n').format(proceso.getPID(),mem,cpu,
                                                                                         proceso.getUser(),thread,proceso.getCommand(),proceso.getCounter()))
    del mem
    del cpu
    del user
    del pid
    del procesos
    del thread_count
    del lista_procesos
    save_file()
    countF+=1
def divide_and_conquer(url):
    global countF
    print('Dividing')
    url = ('{0} log.log').format(url)
    print(url)
    #check_output(('split --bytes=250M {0}').format(url), shell = True)
    print('Division ended')
    url1 = '/home/ingjaviersalgado23/log.logaa' #Me genera los splits en el home y no en el folder
    url2 = '/home/ingjaviersalgado23/log.logab'
    url3 ='/home/ingjaviersalgado23/log.logac'
    leer_logs(url1)
    check_output(('rm {0}').format(url1), shell = True)
    countF +=1
    leer_logs(url2)
    check_output(('rm {0}').format(url2), shell = True)
    countF+=1
    leer_logs(url3)
    check_output(('rm {0}').format(url3), shell = True)
    countF+=1
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def save_file():
    global dir_procesos
    global countF
    print("Saving file")
    cPickle.dump(new_dir_procesos, open(('/home/ingjaviersalgado23/Analisis/analisisFinal{0}p1.p').format(countF), 'wb'))

def load_file(url):
    print("loading file")
    global new_dir_procesos
    tempo_dir_procesos= pickle.load(open(str('{0}').format(url),"rb"))
    print(len(tempo_dir_procesos))
    for process in tempo_dir_procesos:
        process = tempo_dir_procesos[process]
        if (len(new_dir_procesos) == 0):
            new_dir_procesos[process.getCommand()] = process
        for dirProcess in new_dir_procesos:
            # print(process.getCommand(), dirProcess)
            if (process.getCommand() == dirProcess):
                mem = (process.getMem())
                cpu = (process.getCPU())
                thread = (process.getThread())
                tempo_proceso = new_dir_procesos[dirProcess]
                tempo_proceso.setMem(float(mem))
                tempo_proceso.setCPU(float(cpu))
                tempo_proceso.setThread(float(thread))
                tempo_proceso.incCounter(float(process.getCounter()))
                existe = True
                break
            else:
                existe = False
        if (existe == False):
            new_dir_procesos[process.getCommand()] = process


dir_procesos = {}
new_dir_procesos = {}
countF = 0