import sys
import pyautogui
from time import sleep, time
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list
from powi.equipment import *
from time import sleep, time
import os
import cv2

"""GENERAL AUTOGUI FUNCTIONS"""
def give_loc(filename='binno_tab'):
    return pyautogui.locateOnScreen(f'image_autogui_library\{filename}.png', confidence=0.8)

def click(coords):
    pyautogui.moveTo(coords)
    pyautogui.click()

def change_value(coords, val):
    click(coords)
    pyautogui.press('backspace', presses=3)
    pyautogui.write(f"{val}")

def give_loc_rel(filename='binno_tab', relative_width=0.75):
    x,y,w,h = give_loc(filename)
    x = x + relative_width*w
    y = y + h/2
    return x,y

def add_relative_y(anchor, add_relative_y=0.1):
    x,y = anchor
    y += add_relative_y
    return x,y

"""I2C Autogui Variables"""

print("Initialize I2C Autogui Variables.")
print()

binno_tab = give_loc('binno_tab')

i2c_send_textbox = give_loc_rel('i2c_send', 0.5)
i2c_send_write = give_loc_rel('i2c_send', 0.75)

i2c_cp_dropdown = give_loc_rel('i2c_cp_setting', 0.56)
i2c_cp_0 = add_relative_y(i2c_cp_dropdown, add_relative_y=24)
i2c_cp_1 = add_relative_y(i2c_cp_0, add_relative_y=18)
i2c_cp_2 = add_relative_y(i2c_cp_1, add_relative_y=18)
i2c_cp_3 = add_relative_y(i2c_cp_2, add_relative_y=18)
i2c_cp_write = give_loc_rel('i2c_cp_setting', 0.75)

initialize_com_port = give_loc('initialize_com_port')

"""I2C Autogui Functions"""
def change_cp(cp):
    click(i2c_cp_dropdown)
    if cp == 0: click(i2c_cp_0)
    elif cp == 1: click(i2c_cp_1)
    elif cp == 2: click(i2c_cp_2)
    elif cp == 3: click(i2c_cp_3)
    else: input("Invalid CP!")
    click(i2c_cp_write)

def set_i2c_bit(cmdbit):
    change_value(i2c_send_textbox, cmdbit)
    click(i2c_send_write)

# scope = Oscilloscope("10.125.10.170")

# scope.run()
def a(b):
    change_cp(0)
    set_i2c_bit(0)
    sleep(2)
    change_cp(0)
    set_i2c_bit(254)
    sleep(5)

    change_cp(0)
    set_i2c_bit(0)
    sleep(b)
    change_cp(0)
    set_i2c_bit(254)
    sleep(5)


a(1)
a(5)
a(10)





# input("enter to continue")