#!/usr/sbin/python

import sys, os, re

PS1 = r"[\W] $ "
PATH = os.getenv("PATH")

def writePrompt(ps1):
    basename = os.path.basename(os.getcwd())
    ps1 = PS1.replace(r"\W", basename)
    os.write(1, ps1.encode("utf-8"))
    os.write(1, b'\n')

def cd(path):
    os.chdir(path)

def exit():
    os.write(1, b"exit\n")
    sys.exit(0)


