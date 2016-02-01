__author__ = 'Patipon'

from PySide import QtGui, QtCore
from UILoader import UiLoader
from PySide.QtUiTools import QUiLoader
import sys



class PageOne(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        loader = QUiLoader()
        file = QtCore.QFile("createRoom1.ui")
        file.open(QtCore.QFile.ReadOnly)
        widget = loader.load(file, parent)
        file.close()








if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main_window = PageOne()
    main_window.show()
    sys.exit(app.exec_())