import os
import queue
import msvcrt
import json
from pynput import keyboard

terminalSize = 0
startText = 'LockBox'
currentMenu = 0
listener = None
actionQueue = queue.Queue()

def on_press(key):
    try:
        HandleInput(key.char)
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def HandleInput(key):
    global currentMenu
    match currentMenu:
        case 0:
            print("Current Menu: 0 is recognized")
            match key:
                case "e":
                    actionQueue.put("exit")
                case "l":
                    actionQueue.put("password_list")
                case "a":
                    actionQueue.put("add_password")
                case _:
                    print("Invalid Key pressed")
        case 1:
            match key:
                case "c":
                    actionQueue.put("main_menu")
                case "e":
                    actionQueue.put("exit")
        case 2:
            match key:
                case "c":
                    actionQueue.put("main_menu")
                case "e":
                    actionQueue.put("exit")

def MainMenu():
    global currentMenu
    currentMenu = 0
    os.system("cls")
    print("LockBox")
    print("1. See Password List (L)")
    print("2. Add Password (A)")
    print("3. Exit (E)")

def PasswordList(pwdDict):
    global currentMenu
    currentMenu = 1
    os.system("cls")
    print("Password List")
    for name, pwd in pwdDict.items():
        print(f"{name}: {pwd}")

def AskForPwd():
    pwd = input("Enter Password: ")
    if pwd == "":
        print("Password is empty. Do you want to cancel? (Y = Yes / N = No):")
        answer = input()
        if answer.lower() == "y":
            return None
        elif answer.lower() == "n":
            return AskForPwd()
    else:
        return pwd

def AskForName():
    name = input("Enter Password Name (Leave empty to cancel): ")
    return name

def CheckIfNameExists(name, pwdDict):
    if name in pwdDict:
        overwrite = input("Name already exists, do you want to overwrite? (y = yes / n = no")
        if overwrite.lower() == "y":
            return name
        elif overwrite.lower() == "n":
            print("Please input new Password Name: ")
            AskForName()
        else:
            print("Invalid answer")
            AskForName()
    else:
        return name

def AddPassword(pwdDict):
    global currentMenu
    currentMenu = 2
    os.system("cls")
    listener.stop()
    while msvcrt.kbhit():
        msvcrt.getwch()
    name = AskForName()
    if name == "":
        StartListener()
        MainMenu()
        return pwdDict
    CheckIfNameExists(name, pwdDict)
    pwd = AskForPwd()
    if pwd == None:
        StartListener()
        MainMenu()
        return pwdDict
    pwdDict[name] = pwd
    StartListener()
    MainMenu()
    return pwdDict

def StartListener():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

def LoadPasswords(pwdDict):
    try:
        with open("passwords.json", "r") as file:
            pwdDict = json.load(file)
            return pwdDict
    except FileNotFoundError:
            return pwdDict

def SavePasswords(pwdDict):
    with open("passwords.json", "w") as file:
        json.dump(pwdDict, file)

def Main():
    pwdDict = {}
    pwdDict = LoadPasswords(pwdDict)

    global terminalSize
    terminalSize = os.get_terminal_size()
    width = terminalSize.columns

    os.system("cls")

    halfWidth = width // 2
    for i in range(halfWidth):
        print("-", end="")
    print(" LockBox")
    MainMenu()
    StartListener()

    while True:
        action = actionQueue.get()
        match action:
            case "exit":
                os.system("cls")
                while msvcrt.kbhit():
                    msvcrt.getwch()
                exit()
            case "main_menu":
                MainMenu()
            case "password_list":
                PasswordList(pwdDict)
            case "add_password":
                pwdDict = AddPassword(pwdDict)
                SavePasswords(pwdDict)
Main()
