from powi.equipment import convert_argv_to_int_list
from tkinter.constants import END
import pyautogui
from time import time, sleep
import sys

led = int(sys.argv[1])

"""RELAY OPTIONS"""

from powi.equipment import *

board = pyfirmata.Arduino('COM8')
iterator = util.Iterator(board)
iterator.start()

RELAY1 = board.get_pin('d:10:o')
RELAY2 = board.get_pin('d:9:o')
RELAY3 = board.get_pin('d:8:o')

def led_46V():
    # print("46V LED")
    RELAY1.write(1)
    RELAY2.write(0)
    RELAY3.write(0)

def led_36V():
    # print("36V LED")
    RELAY1.write(0)
    RELAY2.write(1)
    RELAY3.write(0)

def led_24V():
    # print("24V LED")
    RELAY1.write(0)
    RELAY2.write(0)
    RELAY3.write(1)

def NL():
    # print("NL")
    RELAY1.write(0)
    RELAY2.write(0)
    RELAY3.write(0)


if led == 46: led_46V()
elif led == 36: led_36V()
elif led == 24: led_24V()
elif led == 0: NL()
else: print("Invalid LED.")