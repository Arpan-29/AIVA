import pydirectinput as P
import keyboard
import time
import pyautogui as A

def click(x, y):

    # x = int(x / 1.25)
    # y = int(y / 1.25)

    P.moveTo(x, y)
    print(x, y)
    P.mouseDown()
    time.sleep(0.01)
    P.mouseUp()

    time.sleep(0.5)

def rightClick(x, y):

    move(x, y)
    P.rightClick()
    time.sleep(0.5)

def move(x, y):

    P.moveTo(x, y)
    time.sleep(0.5)

def press(key):

    P.keyDown(key)
    time.sleep(0.01)

def release(key):

    P.keyUp(key)
    time.sleep(0.01)

def pressOnce(key):

    P.press(key)

def write(str):

    for ch in str:
        pressOnce(ch)

    time.sleep(0.05)
