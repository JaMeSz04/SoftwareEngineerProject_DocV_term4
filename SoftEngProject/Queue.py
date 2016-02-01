__author__ = 'Patipon'




class Queue:
    def __init__(self):
        self.list = []

    def enqueue(self, item):
        self.list.append(item)

    def dequeue(self):
        a = self.list[0]
        self.list.pop(0)
        return a

    def isEmpty(self):
        if not self.list:
            return True
        else:
            return False