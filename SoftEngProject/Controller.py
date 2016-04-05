__author__ = 'Patipon'


from output import*
from Server_Family import*
from PySide.QtGui import*
from tabChat import*
from JavaCompile import*
from pythonCompile import*

class Controller(QtGui.QMainWindow):

    def __init__(self):
        super(Controller,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.serverMsg = ServerMsg("127.0.0.1", 3616)
        self.serverFile = ServerFile("127.0.0.1", 3617)
        self.javaCompiler = JavaComplie()
        self.pythonCompiler = PythonCompile()
        self.serverMsg.usernameTrigger.connect(self.newConnectionHandler)
        self.serverMsg.newMsg.connect(self.newMsgHandler)
        self.serverFile.newFile.connect(self.newFileHandler)
        self.ui.sendButton.clicked.connect(self.sendButtonHandler)


    def sendButtonHandler(self):
        text  = self.ui.lineEdit.text()
        self.ui.lineEdit.setText("")
        print("text = " + text)
        print(self.ui.tabWidget.currentWidget().getUsername())
        self.sendMsgTo(self.ui.tabWidget.currentWidget().getUsername(), text)

    def sendMsgTo(self,username, msg):
        userList = self.serverMsg.getUsernameList()
        for i in range (len(userList)):
            if userList[i] == self.ui.tabWidget.currentWidget().getUsername():
                self.serverMsg.threadingList[i].sendMsg(msg)

    def sendSysMsgTo(self, username, msg):
        userList = self.serverMsg.getUsernameList()
        for i in range (len(userList)):
            print(self.ui.tabWidget.currentWidget())
            if userList[i] == self.ui.tabWidget.currentWidget().getUsername():
                self.serverMsg.threadingList[i].sendSysMsg(msg)
                print("init data msg : " + msg)



    def newConnectionHandler(self, username):
        #send SYS MSG (HOST INFO)
        self.ui.OnlineList.addItem(QListWidgetItem(username))
        self.ui.tabWidget.addTab(TabChat(username),username)
        self.sendSysMsgTo(username,"initData,ShubU's Room;5;JP;3.30PM")
        print("messsage sent")



    def newMsgHandler(self, msg):
        print("New msg received : " + msg)
        self.tabList = self.serverMsg.getUsernameList()
        name = ""
        check = 0
        newData = ""
        for i in msg:
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


    def newFileHandler(self, filename):
        name = filename.split(".")
        if name[1] == "py":
            self.pythonCompiler.setFileDir(filename)
            ans = self.pythonCompiler.compilePy()
            print(ans)
        elif name[1] == "java":
            self.javaCompiler.setFileDirectory(name)
            print("output from file "  + str(self.javaCompiler.compileJav()))

            output = self.javaCOmpiler.compileJav()
        #aow output pai compare gub expected output

        #aow output pai check nai checker tor




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    a = Controller()



    a.show()
    sys.exit(app.exec_())


