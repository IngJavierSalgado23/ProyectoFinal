import os
import signal
from multiprocessing import Queue
from multiprocessing import Process
import subprocess as sp
from subprocess import check_output
import time
from Tkinter import *
import matplotlib.pyplot as plt
class Grafica:
    def __init__(self):
        opcion = 1
        print("Graficando")
        datos = []
        total = len(datos)
        while (len(datos)<1000):
            if(opcion == 0): #CPU
                check_output("ps axo pmem,pcpu> /home/ingjaviersalgado23/grafica.log", shell=True)
                check_output("tail -n +2 /home/ingjaviersalgado23/grafica.log > /home/ingjaviersalgado23/grafica2.log",shell=True)
                out = check_output("awk '{print $2}' /home/ingjaviersalgado23/grafica2.log ", shell=True)
                procesos = (out.splitlines())
            elif(opcion ==1): #Memoria
                check_output("ps axo pmem,pcpu> /home/ingjaviersalgado23/grafica.log", shell=True)
                check_output("tail -n +2 /home/ingjaviersalgado23/grafica.log > /home/ingjaviersalgado23/grafica2.log",
                             shell=True)
                out = check_output("awk '{print $1}' /home/ingjaviersalgado23/grafica2.log ", shell=True)
                procesos = (out.splitlines())
            for proceso in procesos:
                total += eval(proceso)
            print(len(datos))
            datos.append(total)
            total = 0
            if (len(datos) > 20):
                fig = plt.plot(datos)
                plt.ylabel("Uso de CPU")
                plt.show()
                check_output("rm /home/ingjaviersalgado23/grafica.log", shell=True)
                check_output("rm /home/ingjaviersalgado23/grafica2.log", shell=True)
                time.sleep(3)
                print("clearing")

#graf = Grafica()
