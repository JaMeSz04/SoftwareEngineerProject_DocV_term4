__author__ = 'Patipon'


from output import*
from Server_Family import*
from PySide.QtGui import*
from tabChat import*
from JavaCompile import*



class Controller(QtGui.QMainWindow):

    def __init__(self):
        super(Controller,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.serverMsg = ServerMsg("161.246.94.168", 3616)
        self.serverFile = ServerFile("161.246.94.168", 3617)
        self.javaCompiler = JavaComplie()
        self.serverMsg.usernameTrigger.connect(self.newConnectionHandler)
        self.serverMsg.newMsg.connect(self.newMsgHandler)
        self.serverFile.newFile.connect(self.newFileHandler)


    def newConnectionHandler(self, username):
        print("hello world")
        self.ui.OnlineList.addItem(QListWidgetItem(username))
        self.ui.tabWidget.addTab(TabChat(username),username)


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
        name = filename
        print("New file received : " + name)
        self.javaCompiler.setFileDirectory(name)
        print("output from file "  + str(self.javaCompiler.compileJav()))
        #aow output pai check nai checker tor




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    a = Controller()



    a.show()
    sys.exit(app.exec_())


