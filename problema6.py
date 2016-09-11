import os
def imprime():
    print("Proceso", os.getpid())
    while(True):
        x = 1 #Para no mandar a los hijos al estado defunct
def start_program():
    padre = os.getpid()
    child = 0
    for i in range(0,10):
        if(os.getpid()== padre):
            child=os.fork()
    if(os.getpid()!=padre):
        imprime()
   



start_program()
