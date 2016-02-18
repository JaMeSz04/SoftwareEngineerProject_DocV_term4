__author__ = 'Patipon'




class RecvFile:
    def __init__(self, index, filename):
        self.index = index
        self.name = filename
        self.matchedQuestion = None

    def getIndex(self):
        return self.index

    def getName(self):
        return self.name

    def setIndex(self, index):
        self.index = index

    def setName(self, name):
        self.name = name
