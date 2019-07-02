import os
import sys

class GHDL():
    def __init__(self):
        self.lastfile = None
        self.lastentity = None
        self.path = "ghdl-0.36\\bin\\ghdl.exe"

    def askQuestion(self, question):
        while True:
            anwser = input(question)
            if anwser == "y" or anwser == "Y":
                return True
            if anwser == "n" or anwser == "N":
                return False
                break
            print("Please respond with 'y' for Yes or 'n' for No")

    def askNumber(self, question, min, max=-1):
        while True:
            count = input(question)
            if count.isdigit() and int(count) >= min and ((max != -1 and int(count) <= max) or max == -1):
                return int(count)
            else:
                print("Please input a number (valid range: " + str(min) + "-" + str(max) + ")")

    # for the main menu
    def menu(self, question, choices, verify): # return the user string. If verify is true, it has to be a valid choice
        print(question)
        for c in choices:
            print("[" + c[0] + "] " + c[1])
        while True:
            ch = input()
            if not verify:
                return ch
            for c in choices:
                if c[0] == ch:
                    return ch
            print("Invalid choice, try again: ")

    def printlast(self):
        msg = ""
        if self.lastfile is not None:
            msg = " (Last file: " + self.lastfile
        if self.lastentity is not None:
            if msg == "":
                msg = " (Last entity: " + self.lastentity + ")"
            else:
                msg = ", Last entity: " + self.lastentity + ")"
        elif msg != "":
            return msg + ")"
        return msg

    def exe(self, cmd):
        print(">" + cmd)
        os.system(cmd)

    # main loop
    def loop(self):
        # MAIN MENU
        while True:
            s = self.menu("\nMain menu" + self.printlast(), [["0", "Compile"], ["1", "Build"], ["2", "Run"], ["3", "Build and Run"], ["4", "Import"], ["5", "Make"], ["6", "Clean workspace"], ["Any", "Exit"]], False)
            if s == "0":
                f = input("Input the file to compile: ")
                if f == "":
                    if self.lastfile is None: continue
                    f = self.lastfile
                self.exe(self.path + " -a --workdir=work  \"" + f + "\"")
                self.lastfile = f
            elif s == "1":
                e = input("Input the entity to build: ")
                if e == "":
                    if self.lastentity is None: continue
                    e = self.lastentity
                self.exe(self.path + " -e --workdir=work \"" + e + "\"")
                self.lastentity = e
            elif s == "2":
                r = input("Input the entity to run: ")
                if r == "":
                    if self.lastentity is None: continue
                    r = self.lastentity
                a = input("Parameter(s)? : ")
                self.exe(self.path + " -r --workdir=work \"" + r + "\" " + a)
                self.lastentity = r
            elif s == "3":
                e = input("Input the entity to build and run: ")
                if e == "":
                    if self.lastentity is None: continue
                    e = self.lastentity
                self.exe(self.path + " -e --workdir=work \"" + e + "\"")
                a = input("Parameter(s)? : ")
                self.exe(self.path + " -r --workdir=work \"" + e + "\" " + a)
                self.lastentity = e
            elif s == "4":
                f = input("Input the file(s) to import: ")
                if f == "": continue
                self.exe(self.path + " -i --workdir=work \"" + f + "\"")
            elif s == "5":
                m = input("Input the entity to make: ")
                if m == "":
                    if self.lastentity is None: continue
                    m = self.lastentity
                self.exe(self.path + " -m --workdir=work \"" + m + "\"")
                self.lastentity = m
            elif s == "6":
                self.exe(self.path + " --clean --workdir=work")
            else: # quit
                return False

    def start(self):
        # we start HERE
        print("GHDL quick use script v0.1")
        while self.loop(): # loop as long as loop() returns true
            pass

g = GHDL()
g.start()