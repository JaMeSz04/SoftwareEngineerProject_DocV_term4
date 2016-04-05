__author__ = 'Patipon'
from PySide import QtGui
from PySide import QtCore

class TabChat(QtGui.QWidget):
    def __init__(self, username, parent = None):
        super(TabChat,self).__init__(parent)
        self.username = username
        self.vBoxLayout = QtGui.QVBoxLayout()
        self.plainTextEdit = QtGui.QPlainTextEdit()
        styleSheetString = "#QPlainTextEdit { border: 1px white; }"
        self.plainTextEdit.setStyleSheet(styleSheetString)
        self.vBoxLayout.addWidget(self.plainTextEdit)
        self.setLayout(self.vBoxLayout)


    def getUsername(self):
        return self.username
    def update(self, text):
        print("text to update : " + text)
        print("test text :" + text[:5])
        print(text[:5] == "You :")
        if (text[:5] != "You :"):
            self.plainTextEdit.appendPlainText(self.username +  " : " + text)
        else:
            self.plainTextEdit.appendPlainText(text)
        print("UPDATED successfully")






