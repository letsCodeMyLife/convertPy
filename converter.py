import shutil
import zipfile
import subprocess
import os
import consolePrint
import sys
import time

sep = os.sep

WIN = 0; LINUX = 1; MAC = 2

if "PYTHONPATH" in os.environ:
    PYTHONPATH = os.environ["PYTHONPATH"]

    if (PYTHONPATH[0] == "'" or PYTHONPATH[0] == '"') \
       and (PYTHONPATH[-1] == "'" or PYTHONPATH[-1] == '"'):
        PYTHONPATH = PYTHONPATH[1:]
        PYTHONPATH = PYTHONPATH[:-1]
else:
    PYTHONPATH = sys.path[-2]

def _createExecuter(outFile, inFile, withWindow, icon, pwd, x64, upx):
    consolePrint.printGreen("[+] beginning to make the executable")

    if not sys.platform == "win32":
        consolePrint.printYellow("[#] Your OS is not prepared to execute the file that have to be compiled.\nYou can ignore this warning.")
    
    if withWindow:
        with open("executers" + sep + "main.bat", "w") as file:
            file.write("python" + sep + "python.exe {}".format(os.path.split(inFile)[1]))
    else:
        with open("executers" + sep + "main.bat", "w") as file:
            file.write("python" + sep + "pythonw.exe {}".format(os.path.split(inFile)[1]))

    command = ["executers" + sep + "converter.exe", "/bat", "executers" + sep + \
                            "main.bat", "/exe", "executers" + sep + os.path.split(outFile)[1],
               "/invisible"]
    if icon:
        consolePrint.printGreen("[+] ICON: " + icon)
        command.append("/icon")
        command.append(icon)

    if pwd:
        consolePrint.printGreen("[+] A password is specified")
        consolePrint.printYellow("[#] WARNING: The password can be easily broken!")
        command.append("/password")
        command.append(pwd)

    if x64:
        consolePrint.printGreen("[+] The application is created for 64 bit processors")
        consolePrint.printYellow("[#] The application cant run on 32 bit processors!")
        command.append("/x64")

    if upx:
        consolePrint.printGreen("[+] The executable will be compressed with UPX")
        consolePrint.printYellow("[#] UPX can irritate some Antivirusses!")
        command.append("/upx")

    file = subprocess.Popen(command)
    file.communicate()

    if not os.path.isfile(os.path.dirname(__file__) + sep + "executers" + sep + os.path.split(outFile)[1]):
        consolePrint.printRed("[-] FATAL ERROR: The file can not be converted!!")

    consolePrint.printGreen("[+] deleting old batch file")
    os.remove("executers" + sep + "main.bat")

def _copyPython(outFile):
    shutil.copytree(PYTHONPATH, os.path.dirname(outFile) + sep + "python")

def convert(inFile, outFile, putZip, withWindow, toDestroy, icon=False,
            pwd=False, x64=False, upx=False):
    toDestroy.destroy()
    time1 = time.time()
    _createExecuter(outFile, inFile, withWindow, icon, pwd, x64, upx)
    consolePrint.printGreen("[+] Created executable!")
    consolePrint.printGreen("[+] Beginning to copy runtime files into the folder! This will take a while.")
##    _copyPython(outFile)
    shutil.copyfile("executers" + sep + os.path.split(outFile)[1], outFile)
    shutil.copyfile(inFile, os.path.dirname(outFile) + sep + os.path.split(inFile)[1])
    consolePrint.printGreen("[+] Ready with the process! {}".format("It has take " + str(time.time() - time1) + "seconds"))
