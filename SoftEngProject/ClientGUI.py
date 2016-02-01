__author__ = 'Patipon'
from PyQt5 import QtGui, QtCore ,uic



import sys


class ClientGUI(QtGui.QMainWIndow):
    def __init__(self):
        QtGui.QMainWIndow.__init__(self)
        self.ui = uic.loadUi("C:\\Users\\Patipon\\Documents\\ClientGUI.ui")
        self.ui.show()

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    win = ClientGUI()
    sys.exit(app.exec_())



