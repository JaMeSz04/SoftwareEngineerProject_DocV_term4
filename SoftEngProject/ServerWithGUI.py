__author__ = 'Patipon'
import socket
import threading
from PySide import QtGui, QtCore
from ServerGUI import*
from tabChat import TabChat
import sys


class Server:

    def __init__(self, ipAddr, port):
        app = QtGui.QApplication(sys.argv)
        self.ipAddr = ipAddr
        self.port = port
        self.serverGUI = None
        self.serverUI = None
        self.connectionList = []
        self.threadingList = []
        self.createServerGUI()
        self.start()
        sys.exit(app.exec_())

    def createServerGUI(self):
        self.serverGUI = ServerGUI()
        self.serverGUI.show()
        self.serverUI = self.serverGUI.getUI()

    def start(self):
        print("START")
        self.s = socket.socket()
        self.s.bind((self.ipAddr,self.port))
        print("BINDED")
        self.s.listen(5)
        print("server started...")
        conHandler = self.acceptConneectionHandler(self.s)
        conHandler.start()
        self.serverUI.connect(self.acceptConneectionHandler,QtCore.SIGNAL("newConnection(QString)"),self.updateIncomingUser)
        self.threadingList.append(conHandler)


    def acceptConnection(self):
        while True:
            conn, addr = self.s.accept()
            print("CONNECTED WITH " + str(addr))
            self.username = conn.recv(1024)
            self.username = self.username.decode("utf-8")
            print("Username "  + self.username)
            self.updateIncomingUser()
            self.connectionList.append((conn,addr,self.username))
            print("Client connected ip : " + str(addr))
            c = ClientHandler(conn, addr,self.serverUI)

            self.threadingList.append(c)

    def updateIncomingUser(self,username, tauple):
        print(self.serverUI)
        print("user info  : " + str(tauple))
        self.connectionList.append(tauple)
        self.serverUI.OnlineList.addItem( QListWidgetItem(username) )
        self.serverGUI.getTabWidget().addTab(TabChat(username),username)

    class acceptConneectionHandler(QtCore.QThread):
        def __init__(self,socket,parent = None):
            super(Server.acceptConneectionHandler,self).__init__(parent)
            self.s = socket


        def run(self):
            while True:
                conn,addr = self.s.accept()

                print("CONNECTED WITH " + str(addr))
                username = conn.recv(1024)
                username = username.decode("utf-8")
                print("USERNAME : " + username)
                if conn:
                    self.emit(QtCore.SIGNAL("newConnection(QString)"), username, (conn,addr,username))

                print("CONNECT IP : " + str(addr))




class ClientHandler():
    def __init__(self, conn,addr,ui):
        self.conn = conn
        self.recvUserData()
        self.exiting = False
        self.notify = False
        self.ui = ui
        threading.Thread(target = self.run ).start()

    def __del__(self):
        self.exiting = True
        self.wait()


    def recvUserData(self):
        self.username = self.conn.recv(1024)
        self.username.decode("utf-8")

    def sendMessage(self, data):
        data = data.encode("utf-8")
        self.conn.send(data)

    def run(self):
        while True:
            initData = self.conn.recv(1024)
            initData = initData.decode("utf-8")
            self.initDataList = initData.split(",")
            #one is quuestion Num , second is filename , third is filetype, forth is filesize
            if self.initDataList[0][0:3] == "[1]":
                self.getFile()
                self.notify = True
                self.ui.TabChat.update("FILE INCOMING")
                #file type
            elif self.initDataList[0][0:3] == "[2]":
                self.msg = self.initDataList[3:]
                self.msg = self.msg.decode("utf-8")
                self.notify = True
                self.ui.TabChat.update("FILE INCOMING")
                #msg type

    def getFile(self):
        filename = str(self.conn)+ "-" + self.initDataList[0][3:]  + str(self.initDataList[2])
        file = open(filename, "wb")
        data = self.conn.recv(1024)
        totalRecv = len(data)
        file.write(data)
        print(self.initDataList[1])
        while totalRecv < int(self.initDataList[3][1:]):
            print("transmitting data...")
            data = self.conn.recv(1024)
            totalRecv += len(data)
            file.write(data)
            print(str(totalRecv/float(self.initDataList[3])) + "% done")
        file.close()
        self.dataFile = filename

    def getNotify(self):
        return self.notify

    def setNotify(self, notify):
        self.notify = notify

    def getFileType(self):
        if (self.initDataList[0][0:3] == "[1]"):
            return "file"
        elif (self.initDataList[0][0:3] == "[2]"):
            return "msg"

    def getDataFile(self):
        return self.dataFile

    def getMsg(self):
        return self.msg


a = Server("127.0.0.1", 3616)
