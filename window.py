import Tkinter as tk
import ttk
from Tkinter import *
from Funciones import *
from multiprocessing import Process
import traceback

from threading import Thread
def click_derecho(event):
    print("Proceso a matar")
    try:
        for item in tree.selection():
            item_text = tree.item(item, "values")
            pid = (item_text[4])
            print pid
        matar_proceso(pid)
        lee_procesos_log(1,True)
    except:
        print("Opcion no valida")
        print(traceback.format_exc())

def refresh_gui():
    opcion = 1
    while(True):
        while(queue_opcion.empty() == False):
            opcion = queue_opcion.get()
        #print(opcion)
        lee_procesos_log(opcion,True)
        time.sleep(5)


def lee_procesos_log(opcion,hijo):
    if(hijo):
        pass
    else:
        queue_opcion.put(opcion)
    check_output("ps axo pmem,pcpu,user,pid,nlwp,command> /home/ingjaviersalgado23/tempo.log", shell=True)
    if (opcion == 1): #Ordenar por memoria
        check_output("head -n 1 /home/ingjaviersalgado23/tempo.log > /home/ingjaviersalgado23/tempo2.log",shell=True)
        check_output("tail -n +2 /home/ingjaviersalgado23/tempo.log | sort -nrk 1,1 >> /home/ingjaviersalgado23/tempo2.log",shell=True)
        out = check_output("awk '{print $1}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        mem = (out.splitlines())
        out = check_output("awk '{print $2}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        cpu = (out.splitlines())
        out = check_output("awk '{print $3}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        user = (out.splitlines())
        out = check_output("awk '{print $4}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        pid = (out.splitlines())
        out = check_output("awk '{print $6}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        procesos = (out.splitlines())
        out = check_output("awk '{print $5}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        thread_count = (out.splitlines())
    elif (opcion ==2): #CPU
        check_output("head -n 1 /home/ingjaviersalgado23/tempo.log > /home/ingjaviersalgado23/tempo2.log",shell=True)
        check_output("tail -n +2 /home/ingjaviersalgado23/tempo.log | sort -nrk 2,2 >> /home/ingjaviersalgado23/tempo2.log",shell=True)
        out = check_output("awk '{print $1}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        mem = (out.splitlines())
        out = check_output("awk '{print $2}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        cpu = (out.splitlines())
        out = check_output("awk '{print $3}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        user = (out.splitlines())
        out = check_output("awk '{print $4}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        pid = (out.splitlines())
        out = check_output("awk '{print $6}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        procesos = (out.splitlines())
        out = check_output("awk '{print $5}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        thread_count = (out.splitlines())
    elif(opcion ==3): #PID
        check_output("head -n 1 /home/ingjaviersalgado23/tempo.log > /home/ingjaviersalgado23/tempo2.log",shell=True)
        check_output("tail -n +2 /home/ingjaviersalgado23/tempo.log | sort -nrk 4,4 >> /home/ingjaviersalgado23/tempo2.log",shell=True)
        out = check_output("awk '{print $1}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        mem = (out.splitlines())
        out = check_output("awk '{print $2}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        cpu = (out.splitlines())
        out = check_output("awk '{print $3}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        user = (out.splitlines())
        out = check_output("awk '{print $4}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        pid = (out.splitlines())
        out = check_output("awk '{print $6}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        procesos = (out.splitlines())
        out = check_output("awk '{print $5}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        thread_count = (out.splitlines())
    elif (opcion == 4): #User
        check_output("head -n 1 /home/ingjaviersalgado23/tempo.log > /home/ingjaviersalgado23/tempo2.log", shell=True)
        check_output(
            "tail -n +2 /home/ingjaviersalgado23/tempo.log | sort -drk 3,3 >> /home/ingjaviersalgado23/tempo2.log",
            shell=True)
        out = check_output("awk '{print $1}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        mem = (out.splitlines())
        out = check_output("awk '{print $2}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        cpu = (out.splitlines())
        out = check_output("awk '{print $3}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        user = (out.splitlines())
        out = check_output("awk '{print $4}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        pid = (out.splitlines())
        out = check_output("awk '{print $6}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        procesos = (out.splitlines())
        out = check_output("awk '{print $5}' /home/ingjaviersalgado23/tempo.log ", shell=True)
        thread_count = (out.splitlines())
    elif (opcion == 5): #Command
        check_output("head -n 1 /home/ingjaviersalgado23/tempo.log > /home/ingjaviersalgado23/tempo2.log", shell=True)
        check_output(
            "tail -n +2 /home/ingjaviersalgado23/tempo.log | sort -drk 6,6 >> /home/ingjaviersalgado23/tempo2.log",
            shell=True)
        out = check_output("awk '{print $1}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        mem = (out.splitlines())
        out = check_output("awk '{print $2}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        cpu = (out.splitlines())
        out = check_output("awk '{print $3}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        user = (out.splitlines())
        out = check_output("awk '{print $4}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        pid = (out.splitlines())
        out = check_output("awk '{print $6}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        procesos = (out.splitlines())
        out = check_output("awk '{print $5}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        thread_count = (out.splitlines())
    elif (opcion == 6): #Thread count
        print("NLWP")
        check_output("head -n 1 /home/ingjaviersalgado23/tempo.log > /home/ingjaviersalgado23/tempo2.log", shell=True)
        check_output(
            "tail -n +2 /home/ingjaviersalgado23/tempo.log | sort -nrk 5,5 >> /home/ingjaviersalgado23/tempo2.log",
            shell=True)
        out = check_output("awk '{print $1}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        mem = (out.splitlines())
        out = check_output("awk '{print $2}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        cpu = (out.splitlines())
        out = check_output("awk '{print $3}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        user = (out.splitlines())
        out = check_output("awk '{print $4}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        pid = (out.splitlines())
        out = check_output("awk '{print $6}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        procesos = (out.splitlines())
        out = check_output("awk '{print $5}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        thread_count = (out.splitlines())
    repaint(procesos,user,mem,cpu,pid,thread_count)

def lee_procesos_log2(opcion):
    print('Sorting Recommendations', opcion)
    #Se puede optimizar todo este codigo y practicamente eliminarlo y anexarlo al de arriba con otro argumento. si hay tiempo corregirlo
    url = '/home/ingjaviersalgado23/crearLogs/AnalisisFinal0.log '
    if (opcion == 1):  # Ordenar por PID
        check_output(("head -n 1 {0} > /home/ingjaviersalgado23/tempo3.log").format(url),shell=True)
        check_output(("tail -n +2 {0} | sort -nrk 1,1 >> /home/ingjaviersalgado23/tempo3.log").format(url),shell=True)
        # check_output(
        #     ("tail  -n +0 {0} | sort -nrk 1,1 > /home/ingjaviersalgado23/tempo3.log").format(url),
         #   shell=True)
    elif (opcion == 2):  # Memoria
        check_output(("head -n 1 {0} > /home/ingjaviersalgado23/tempo3.log").format(url),shell=True)
        check_output(("tail -n +2 {0} | sort -nrk 2,2 >> /home/ingjaviersalgado23/tempo3.log").format(url),shell=True)
    elif (opcion == 3):  # CPU
        check_output(("head -n 1 {0} > /home/ingjaviersalgado23/tempo3.log").format(url),shell=True)
        check_output(("tail -n +2 {0} | sort -nrk 3,3 >> /home/ingjaviersalgado23/tempo3.log").format(url),shell=True)

    elif (opcion == 4):  # User
        check_output(("head -n 1 {0} > /home/ingjaviersalgado23/tempo3.log").format(url),shell=True)
        check_output(("tail -n +2 {0} | sort -nrk 4,4 >> /home/ingjaviersalgado23/tempo3.log").format(url),shell=True)
    elif (opcion == 5):  # Thread
        check_output(("head -n 1 {0} > /home/ingjaviersalgado23/tempo3.log").format(url),shell=True)
        check_output(("tail -n +2 {0} | sort -nrk 5,5 >> /home/ingjaviersalgado23/tempo3.log").format(url),shell=True)
    elif (opcion == 6):  # Counter
        check_output(("head -n 1 {0} > /home/ingjaviersalgado23/tempo3.log").format(url),shell=True)
        check_output(("tail -n +2 {0} | sort -nrk 6,6 >> /home/ingjaviersalgado23/tempo3.log").format(url),shell=True)
    elif(opcion == 7): #Procesos
        check_output(("head -n 1 {0} > /home/ingjaviersalgado23/tempo3.log").format(url),shell=True)
        check_output(("tail -n +2 {0} | sort -nrk 7,7 >> /home/ingjaviersalgado23/tempo3.log").format(url),shell=True)
    out = check_output("awk '{print $1}' /home/ingjaviersalgado23/tempo3.log ", shell=True)
    pid = (out.splitlines())
    out = check_output("awk '{print $2}' /home/ingjaviersalgado23/tempo3.log ", shell=True)
    mem = (out.splitlines())
    out = check_output("awk '{print $3}' /home/ingjaviersalgado23/tempo3.log ", shell=True)
    cpu = (out.splitlines())
    out = check_output("awk '{print $4}' /home/ingjaviersalgado23/tempo3.log ", shell=True)
    user = (out.splitlines())
    out = check_output("awk '{print $5}' /home/ingjaviersalgado23/tempo3.log ", shell=True)
    thread_count = (out.splitlines())
    out = check_output("awk '{print $6}' /home/ingjaviersalgado23/tempo3.log ", shell=True)
    counter = (out.splitlines())
    out = check_output("awk '{print $7}' /home/ingjaviersalgado23/tempo3.log ", shell=True)
    procesos= (out.splitlines())

    repaint2(procesos, user, mem, cpu, pid, thread_count,counter)

def repaint(procesos,user,mem,cpu,pid,thread_count):
    global label_thread_count
    global label_procesos_count
    thread_count_l = 0
    for i in tree.get_children():
        tree.delete(i)
    for i in range(1, len(mem) - 1):
        thread_count_l+=int(thread_count[i])
        tree.insert("", "end", text=procesos[i], values=("", user[i], mem[i], cpu[i], pid[i],thread_count[i]))
    print("Refresh")
    label_thread_count.config(text=("Total de Threads Corriendo = {0}").format(thread_count_l))
    label_procesos_count.config(text=("Total de Procesos Corriendo = {0}").format(len(mem)))
    memoria_fisica = virtual_memory()
    label_Memoria_Fisica.config(text =("Total de Memoria Fisica = {0} mB").format(memoria_fisica.total / (1024 * 1024)))
    swap = swap_memory()
    memoria_virtual = swap.total + memoria_fisica.total;
    label_Memoria_Virtual.config(text=("Total de Memoria Virtaul = {0} mB").format(memoria_virtual / (1024 * 1024)))
    label_Memoria_cache.config(text=('Memoria Cache = {0} mB').format(memoria_fisica.cached/(1024*1024)))
def repaint2(procesos,user,mem,cpu,pid,thread_count,counter):
    for i in treeR.get_children():
        treeR.delete(i)
    for i in range(1, len(mem) - 1):
        treeR.insert("", "end", text=procesos[i], values=("", user[i], mem[i], cpu[i], pid[i],thread_count[i],counter[i]))
    print("Refresh")

queue_opcion = Queue()
queue_PID = Queue()
delay = 0
consigue_Procesos = Thread(target=guarda_procesos, args=(delay,))
consigue_Procesos.daemon = True
consigue_Procesos.start()
refresh_tktree = Thread(target = refresh_gui)
refresh_tktree.daemon = True

root = tk.Tk()
note = ttk.Notebook(root)

root.title("Procesos Corriendo")
root.geometry("1100x700")



tab_procesos = ttk.Frame(note)
tab_graficas = ttk.Frame(note)
tab_recomenadaciones = ttk.Frame(note)
tab_info = ttk.Frame(note)

note.add(tab_procesos,text='Procesos')
note.add(tab_graficas, text= 'Perfomance')
note.add(tab_recomenadaciones,text='Recommendaciones')
note.add(tab_info,text='Informacion')

panel_procesos = PanedWindow(tab_procesos)
panel_procesos.pack(side=TOP)
panel_graficas = PanedWindow(tab_graficas)
panel_graficas.pack(side=TOP)
panel_recomenadaciones = PanedWindow(tab_recomenadaciones)
panel_recomenadaciones.pack(side=TOP)
panel_informacion = PanedWindow(tab_info)
panel_informacion.pack(side = TOP)

scrollbar=Scrollbar(tab_procesos)
scrollbar.pack(side=RIGHT, fill=Y)
tree = ttk.Treeview(tab_procesos,yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)
scrollbarR=Scrollbar(tab_recomenadaciones)
scrollbarR.pack(side = RIGHT,fill = Y)
treeR = ttk.Treeview(tab_recomenadaciones,yscrollcommand=scrollbarR.set)
scrollbarR.config(command=treeR.yview)

label_thread_count = Label(root,text=("Total de Threads Corriend = 0"))
label_procesos_count = Label(root,text="Total de procesos corriendo = 0")
label_Memoria_Virtual = Label(root, text='Tamano de Memoria Fisica = 0')
label_Memoria_Fisica = Label(root,text= 'Tamano de Memoria Virtual = 0 ')
label_Memoria_cache = Label(root, text='Cache = 0')
label_Recommendaciones = Label(tab_recomenadaciones, text='El Proceso que usa mas Memoria = /usr/lib/x86_64-linux-gnu/h\nEl Proceso que usa mas CPU = '
                                                          'gzip\n El proceso que esta activo la mayor cantidad de tiempo es  de root y es [bioset].'
                                                          'Por parte del usuario = /usr/lib/x86_64-linux-gnu/i ')
label_informacion = Label(tab_info, text = 'Task Monitor\nEspecificaciones:\nUso de CPU: 35-40% Max: 150%(Realizando Recomendaciones)\n'
                                           'Uso de Memoria:3-5% Max: 100% (Realizando Recomendaciones)\nCantidad de Threads: 5 max: 8 \nResfresh Rate= 5 sec'
                                           '\nEspecificaciones de la computadora utilizada para la prueba:\nProcesador:2 Nucleos Virtuales a 4.0GHz\n'
                                           'Memoria RAM: 8Gb\nSistema Operativo: Ubuntu 14\nEl analisis fue hecho utilizando una maquina virtual en VirtualBox',
                          font=('Arial',16),justify=LEFT)


top = Frame(tab_procesos)
bottom = Frame(tab_procesos)
top.pack(side=TOP, fill = BOTH, expand= False)
bottom.pack(side=BOTTOM, fill=BOTH, expand=False)
frame_grafica_mem = Frame(tab_graficas)
frame_grafica_cpu = Frame(tab_graficas)
canvas_mem = Canvas(frame_grafica_mem)
canvas_mem.pack(side=RIGHT, fill=BOTH, expand=1)
canvas_cpu = Canvas(frame_grafica_cpu)
canvas_cpu.pack(side=RIGHT, fill=BOTH, expand=1)
frame_grafica_cpu.pack(side=BOTTOM,expand=1,fill=BOTH)
frame_grafica_mem.pack(side=TOP,expand=1,fill=BOTH)
tree["columns"] = ("Command", "User", "Memory", "CPU", "PID","Threads")
names = ("Command", "User", "Memory", "CPU", "PID","Threads")
tree.heading("Memory", command =lambda: lee_procesos_log(1,False))
tree.heading("CPU",command = lambda: lee_procesos_log(2,False))
tree.heading("PID", command = lambda: lee_procesos_log(3,False))
tree.heading("User", command = lambda: lee_procesos_log(4,False))
tree.heading("Command",command =lambda: lee_procesos_log(5,False))
tree.heading("Threads",command = lambda: lee_procesos_log(6,False))

treeR["columns"] = ("Command", "User", "Memory", "CPU", "PID","Threads",'Counter')
names2 = ("Command", "User", "Memory", "CPU", "PID","Threads",'Counter')
treeR.heading("Memory", command =lambda: lee_procesos_log2(2))
treeR.heading("CPU",command = lambda: lee_procesos_log2(3))
treeR.heading("PID", command = lambda: lee_procesos_log2(1))
treeR.heading("User", command = lambda: lee_procesos_log2(4))
treeR.heading("Command",command =lambda: lee_procesos_log2(7))
treeR.heading("Threads",command = lambda: lee_procesos_log2(5))
treeR.heading("Counter",command = lambda: lee_procesos_log2(6))
for name in names:
    tree.column(name, width=100)
    tree.heading(name, text=name)
for name in names2:
    treeR.column(name, width=100)
    treeR.heading(name, text=name)

lee_procesos_log(3,False)
lee_procesos_log2(1)

label_thread_count.pack(in_ = bottom,side=RIGHT)
label_procesos_count.pack(in_ = bottom,side=RIGHT)
label_Memoria_Fisica.pack(in_ = bottom, side= RIGHT)
label_Memoria_Virtual.pack(in_ = bottom, side = RIGHT)
label_Memoria_cache.pack(in_= bottom, side = RIGHT)
label_Recommendaciones.pack(side = BOTTOM)
label_informacion.pack(side = TOP)
btnMap = Button (root,text='Map Disk', command=map_disk)
btnMap.pack(in_=top,side = RIGHT)
btnAnalisis = Button(tab_recomenadaciones,text='Hacer Analisis', command = analizandoLogs)
btnAnalisis.pack(side=TOP)
btnGraficaMemoria = Button(root, text = 'Graficar RAM',
                           command=lambda: grafica_memoria(1))
btnGraficaMemoria.pack(in_ = top,side = LEFT)
btnMemoriaVirtual = Button(root, text='Graficar Memoria Swap', command = lambda: grafica_memoria(0))
btnMemoriaVirtual.pack(in_= top, side = LEFT)
btnMapFolders = Button(root, text = 'Map Folders', command = mapBoabab)
btnMapFolders.pack(in_ = top, side = RIGHT)
btnCrearProceso = Button (root,text = 'Crear Proceso', command = crearProceso)
btnCrearProceso.pack(in_=top,side=RIGHT)
btnShowMemory =Button(root,text='Limpiar Memoria',command = limpia_memoria)
btnShowMemory.pack(in_=top, side=RIGHT)
btnExit = Button(root, text='Exit', command=root.destroy)
btnExit.pack(in_=bottom, side=LEFT)
tree.bind("<Button-3>", click_derecho)
tree.pack(fill=BOTH, expand=1, side=LEFT)
treeR.pack(fill=BOTH, expand=1, side=LEFT)
refresh_tktree.start()
note.pack(expand=1,fill=BOTH)


grafica(canvas_cpu,canvas_mem)
root.mainloop()