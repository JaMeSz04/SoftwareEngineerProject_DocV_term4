__author__ = 'Patipon'

import socket
import threading


class Server:
    def __init__(self, ipAddr, port):
        self.ipAddr = ipAddr
        self.port = port
        self.connectionList = []
        self.threadingList = []

    def start(self):
        self.s = socket.socket()
        self.s.bind((self.ipAddr,self.port))
        self.s.listen(5)
        print("server started...")
        threading.Thread(target = self.acceptConnection).start()

    def acceptConnection(self):
        while True:
            conn, addr = self.s.accept()
            self.incoming = True
            self.connectionList.append((conn,addr))
            print("Client connected ip : " + str(addr))
            c = ClientHandler(conn, addr)
            c.start()
            self.threadingList.append(c)
    def getIncoming(self):
        return self.incoming

    def setImcoming(self, incoming):
        self.incoming = incoming


class ClientHandler(threading.Thread):
    def __init__(self, sock, addr):
        threading.Thread.__init__(self)
        self.s = sock
        self.addr = addr
        #First line data Pattern (Question num, filesize, language used)


    def start(self):
        print("waiting for data from : " + str(self.addr))
        self.getName()
        self.getFirstData()
        self.getFile()

    def getName(self):
        self.name = self.s.recv(1024)
        self.name = self.name.decode("utf-8")


    def getFile(self):
        file = open(str(self.addr) + ".txt" , "wb")
        data = self.s.recv(1024)
        totalRecv = len(data)
        file.write(data)
        print(self.firstData[2])
        while totalRecv < int(self.firstData[2][1:]):
            print("transmitting data...")
            data = self.s.recv(1024)
            totalRecv += len(data)
            file.write(data)
            print(str(totalRecv/float(self.firstData[1])) + "% done")

    def getName(self):
        name = self.s.recv(1024)
        name = name.decode("utf-8")


    def getFirstData(self):
        data = self.s.recv(1024)
        data = data.decode("utf-8")
        self.firstData = data.split(",")
        print(self.firstData)


a = Server("127.0.0.1", 3616)
a.start()








