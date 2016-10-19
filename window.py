import Tkinter as tk
import ttk
from Tkinter import *
from Funciones import *
from multiprocessing import Process
from threading import Thread
def click_derecho(event):
    print("Proceso a matar")
    try:
        for item in tree.selection():
            item_text = tree.item(item, "values")
            pid = (item_text[4])
            print pid
        matar_proceso(pid)
        lee_procesos_log(tree,1)
    except:
        print("Opcion no valida")

def refresh_gui():
    opcion = 1
    while(True):
        if(queue_opcion.empty() == False):
            opcion = queue_opcion.get()
        #print(opcion)
        lee_procesos_log(opcion,True)
        time.sleep(5)


def lee_procesos_log(opcion,hijo):
    if(hijo):
        pass
    else:
        queue_opcion.put(opcion)
    check_output("ps axo pmem,pcpu,user,pid,command> /home/ingjaviersalgado23/tempo.log", shell=True)
    if (opcion == 0):
        out = check_output("awk '{print $1}' /home/ingjaviersalgado23/tempo.log ", shell=True)
        mem = (out.splitlines())
        out = check_output("awk '{print $2}' /home/ingjaviersalgado23/tempo.log ", shell=True)
        cpu = (out.splitlines())
        out = check_output("awk '{print $3}' /home/ingjaviersalgado23/tempo.log ", shell=True)
        user = (out.splitlines())
        out = check_output("awk '{print $4}' /home/ingjaviersalgado23/tempo.log ", shell=True)
        pid = (out.splitlines())
        out = check_output("awk '{print $5}' /home/ingjaviersalgado23/tempo.log ", shell=True)
        procesos = (out.splitlines())
    elif (opcion == 1):
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
        out = check_output("awk '{print $5}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        procesos = (out.splitlines())
    elif (opcion ==2):
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
        out = check_output("awk '{print $5}' /home/ingjaviersalgado23/tempo2.log ", shell=True)
        procesos = (out.splitlines())
    repaint(procesos,user,mem,cpu,pid)
def repaint(procesos,user,mem,cpu,pid):
    for i in tree.get_children():
        tree.delete(i)
    for i in range(1, len(mem) - 1):
        tree.insert("", "end", text=procesos[i], values=("", user[i], mem[i], cpu[i], pid[i]))
    print("Refresh")

queue_opcion = Queue()
queue_PID = Queue()
delay = 1
consigue_Procesos = Thread(target=guarda_procesos, args=(delay,))
consigue_Procesos.daemon = True
consigue_Procesos.start()
refresh_tktree = Thread(target = refresh_gui)
refresh_tktree.daemon = True
root = tk.Tk()
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
tree = ttk.Treeview(yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)
root.title("Procesos Corriendo")
top = Frame(root)
bottom = Frame(root)
top.pack(side=TOP, fill = BOTH, expand= False)
bottom.pack(side=BOTTOM, fill=BOTH, expand=False)
tree["columns"] = ("Command", "User", "Memory", "CPU", "PID")
names = ("Command", "User", "Memory", "CPU", "PID")
for name in names:
    tree.column(name, width=100)
    tree.heading(name, text=name)
lee_procesos_log(0,False)
btnMap = Button(root, text='Mapea al disco duro', command=map_disk)
btnMap.pack()
btnSortCPU = Button(root, text='Procesos por CPU', command=lambda: lee_procesos_log(2,False))
btnSortMem = Button(root, text='Procesos por Memoria', command=lambda: lee_procesos_log(1,False))
btnMap.pack(in_=top, side=RIGHT)
btnSortCPU.pack(in_=top, side=RIGHT)
btnSortMem.pack(in_=top, side=RIGHT)
#btnGraficaCPU = Button(root, text='Graficar el uso de CPU', command=lambda: grafica(0,queue_PID))
btnGraficaCPU = Button(root, text='Graficar el uso de CPU', command=lambda:carlosGrafica(1))
btnGraficaCPU.pack(in_=bottom, side=RIGHT)
btnGraficaMem = Button(root, text='Graficar el uso de Memoria', command=lambda: carlosGrafica(2))
btnGraficaMem.pack(in_=bottom, side=RIGHT)
btnExit = Button(root, text='Exit', command=root.destroy)
btnExit.pack(in_=bottom, side=LEFT)
tree.bind("<Button-3>", click_derecho)
tree.pack(fill=BOTH, expand=1, side=LEFT)
refresh_tktree.start()
root.mainloop()
