import pyautogui
from time import sleep, time
import os
import shutil
        

class AutoguiCalibrate():

    def __init__(self):
        import os.path
        from os import path

        if os.path.isfile('coordinates.txt'):
            self.calibration_status = True
        else:
            self.calibration_status = False
            print("This is an ATE autogui configurator.")
            print("Design to determine the exact location of specific points to be automated.\n\n")
            print("Calibration begins now..\n\n")   
            with open('coordinates.txt', 'w') as f: pass
            self.save_coordinates()
        

    def initialize_dictionary(self):
        self.dict = {}

    def get_coordinates(self, target):
        input(f">> {target}. Press ENTER to get coordinates.")
        x,y = pyautogui.position()
        self.dict[target] = x,y

    def get_coordinates_manual(self, target):
        input(f">> {target}. Press ENTER to get coordinates.")
        x,y = pyautogui.position()
        return x,y

    def save_coordinates(self):
        if self.calibration_status == False:
            self.calibrate_autogui()
            with open('coordinates.txt', 'w') as f:
                f.write(str(self.dict))

    def recalibrate(self):
        print("Recalibrating...")
        self.calibration_status = False
        self.save_coordinates()
        print("Recalibration complete.")

    def load_coordinates(self):
        with open('coordinates.txt', 'r') as f:
            str_dict = f.read()
            self.dictionary = eval(str_dict)
            return self.dictionary

    def moveTo(self, target):
        if type(target) == type((0,0)):
            pyautogui.moveTo(target)
        else:
            self.dictionary = self.load_coordinates()
            x,y = self.dictionary[target]
            pyautogui.moveTo(x,y)

    def click(self, target):
        self.moveTo(target)
        pyautogui.click()

    def change_value(self, target, value):
        self.click(target)
        self.ctrl_a()
        pyautogui.press('backspace', presses=1)
        pyautogui.write(f"{value}")
    
    
    def ctrl_a(self):
        pyautogui.keyDown('ctrl')
        sleep(0.1)
        pyautogui.press('a')
        sleep(0.1)
        pyautogui.keyUp('ctrl')

    def alt_tab(self):
        pyautogui.keyDown('alt')
        sleep(0.2)
        pyautogui.press('tab')
        sleep(0.2)
        pyautogui.keyUp('alt')

    def esc(self):
        pyautogui.press('esc')

    def enter(self):
        pyautogui.press('enter')




    # recalibrate -> save_coordinates -> calibrate_autogui() -> initialization

    def operation(self):
        """
        ENTER REFERENCE HERE FOR EASY USAGE OF AUTOGUI
        
        commands below are customizable depending on user's usage.
        
        """

        # FOR FLICKER
        self.select_flicker_app = self.get_coordinates('select_flicker_app')
        self.flicker_button = self.get_coordinates('flicker_button')
        # self.select_ate_app = self.get_coordinates('select_ate_app')
        self.select_file_tab = self.get_coordinates('select_file_tab')
        self.select_save_as = self.get_coordinates('select_save_as')
        

    
    
    def calibrate_autogui(self):

        """FLICKER COORDINATES SETTINGS"""
        self.initialize_dictionary()
        self.operation()