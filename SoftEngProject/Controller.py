__author__ = 'Patipon'
from ServerGUI import*
from NewServer import*
from JavaCompile import*
from Queue import Queue
import threading
import os

class Controller:
    def __init__(self):
        app = QtGui.QApplication(sys.argv)
        self.server = Server()
        self.compileQueue = Queue()
        self.javaCompiler = JavaComplie()
        self.server.start()
        self.createServerGUI()
        threading.Thread(target = self.checkNotify).start()
        threading.Thread(target = self.queueHandler).start()
        threading.Thread(target = self.checkIncoming).start()
        sys.exit(app.exec_())

    def createServerGUI(self):
        self.serverGUI = ServerGUI()
        self.serverGUI.show()
        self.serverUI = self.serverGUI.getUI()

    def checkNotify(self):
        while True:
            for i in self.server.threadingList:
                if i.getNotify():
                    if (i.getFileType() == "file"):
                        compileFile = i.getDataFile()
                        self.compileQueue.enqueue(compileFile)
                        i.setNotify(False)

                    elif (i.getFileType() == "msg"):
                        msg = i.getMsg()
                        i.setNotify(False)

    def checkIncoming(self):
        while True:
            if self.server.getIncoming():
                conn = self.server.getConn()
                item = QListWidgetItem(str(conn[1]))
                self.serverUI.OnlineList.addItem(item)
                self.server.setIncoming(False)



    def queueHandler(self):
        while True:
            if self.compileQueue.isEmpty():
                continue
            else:
                file = self.compileQueue.dequeue()
                if file.rfind(".java") != -1:
                    self.javaCompiler.setFileDirectory(file)
                    output = self.javaCompiler.compileJav()
                elif file.rfind(".py") != -1:
                    print("SHUBU PYTHON")









Controller()




