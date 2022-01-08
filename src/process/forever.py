#!/usr/bin/python
from subprocess import Popen
from colorama import init, Fore
init()

while True:
    print(Fore.MAGENTA + 'Starting bot with infinite execution!' + Fore.RESET)
    p = Popen("python .\index.py", shell=True)
    p.wait() 