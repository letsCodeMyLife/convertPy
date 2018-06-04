import sys

canPrint = True

def printRed(string):
    if canPrint:
        print("\x1b[31m{}\x1b[0m".format(string))
    else:
        print(string)

def printYellow(string):
    if canPrint:
        print("\x1b[33m{}\x1b[0m".format(string))
    else:
        print(string)

def printGreen(string):
    if canPrint:
        print("\x1b[32m{}\x1b[0m".format(string))
    else:
        print(string)

if sys.version_info[0] > 2:
    try:
        import colorama
        colorama.init()
    except:
        canPrint = False
