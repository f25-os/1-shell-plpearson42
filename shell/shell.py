#!/usr/sbin/python

import sys
import os
import re

PS1 = r" [\W] $ "
PATH = re.split(":",os.environ["PATH"])
MAX_READ = 1024


def tokenIn(cmd):
    return re.split(" ", cmd.decode("utf-8"))[:-1]


def writePrompt():
    basename = os.path.basename(os.getcwd())
    ps1 = PS1.replace(r"\W", basename)
    os.write(1, ps1.encode("utf-8"))
    os.write(1, b'\n')


def cd(path):
    os.chdir(path)


def exit():
    os.write(1, b"exit\n")
    sys.exit(0)


def run(tokens):
    isParent = os.fork()
    if isParent != 0:
        os.wait()
        return 0
    else:
        for path in PATH:
            try:
                os.execv("%s/%s"%(path, tokens[0]), tokens[1:])
            except:
                pass
    return 1


while 1:
    writePrompt()
    cmd = os.read(0, MAX_READ)
    tokens = tokenIn(cmd)
    print(tokens)
    if tokens[0] == "exit":
        exit()
    elif tokens[0] == "cd":
        cd(tokens[1])
    else:
        if run(tokens) != 0:
            os.write(2, b"command not found")
        continue






    
    



















































