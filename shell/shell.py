#!/usr/bin/python3

import sys
import os
import re

PS1 = r" [\W] $ "
PATH = re.split(":", os.environ["PATH"])
MAX_READ = 1024


def tokenIn(cmd):
    return re.split(r"[ \n]", cmd.decode()[:-1])


def writePrompt():
    basename = os.path.basename(os.getcwd())
    if os.getcwd() == os.environ["HOME"]:
        basename = '~'
    ps1 = PS1.replace(r"\W", basename)
    os.write(1, ps1.encode())
    return 0


def cd(args):
    if len(args) == 1:
        os.chdir(os.environ["HOME"])  # cd with no args takes you home
        return 0
    try:
        os.chdir(args[1])
    except FileNotFoundError:
        os.write(2, ("cd: %s: No such file or directory/n" % args[1]).encode())
        return 1
    except NotADirectoryError:
        os.write(2, ("cd: %s: Not a directory/n" % args[1]).encode())
        return 2


def exit(quietly = False):
    if not quietly:
        os.write(1, b"exit\n")
    sys.exit(0)


def run(args):
    id = os.fork()

    if id < 0:
        os.write(2, b"fork failed")
    elif id == 0:
        args = handleRedir(args)
        for dir in PATH:
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ)
            except FileNotFoundError:
                pass

        os.write(2, ("shell.py: %s: command not found\n" % args[0]).encode())
        exit(True)  # exit quietly from the child shell
    else:
        os.wait()
        return 0


def handleRedir(args):
    if ">" in args:
        redir = args.index(">")
        os.close(1)  # close STDOUT
        os.open(args[redir+1], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)
        args = args[:redir]  # truncate args to before redir
    return args


def handlePipe(args):
    # Placeholder
    return args


while 1:
    writePrompt()
    cmd = os.read(0, MAX_READ)
    args = tokenIn(cmd)
    if args[0] == '':
        continue
    elif args[0] == "exit":
        exit()
    elif args[0] == "cd":
        cd(args)
    else:
        run(args)
