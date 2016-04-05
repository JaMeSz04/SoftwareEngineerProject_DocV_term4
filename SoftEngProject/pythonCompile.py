import subprocess
import os.path
import sys


class PythonCompile:
    def __init__(self):
        self.python = "C:\\python34\\python"
        self.dir = None

    def setPyDir(self, dir):
        self.python = dir

    def setFileDir(self, dir):
        self.dir = dir

    def compilePy(self):
        #getAllJavaFileIn .Py directory
        allFile = os.listdir('.')
        for fn in allFile:
            if fn.rfind(self.dir) != -1:
                print("Found a java file named " + fn)
                cmd = [self.python, fn]
                outputStatus = subprocess.Popen(cmd, stdout = subprocess.PIPE,stdin = subprocess.PIPE )
                output = outputStatus.communicate()
                print(output)
                listoutput = list(output)
                print(listoutput)
                returnoutput = listoutput[0].decode("utf-8")
                return returnoutput


            else:
                print("File not found")

                
