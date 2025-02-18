"""
Automatically change IP address every second
"""
import sys
import os
from colorama import Fore, init
from time import sleep
import ctypes
from shutil import which

init(autoreset=True)

def term():
    os.system("clear" if os.name == "posix" else "cls")

def rootCheck():
    term()
    if os.name == "posix":
        if os.geteuid() != 0:
            sys.exit(Fore.RED + "[!] You must run this script as root." + Fore.RESET)
    elif os.name == "nt":
        if not ctypes.windll.shell32.IsUserAnAdmin():
            sys.exit(Fore.RED + "[!] You must run this as admin." + Fore.RESET)

def requiredPackages():
    term()
    packages = ["tor", "tornet"]
    missing = []
    for package in packages:
        if which(package) is None:
            print(Fore.RED + f"[!] Error! {package} is not installed." + Fore.RESET)
            missing.append(package)
    if missing:
        sys.exit(Fore.RED + "Still Error? Please install manually: " + ", ".join(missing) + Fore.RESET)

def changeIP():
    change = input(Fore.RED + "Do you want to change your IP address? (y/n): " + Fore.RESET).strip().lower()
    if change in ["yes", "y"]:
        try:
            duration = int(input(Fore.RED + "How many seconds: " + Fore.RESET).strip())
            print("[+] Changing your IP...")
            sleep(1)
            os.system("systemctl start tor")
            os.system(f"tornet --interval {duration} --count 0")
        except ValueError:
            print(Fore.RED + "[!] Invalid input. Please enter a number." + Fore.RESET)

def main():
    rootCheck()
    requiredPackages()
    changeIP()

if __name__ == '__main__':
    main()
