__author__ = 'Patipon'


from socket import*
import threading



class Server:
    def __init__(self, ipAddr = "127.0.0.1", port = 3616):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.host = ipAddr
        self.port = port
        self.connectionList = []
        self.threadingList = []
        self.incoming = False

    def start(self):
        self.s.bind((self.host,self.port))
        self.s.listen(10)
        threading.Thread(target = self.acceptConnection).start()

    def acceptConnection(self):
        while True:
            self.conn , self.addrIn = self.s.accept()
            self.incoming = True
            self.temp = (self.conn,self.addrIn)
            self.connectionList.append((self.conn,self.addrIn))
            client = ClientHandler(self.conn)
            self.threadingList.append(client)

    def broadcast(self,data):
        for i in self.threadingList:
            i.sendMessage(data)

    def getIncoming(self):
        return self.incoming
    def getConn(self):
        return self.temp

    def setIncoming(self,incoming):
        self.incoming = incoming





class ClientHandler():
    def __init__(self, conn):
        self.conn = conn
        self.recvUserData()
        threading.Thread(target = self.run).start()
        self.notify = False



    def recvUserData(self):
        self.username = self.conn.recv(1024)
        self.username.decode("utf-8")

    def sendMessage(self, data):
        data = data.encode("utf-8")
        self.conn.send(data)

    def run(self):
        while True:
            initData = self.conn.recv(1024)
            initData = initData.decode("utf-8")
            self.initDataList = initData.split(",")
            #one is quuestion Num , second is filename , third is filetype, forth is filesize
            if self.initDataList[0][0:3] == "[1]":
                self.getFile()
                self.notify = True
                #file type
            elif self.initDataList[0][0:3] == "[2]":
                self.msg = self.initDataList[3:]
                self.msg = self.msg.decode("utf-8")
                self.notify = True
                #msg type

    def getFile(self):
        filename = str(self.conn)+ "-" + self.initDataList[0][3:]  + str(self.initDataList[2])
        file = open(filename, "wb")
        data = self.conn.recv(1024)
        totalRecv = len(data)
        file.write(data)
        print(self.initDataList[1])
        while totalRecv < int(self.initDataList[3][1:]):
            print("transmitting data...")
            data = self.conn.recv(1024)
            totalRecv += len(data)
            file.write(data)
            print(str(totalRecv/float(self.initDataList[3])) + "% done")
        file.close()
        self.dataFile = filename

    def getNotify(self):
        return self.notify

    def setNotify(self, notify):
        self.notify = notify

    def getFileType(self):
        if (self.initDataList[0][0:3] == "[1]"):
            return "file"
        elif (self.initDataList[0][0:3] == "[2]"):
            return "msg"

    def getDataFile(self):
        return self.dataFile

    def getMsg(self):
        return self.msg









