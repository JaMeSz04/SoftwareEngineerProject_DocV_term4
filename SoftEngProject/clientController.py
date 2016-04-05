__author__ = 'Patipon'

from PySide import QtGui
from PySide import QtCore
from ClientGUIFinal import*
import sys


class ClientController(QtGui.QMainWindow):
    def __init__(self):
        super(ClientController,self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)






if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    a = ClientController()



    a.show()
    sys.exit(app.exec_())