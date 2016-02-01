import subprocess
import os.path
import sys


class JavaComplie:
    def __init__(self):
        self.javac = "C:\\Program Files\\Java\\jdk1.8.0_60\\bin\\javac"
        self.java = "C:\\Program Files\\Java\\jdk1.8.0_60\\bin\\java"

    def setJavac(self, javac):
        self.javac = javac

    def setJava(self,java):
        self.java = java

    def setFileDirectory(self, dir):
        self.dir = dir

    def compileJav(self):
        print("Java file named " + self.dir)
        print(subprocess.call([self.javac,self.dir]))
        classjav,ext = os.path.splitext(self.dir)
        className = self.dir[0:self.dir.rfind(".java")]
        print("class name is " + className)
        print("compiled")
        cmd = [self.java,className]
        outputStatus =  subprocess.Popen(cmd,stdout = subprocess.PIPE,stdin = subprocess.PIPE)
        word = "hehe"
        word = word.encode("utf-8")
        print(outputStatus.poll())
        output = outputStatus.communicate(word)

        print(outputStatus)
        print(outputStatus.poll())
        return output

                
                
                
            
