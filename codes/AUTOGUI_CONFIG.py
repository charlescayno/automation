import pyautogui
from time import sleep, time

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


    def ac_control(self):
        self.ac_on = self.get_coordinates('AC_ON')
        self.ac_off = self.get_coordinates('AC_OFF')
        self.vrms_gui = self.get_coordinates('VRMS')
        self.freq_gui = self.get_coordinates('FREQ')
        return self.ac_on, self.ac_off, self.vrms_gui, self.freq_gui

    def soak_settings(self):
        self.soak_time = self.get_coordinates('SOAK_TIME')
        self.delay_per_line = self.get_coordinates('DELAY_PER_LINE')
        self.delay_per_load = self.get_coordinates('DELAY_PER_LOAD')
        self.integration_time = self.get_coordinates('INTEGRATION')
        return self.soak_time, self.delay_per_line, self.delay_per_load, self.integration_time

    def test_selection(self):
        self.select_test = self.get_coordinates('SELECT_TEST')
        self.select_test_option = self.get_coordinates('SELECT_TEST_OPTION')
        self.select_test_digital_control = self.get_coordinates('SELECT_TEST_DIGITAL_CONTROL')

    def multiprotocol_control(self, type='binno'):
        self.initialize_com_port = self.get_coordinates('INITIALIZE_COM_PORT')
        self.activate_load_settings_for_ate = self.get_coordinates('ACTIVATE_LOAD_SETTINGS_FOR_ATE')
        self.activate_load_settings_for_ate_ok_button = self.get_coordinates('ACTIVATE_LOAD_SETTINGS_FOR_ATE_OK_BUTTON')
        self.activate_load_settings_for_ate_test_type = self.get_coordinates('ACTIVATE_LOAD_SETTINGS_FOR_ATE_TEST_TYPE')
        self.multiprotocol_control_exit_button = self.get_coordinates('MULTIPROTOCOL_CONTROL_EXIT_BUTTON')

        if type == 'binno':
            self.binno_tab = self.get_coordinates('BINNO_TAB')
            self.i2c_send_write_bit = self.get_coordinates('I2C_SEND_WRITE_BIT')
            self.i2c_send_write_button = self.get_coordinates('I2C_SEND_WRITE_BUTTON')
        if type == 'rheostat':
            self.rheostat_tab = self.get_coordinates('RHEOSTAT_TAB')
            self.rheostat_manual_change = self.get_coordinates('RHEOSTAT_MANUAL_CHANGE')
            self.rheostat_set_resistance_button = self.get_coordinates('RHEOSTAT_SET_RESISTANCE_BUTTON')
            self.rheostat_settings_start = self.get_coordinates('RHEOSTAT_SETTINGS_START')
            self.rheostat_settings_end = self.get_coordinates('RHEOSTAT_SETTINGS_END')
            self.rheostat_settings_step_size = self.get_coordinates('RHEOSTAT_SETTINGS_STEP_SIZE')
            


    def calibrate_autogui(self):
        self.initialize_dictionary()
        self.ac_control()
        self.soak_settings()
        # self.multiprotocol_control('binno')
        self.multiprotocol_control('rheostat')

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
        pyautogui.press('backspace', presses=3)
        pyautogui.write(f"{value}")
    
    def change_rheostat_settings(self, start, end, step_size):
        self.dictionary = self.load_coordinates()
        self.change_value(self.dictionary['RHEOSTAT_SETTINGS_START'], start)
        self.change_value(self.dictionary['RHEOSTAT_SETTINGS_END'], end)
        self.change_value(self.dictionary['RHEOSTAT_SETTINGS_STEP_SIZE'], step_size)
    
    def change_rheostat(self, value):
        self.dictionary = self.load_coordinates()
        self.click('INITIALIZE_COM_PORT')
        self.change_value(self.dictionary['RHEOSTAT_MANUAL_CHANGE'], value)
        self.click('RHEOSTAT_SET_RESISTANCE_BUTTON')
    
    def alt_tab(self):
        pyautogui.keyDown('alt')
        sleep(0.2)
        pyautogui.press('tab')
        sleep(0.2)
        pyautogui.keyUp('alt')








# calibrate_autogui()
