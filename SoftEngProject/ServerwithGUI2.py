__author__ = 'Patipon'


import socket
import threading
from PySide.QtUiTools import QUiLoader
import sys
from ServerGUI import*
from output import*
from tabChat import*
from JavaCompile import*






class Server(QtGui.QMainWindow):
    def __init__(self,ipAddr, port,parent = None):
        super(Server,self).__init__()
        self.ipAddr = ipAddr
        self.port = port
        self.javacDir = None
        self.javaDir = None
        self.pyDir = None
        self.javaComplier = None
        self.ui = Ui_MainWindow()
        self.connectionList = []
        self.threadingList = []
        self.fileHanderList = []
        self.connectionListConn = []
        self.tabList = []
        self.ui.setupUi(self)
        self.ui.sendButton.clicked.connect(self.sendButtonHandler)
        self.ui.lineEdit.returnPressed.connect(self.sendButtonHandler)
        self.start()

    def setJavacDirectory(self, dir):
        self.javacDir = dir
    def setJavaDirectory(self, dir):
        self.javaDir = dir
    def setPyDirectory(self, dir):
        self.pyDir = dir

    def sendButtonHandler(self):
        msg = self.ui.lineEdit.text()
        self.ui.tabWidget.currentWidget().update("You : " + msg)
        username = self.ui.tabWidget.currentWidget().getUsername()
        print("username check handler :" + str(username))
        for i in range (len(self.connectionList)):
            print (" i : " + str(self.connectionList[i]))
            if (self.connectionList[i][2] == username):
                self.sendMessageTo(self.connectionListConn[i],msg)
        self.ui.lineEdit.setText("")


    def sendMessageTo(self, conn, msg):
        msg = msg.encode("utf-8")
        conn.send(msg)

    def getPyDir(self):
        return self.pyDir
    def getJavacDir(self):
        return self.javacDir
    def getJavaDir(self):
        return self.javaDir

    def start(self):
        self.javaComplier = JavaComplie()
        self.s = socket.socket()
        self.s.bind((self.ipAddr,self.port))
        print("BINDED")
        self.s.listen(5)
        print("server started...")
        conHandler = acceptHandler(self.s)
        conHandler.start()
        self.connect(conHandler, QtCore.SIGNAL("newConnection(QString)"),self.updateConnection)
        self.connect(conHandler, QtCore.SIGNAL("MsgHandler(QString)"), self.msgHandler)
        self.connect(conHandler, QtCore.SIGNAL("fileHandler(QString)"), self.fileHandler)
        #self.connect(conHandler, QtCore.SIGNAL("sendConn(object)"),self.connHandler)
        conHandler.connSignal.connect(self.connHandler)
        self.threadingList.append(conHandler)

    def connHandler(self,conn):
        print("CONN  : " + str(conn))
        self.connectionListConn.append(conn)

    def msgHandler(self, data):
        print("MSG  : " + data)
        name = ""
        check = 0
        newData = ""
        for i in data:
            if i == ">":
                check = 0
            if check == 1:
                name += i
            if check == 0:
                newData += i
            if i == "<":
                check = 1

        print(name)
        newData = newData [3:]
        print("tabList  :" + str(self.tabList))
        for i in range(len(self.tabList)):
            print(self.tabList[i])
            print(name)
            if self.tabList[i] == name:
                widget = self.ui.tabWidget.widget(i)
                print("Widget : " + str(widget))
                widget.update(newData)
                print("updated")


    def fileHandler(self, data):
        print("data appended")
        self.fileHanderList.append(data)

    def updateConnection(self,data):
        print("data : " + data)
        parts = data.split(":")
        tauple = (parts[0], parts[1],parts[2])
        self.tabList.append(parts[2])
        self.connectionList.append(tauple)
        self.ui.OnlineList.addItem(QListWidgetItem(parts[2]))
        self.ui.tabWidget.addTab(TabChat(parts[2]),parts[2])


    def fileCompileHandler(self):
        while True:
            if len(self.fileHanderList) != 0:
                filename = self.fileHanderList[0]
                self.fileHanderList = self.fileHanderList[1:]
                self.javaComplier.setFileDirectory(filename)
                print(self.javaComplier.compileJav())







