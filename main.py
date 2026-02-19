import os
from pynput import keyboard

terminalSize = 0
startText = 'LockBox'
currentMenu = 0
listener = None
pwdDict = dict(name = "", pwd = "")

def on_press(key):
    #try:
    #    print(f"Key {key} was pressed.")
    #except AttributeError:
    #    print(f"Special Key {key} was pressed")

    HandleInput(key.char)

def on_release(key):
    #print(f"Key {key} was released")
    if key == keyboard.Key.esc:
        return False

def HandleInput(key):
    global currentMenu
    match currentMenu:
        case 0:
            print("Current Menu: 0 is recognized")
            match key:
                case "e":
                    os.system("cls")
                    exit()
                case "l":
                    PasswordList()
                case "a":
                    AddPassword()
                case _:
                    print("Invalid Key pressed")
        case 1:
            match key:
                case "c":
                    MainMenu()
                case "e":
                    os.system("cls")
                    exit()
        case 2:
            match key:
                case "c":
                    MainMenu()
                case "e":
                    os.system("cls")
                    exit()

def MainMenu():
    global currentMenu
    currentMenu = 0
    os.system("cls")
    print("LockBox")
    print("1. See Password List (L)")
    print("2. Add Password (A)")
    print("3. Exit (E)")

def PasswordList():
    global currentMenu
    currentMenu = 1
    os.system("cls")
    print("Password List")
    print("Password 1")
    print("Password 2")

def AddPassword():
    global currentMenu
    global pwdDict
    currentMenu = 2
    os.system("cls")
    name = GetTextInput("Enter Password Name (Leave empty to cancel): ")
    pwdDict[name] = name
    print(pwdDict)

def HearForInput():
    global listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def GetTextInput(prompt):
    global listener
    listener.stop()
    text = input(prompt)
    HearForInput()
    return text

def Main():
    #Main Loop
    global terminalSize
    terminalSize = os.get_terminal_size()
    width = terminalSize.columns

    os.system("cls")

    halfWidth = width // 2
    for i in range(halfWidth):
        print("-", end="")
    print(" LockBox")
    MainMenu()
    #print("Console width:", width)
    HearForInput()

Main()
