import os
import sys
import json
import signal

class GHDL():
    def __init__(self):
        self.ghdlpath = "ghdl-0.36\\bin\\ghdl.exe"
        self.workpath = "workspace"
        self.current = None
        self.base = os.getcwd()

        signal.signal(signal.SIGINT, self.sigint)
        self.load()

    def sigint(self, sig, frame):
        print('\n')

    def load(self):
        try:
            with open('settings.json') as f:
                data = json.load(f)
                if 'ghdl_path' in data: self.ghdlpath = data['ghdl_path']
                if 'work_path' in data: self.workpath = data['work_path']
                if 'last_project' in data:
                    if self.isDir(self.workpath + "\\" + data['last_project']):
                        self.current = data['last_project']
                return True
        except Exception as e:
            print('load() Error:', e)
            return False
        return False

    def save(self, sortBackup=True):
        try:
            with open('settings.json', 'w') as f:
                data = {}
                data['ghdl_path'] = self.ghdlpath
                data['work_path'] = self.workpath
                data['last_project'] = self.current
                json.dump(data, f)
            return True
        except Exception as e:
            print('save() Error:', e)
            return False

        if not self.isDir(self.workpath):
            os.mkdir(self.workpath)

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

    def exe(self, cmd):
        self.projectIn()
        self.workDirCheck('work')
        cmd = self.getExeStr() + " " + cmd
        print(">" + cmd)
        os.system(cmd)
        self.projectOut()

    def getDir(self):
        files = os.listdir(self.workpath)
        res = []
        for f in files:
            if os.path.isdir(os.path.join(os.path.abspath(self.workpath), f)):
                res.append(f)
        res.sort()
        return res

    def isDir(self, folder):
        try:
            return os.path.isdir(folder)
        except:
            return False

    def workDir(self):
        return self.workpath + "\\" + self.current

    def workDirCheck(self, folder):
        if not self.isDir(folder): 
            os.mkdir(folder)

    def projectIn(self):
        os.chdir(self.workpath + "\\" + self.current)

    def projectOut(self):
        os.chdir(self.base)

    def getExeStr(self):
        exe = self.base
        if not exe.endswith("\\"): exe = exe + "\\"
        return "\"" + exe + self.ghdlpath + "\""

    def checkInputMenu(self, s):
        if s == "0":
            d = input("Input the project name (Leave blank to cancel): ")
            if d == "":
                return True
            if self.isDir(self.workpath + "\\" + d):
                print("Folder '" + d + "' already exists")
                return True
            try:
                os.mkdir(self.workpath + "\\" + d)
                self.current = d
                self.save()
                print("Folder '" + d + "' created and set")
            except Exception as e:
                print("Error:", e)
        elif s == "1":
            d = input("Input the project name (Leave blank to cancel): ")
            if d == "":
                return True
            if self.isDir(self.workpath + "\\" + d):
                self.current = d
                self.save()
                print("Project '" + d + "' is set")
                return True
            else:
                print("Folder '" + d + "' not found")
        else:
            return False
        return True

    # main loop
    def loop(self):
        # MAIN MENU
        while True:
            if self.current is None or not self.isDir(self.workpath + "\\" + self.current):
                s = self.menu("\nMain menu", [["0", "New project"], ["1", "Select project"], ["Any", "Exit"]], False)
                if not self.checkInputMenu(s):
                    return
            else:
                s = self.menu("\nMain menu - Current Project: " + self.current, [["0", "New project"], ["1", "Select project"], ["2", "Compile File (-a)"], ["3", "Build Entity (-e)"], ["4", "Run Entity (-r)"], ["5", "Build and Run Entity (-e, -r)"], ["6", "Import (-i)"], ["7", "Make Entity (-m)"], ["8", "Clean Workspace (--clean)"], ["Any", "Exit"]], False)
                if self.checkInputMenu(s):
                    continue
                elif s == "2":
                    f = input("Input the file to compile: ")
                    if f == "":
                        continue
                    self.exe("-a --workdir=work " + f)
                elif s == "3":
                    e = input("Input the entity to build: ")
                    self.exe("-e --workdir=work "+ e)
                elif s == "4":
                    e = input("Input the entity to run: ")
                    if e == "": continue
                    a = input("Parameter(s)? : ")
                    self.exe("-r --workdir=work " + e + " " + a)
                elif s == "5":
                    e = input("Input the entity to build and run: ")
                    if e == "": continue
                    self.exe("-e --workdir=work " + e)
                    a = input("Parameter(s)? : ")
                    self.exe("-r --workdir=work " + e + " " + a)
                elif s == "6":
                    f = input("Input the file(s) to import: ")
                    if f == "": continue
                    self.exe("-i --workdir=work " + f)
                elif s == "7":
                    m = input("Input the entity to make: ")
                    if m == "": continue
                    self.exe("-m --workdir=work " + m)
                elif s == "8":
                    self.exe("--clean --workdir=work")
                else: # quit
                    return

    def start(self):
        # we start HERE
        print("GHDL quick use script v0.3b")
        while self.loop(): # loop as long as loop() returns true
            pass

g = GHDL()
g.start()
g.save()