class acceptHandler(QThread):
    connSignal = QtCore.Signal(socket.socket)

    def __init__(self ,socket1 , parent = None):
        super(acceptHandler,self).__init__(parent)
        self.s = socket1

    def run(self):
        while True:
            conn,addr = self.s.accept()

            print("CONNECTED WITH " + str(addr))
            username = conn.recv(1024)
            username = username.decode("utf-8")
            print("USERNAME : " + username)
            if conn:
                data = str(conn) + ":" + str(addr) + ":" + str(username)
                #self.emit(QtCore.SIGNAL("sendConn(object)"), conn)
                self.connSignal.emit(conn)
                #self.emit(self.connSignal,conn)
                self.emit(QtCore.SIGNAL("newConnection(QString)"), data)
            print("CONNECT IP : " + str(addr))
            clientHandler = ClientHandler(conn)
            clientHandler.start()

            self.connect(clientHandler, QtCore.SIGNAL("NewMsg(QString)"),self.msgHandler)
            self.connect(clientHandler, QtCore.SIGNAL("fileHandler(QString)"),self.fileHandler)
    def msgHandler(self ,data):
        print("msghandler in accept handler work")
        self.emit(QtCore.SIGNAL("MsgHandler(QString)"),data)
    def fileHandler(self, data):
        self.emit(QtCore.SIGNAL("fileHandler(QString"), data)

class ClientHandler(QThread):
    def __init__(self, conn,parent = None):
        super(ClientHandler,self).__init__(parent)
        self.conn = conn
        self.recvUserData()

    def recvUserData(self):
        self.username = self.conn.recv(1024)
        self.username = self.username.decode("utf-8")

    def sendMessage(self, data):
        data = data.encode("utf-8")
        self.conn.send(data)

    def run(self):
        while True:
            print("running")
            initData = self.conn.recv(1024)
            initData = initData.decode("utf-8")
            print("init data : " + str(initData))
            self.initDataList = initData.split(",")
            #one is quuestion Num , second is filename , third is filetype, forth is filesize
            if self.initDataList[0][0:3] == "[1]":
                print("yoyo")
                self.getFile()
                self.notify = True
                #file type
            elif self.initDataList[0][0:3] == "[2]":
                self.msg = self.initDataList[0][4:]
                print(str(self.msg))
                print("Message " + self.msg)
                self.emit(QtCore.SIGNAL("NewMsg(QString)"),self.msg)

    def getFile(self):
        filename = self.username + " with " + self.initDataList[0][3:]  + "." + str(self.initDataList[2])
        print(self.initDataList[2])
        print("filename : " + filename)
        file = open(filename, "wb")
        data = self.conn.recv(1024)
        totalRecv = len(data)
        file.write(data)
        print(self.initDataList[1])
        print("init data list : "  , self.initDataList)
        print("check init data list : " + self.initDataList[3][1:])
        print("file size : " + self.initDataList[len(self.initDataList) - 1])
        while totalRecv < int(self.initDataList[len(self.initDataList) - 1]):
            print("transmitting data...")
            data = self.conn.recv(1024)
            totalRecv += len(data)
            file.write(data)
            print(str(totalRecv/float(self.initDataList[3])) + "% done")
        file.close()
        self.dataFile = filename
        self.emit(QtCore.SIGNAL("fileHandler(QString)"),self.dataFile)


    def getFileType(self):
        if (self.initDataList[0][0:3] == "[1]"):
            return "file"
        elif (self.initDataList[0][0:3] == "[2]"):
            return "msg"

    def getDataFile(self):
        return self.dataFile

    def getMsg(self):
        return self.msg




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    a = Server("127.0.0.1", 3616)
    QtCore.QMetaObject


    a.show()
    sys.exit(app.exec_())
