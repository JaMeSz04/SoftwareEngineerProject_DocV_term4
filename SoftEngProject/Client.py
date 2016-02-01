__author__ = 'Patipon'
import socket
import os
import threading

class Client:
    def __init__(self, ipAddr, port, name):
        self.ipAddr = ipAddr
        self.port = port
        self.name = name

    def start(self):
        self.s = socket.socket()
        self.s.connect((self.ipAddr,self.port))
        #self.setFilename()
        self.sendUserName()
        self.sendBugData()
        threading.Thread(target = self.recvmessage).start()

    def recvmessage(self):
        while True:
            self.data = self.s.recv(1024)
            self.data = self.data.decode("utf-8")
            print(self.data)
            
    def sendBugData(self):
        name = ""
        name = name.encode("utf-8")
        self.s.send(name)

    def sendFile(self):
        self.lunchInitData()
        print("Start send data process")
        with open(self.filename, "rb") as f:
            print("sending")
            data = f.read(1024)
            self.s.send(data)
            while data:
                print("sending")
                data = f.read(1024)
            self.s.shutdown(socket.SHUT_WR)


    def setFilename(self, type):
        self.filename = "testYOYO.txt"
        self.type = type

    def sendUserName(self):
        name = self.name.encode("utf-8")
        self.s.send(name)

    def lunchInitData(self):
        data = "[1]:QuestionOne," + self.filename + "," + self.type + "," + str(os.path.getsize(self.filename))
        data = data.encode("utf-8")
        self.s.send(data)

    def sendMessage(self, msg):
        msg = "[2]:" + "<" + self.name + "> "  + msg
        msg = msg.encode("utf-8")
        self.s.send(msg)
        print("message sent : " + str(msg))
    def shubu(self):
        self.setFilename("java")
        self.lunchInitData()
        self.sendFile()

a = Client("127.0.0.1", 3616,"SHUBU")
a.start()

