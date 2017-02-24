import os
import platform


def clear_console():
    OS = platform.system()
    if OS == "Windows":
        os.system('cls')
    elif OS == "Linux":
        os.system('clear')

if __name__ == "__main__":
    clear_console()