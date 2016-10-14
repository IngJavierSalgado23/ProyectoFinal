import Tkinter as tk
import ttk
from Tkinter import *
from Funciones import *
def main():
    delay = 1
    consigue_Procesos = Process(target=guarda_procesos, args=(delay,))
    consigue_Procesos.daemon = True
    consigue_Procesos.start()

    root = tk.Tk()
    tree = ttk.Treeview()
    root.title("Procesos Corriendo")
    top = Frame(root)
    bottom = Frame(root)
    top.pack(side=TOP)
    bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
    tree["columns"] = ("Command", "User", "Memory", "CPU", "PID")
    names = ("Command", "User", "Memory", "CPU", "PID")
    for name in names:
        tree.column(name, width=100)
        tree.heading(name, text=name)

    lee_procesos_log(tree,0)
    tree.bind("<Button-3>", click_derecho)
    tree.bind("<Double-1>", OnDoubleClick)
    btnMap = Button(root, text='Mapea al disco duro', command=map_disk)
    btnMap.pack()
    btnSortCPU = Button(root, text='Procesos por CPU', command=lambda:lee_procesos_log(tree,2) )
    btnSortMem = Button(root, text='Procesos por Memoria', command=lambda: lee_procesos_log(tree,1))
    btnMap.pack(in_=top,side=RIGHT)
    btnSortCPU.pack(in_=top,side=RIGHT)
    btnSortMem.pack(in_=top,side=RIGHT)
    btnGraficaCPU = Button(root,text= 'Graficar el uso de CPU', command = lambda:grafica(0))
    btnGraficaCPU.pack(in_=bottom,side=RIGHT)
    btnGraficaMem = Button(root,text= 'Graficar el uso de Memoria', command = lambda:grafica(1))
    btnGraficaMem.pack(in_=bottom,side=RIGHT)
    tree.pack()
    root.mainloop()



def click_derecho(event,root):
    #try:
        item = root.tree.selection()[0]
        print("you clicked on", root.tree.item(item,"text"))
    #except:
        print("Error")


def OnDoubleClick(self, event):
    item = self.tree.identify('item', event.x, event.y)
    print("you clicked on", self.tree.item(item, "text"))

def lee_procesos_log(tree,opcion):
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
    repaint(procesos,user,mem,cpu,pid,tree)
def repaint(procesos,user,mem,cpu,pid,tree):
    for i in tree.get_children():
        tree.delete(i)
    for i in range(1, len(mem) - 1):
        tree.insert("", "end", text=procesos[i], values=("", user[i], mem[i], cpu[i], pid[i]))

main()
