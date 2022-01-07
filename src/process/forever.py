#!/usr/bin/python
from subprocess import Popen

while True:
    print("\033[96m\nStarting bot with infinite execution!\n\033[0m")
    p = Popen("python .\index.py", shell=True)
    p.wait() 