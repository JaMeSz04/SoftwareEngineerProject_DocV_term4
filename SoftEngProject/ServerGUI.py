__author__ = 'Patipon'

from PySide import*
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtUiTools import QUiLoader
import sys
from UILoader import UiLoader



class ServerGUI(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        loader = UiLoader()
        self.ui = loader.loadUi('serverGUI.ui', self)
        hLayout = QHBoxLayout()
        self.lineEdit = QLineEdit()
        self.sendButton = QPushButton("Send")
        self.tabWidget = QTabWidget()
        hLayout.addWidget(self.lineEdit)
        hLayout.addWidget(self.sendButton)

        self.ui.chatLogLayout.addWidget(self.tabWidget)
        self.ui.chatLogLayout.addLayout(hLayout)
    def getUI(self):
        return self.ui
    def getChatLineEdit(self):
        return self.lineEdit
    def getSendBututon(self):
        return self.sendButton
    def getTabWidget(self):
        return self.tabWidget


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main_window = ServerGUI()
    main_window.show()
    sys.exit(app.exec_())