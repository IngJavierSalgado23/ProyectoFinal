class Proceso(object):

    def __init__(self,mem,cpu,user,pid,command,nlwp):
        self.mem = mem
        self.cpu = cpu
        self.user = user
        self.pid = pid
        self.command = command
        self.nlwp = nlwp
        self.acomulado = 0
        self.counter = 1

    def setMem(self,num):
        self.mem += num
    def getMem(self):
        return self.mem
    def setCPU(self,num):
        self.cpu += num
    def getCPU(self):
        return self.cpu
    def setUser(self,num):
        self.user = num
    def getUser(self):
        return self.user
    def setPID(self,num):
        self.pid = num
    def getPID(self):
        return self.pid
    def setCommand(self,num):
        self.command = num
    def getCommand(self):
        return str(self.command)
    def setThread(self,num):
        self.nlwp += num
    def getThread(self):
        return self.nlwp
    def setAcumulado(self,num):
        self.acumulado += num
    def getAcumulado(self):
        return self.acumulado
    def incCounter(self,num):
        self.counter += num
    def getCounter(self):
        return float(self.counter)