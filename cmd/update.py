from colorama import init, Fore

import io
import yaml
import shutil
import subprocess
import os
import git
import sys

sys.stdout = io.TextIOWrapper(
    sys.stdout.detach(),
    encoding=sys.stdout.encoding,
    errors='ignore',
    line_buffering=True
)
init()

pathSource = './clone-repo/'


def deleteRecursive(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, 0o777)
            os.remove(filename)
        for name in dirs:
            filename = os.path.join(root, name)
            os.chmod(filename, 0o777)
            os.rmdir(filename)
    shutil.rmtree(path)


def copyRecursive(src, dest):
    shutil.copytree(src, dest, dirs_exist_ok=True)


def success():
    print(Fore.GREEN + '🎉 Updated files!')
    print('Your version is now:', localVersion())
    print('\nRun: python index.py')
    print('Run without stopping (Windows): .\start.bat')
    print('Run without stopping (Linx): ./start.sh', Fore.RESET)

def updateFiles(path):
    print('🔃 Updating files...')
    copyRecursive(path, './')
    deleteRecursive(path)


def localVersion():
    try:
        fileVersion = open("./config/version.yaml", 'r')
        streamVersion = yaml.safe_load(fileVersion)
        version = streamVersion['version']
        app = version['app']
        fileVersion.close()
    except FileNotFoundError:
        app = "Not found, retry file update!"

    return app


def run():
    print('------------------------------------------------------------------')
    try:
        version = subprocess.check_output(["git", "version"]).strip().decode()
        print(Fore.GREEN + 'Git installed:', version, Fore.RESET)
        try:
            print('Cloning repository https://github.com/newerton/bombcrypto-bot.git')
            git.Repo.clone_from(
                'https://github.com/newerton/bombcrypto-bot.git', './clone-repo', branch='main')
            deleteRecursive(pathSource + '.git/')
        except git.exc.GitCommandError:
            print(Fore.GREEN + 'Repository cloned', Fore.RESET)

        updateFiles(pathSource)
        print('------------------------------------------------------------------')
    except FileNotFoundError:
        print(Fore.RED + 'Git not found' + Fore.RESET)
        print(Fore.RED + 'To use auto-update, you need to install Git on your machine' + Fore.RESET)
        if os.name == 'nt':
            print(
                Fore.GREEN + 'Download Git for Windows: https://gitforwindows.org/' + Fore.RESET)
        elif os.name == 'posix':
            print(
                Fore.GREEN + 'Install Git for unix system: sudo apt update && sudo apt install git' + Fore.RESET)

        print('------------------------------------------------------------------')
        exit()



if __name__ == '__main__':
    globals()[sys.argv[1]]()
