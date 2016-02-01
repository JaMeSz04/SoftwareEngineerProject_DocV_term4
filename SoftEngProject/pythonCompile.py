import subprocess
import os.path
import sys


class PythonCompile:
    def __init__(self):
        self.javac = "C:\\Program Files\\Java\\jdk1.8.0_60\\bin\\javac"
        self.java = "C:\\Program Files\\Java\\jdk1.8.0_60\\bin\\java"
        self.python = "C:\\python35\\python"

    def compileJav(self):
        #getAllJavaFileIn .Py directory
        allFile = os.listdir('.')
        for fn in allFile:
            if fn.rfind("JavaCompile.py") != -1:
                print("Found a java file named " + fn)
                cmd = [self.python, fn]
                outputStatus = subprocess.Popen(cmd, stdout = subprocess.PIPE,stdin = subprocess.PIPE )
                output = outputStatus.communicate()
                print(output)
                stringout = output(2)
                stringout = stringout.decode("utf-8")
                print(stringout)
            else:
                print("File not found")

                
