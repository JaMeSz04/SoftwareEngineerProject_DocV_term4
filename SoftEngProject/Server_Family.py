__author__ = 'Patipon'
import socket
import threading
from PySide.QtCore import *
from PySide.QtGui import *

class Server(QMainWindow):

    newFile = Signal(str)
    newMsg = Signal(str)
    usernameTrigger = Signal(str)

    def __init__(self, ipAddr, port):
        super(Server,self).__init__()
        self.c = None
        self.ipAddr = ipAddr
        self.port = port
        self.connectionList = []
        self.threadingList = []
        self.usernameList = []
        self.start()

    def start(self):
        self.s = socket.socket()
        self.s.bind((self.ipAddr,self.port))
        self.s.listen(5)
        print("server started...")

    def acceptConnection(self):
        pass
    def getIncoming(self):
        return self.incoming

    def setImcoming(self, incoming):
        self.incoming = incoming

    def getUsernameTrigger(self):
        return self.usernameTrigger

    def getUsernameList(self):
        return self.usernameList


class ServerFile(Server):


    def __init__(self, ipAddr, port):
        super().__init__(ipAddr,port)
        self.ipAddr = ipAddr
        self.port = port
        threading.Thread(target = self.acceptConnection).start()

    def acceptConnection(self):
        while True:
            conn, addr = self.s.accept()
            self.connectionList.append(conn)
            print("Client connected ip : " + str(addr))
            self.c = ClientHandlerFile(conn, addr)
            self.c.start()
            self.c.newFile.connect(self.newFileHandler)
            self.threadingList.append(self.c)

    def newFileHandler(self, fileName):
        print("newFile in server emiting...")
        self.newFile.emit(fileName)


class ServerMsg(Server):
    def __init__(self, ipAddr, port):
        super().__init__(ipAddr,port)
        self.ipAddr = ipAddr
        self.port = port
        threading.Thread(target = self.acceptConnection).start()
    def acceptConnection(self):
        while True:
            conn, addr = self.s.accept()
            self.connectionList.append(conn)
            print("Client connected ip msg : " + str(addr))
            self.c = ClientHandlerMsg(conn, addr)
            self.c.start()
            print("connecting to signal")
            print("uername msg is equal to " + self.c.name)
            self.usernameList.append(self.c.name)
            self.usernameTrigger.emit(self.c.name)
            self.c.newMsg.connect(self.newMsgHandler)
            self.threadingList.append(self.c)


    def newMsgHandler(self, msg):
        print("Signal emitted")
        self.newMsg.emit(msg)

    def getHandler(self):
        return self.c


class ClientHandlerMsg(QThread):
    usernameTrigger = Signal(str)
    newMsg = Signal(str)

    def __init__(self,sock, addr, parent = None):
        super(ClientHandlerMsg,self).__init__(parent)
        print("Client handler started")
        self.s = sock
        self.addr = addr
        self.name = None
        #First line data Pattern (Question num, filesize, language used)
        print("waiting for data from : " + str(self.addr))
        self.getUsername()
        print("Username = " + str(self.name))

    def run(self):
        print("client handler msg started")
        while True:
            print("yeee")
            data = self.s.recv(1024)
            data = data.decode("utf-8")
            print("no more yee")
            print(data)
            self.newMsg.emit(data)
            print("Emitted")

    def sendMsg(self,msg):
        data = "{#SimMsg}: " + msg
        data = data.encode("utf-8")
        self.s.send(data)

    def sendSysMsg(self, msg):
        data = "{#SysMsg}: " + msg
        data = data.encode("utf-8")
        self.s.send(data)

    def getUsername(self):
        self.name = self.s.recv(1024)
        self.name = self.name.decode("utf-8")
        self.usernameTrigger.emit(self.name)




class ClientHandlerFile(QThread):

    usernameTrigger = Signal(str)
    newFile = Signal(str)

    def __init__(self, sock, addr, parent = None):
        super(ClientHandlerFile,self).__init__(parent)
        self.s = sock
        self.addr = addr
        self.w8ingState = True


        #First line data Pattern (Question num, filesize, language used)

    def run(self):
        print("waiting for data from : " + str(self.addr))
        while True:
            self.recvingState()
            if self.w8ingState == False:
                self.getFirstData()
                self.getFile()
                self.w8ingState = True

    def recvingState(self):
        status = self.s.recv(1024)
        if status.decode("utf-8") == "starting":
            self.w8ingState = False

    def getFile(self):
        filename = ""
        if (self.firstData[2] == "Python"):
            filename = "recvFileTest.py"
        elif (self.firstData[2] == "Java"):
            filename = "recvFileTest.java"
        file = open(filename , "wb")

        data = self.s.recv(1024)
        totalRecv = len(data)
        file.write(data)
        print("first data = " + str(self.firstData))

        while totalRecv < int(self.firstData[3]):
            print("transmitting data...")
            data = self.s.recv(1024)
            totalRecv += len(data)
            file.write(data)
            print(str(totalRecv/float(self.firstData[3])) + "% done")

        file.close()
        self.newFile.emit(str(filename))
        print("yoyo get file laww")

    def getFirstData(self):
        data = self.s.recv(1024)
        if data:
            data = data.decode("utf-8")
            self.firstData = data.split(",")
        print(self.firstData)








