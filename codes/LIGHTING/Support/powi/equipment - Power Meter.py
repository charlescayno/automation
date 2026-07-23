from functools import wraps
from math import isnan
from time import sleep, time
from abc import ABC, abstractmethod
import atexit
import os
import sys
import shutil


try:
    from pyfirmata import Arduino, util
    import pyfirmata
    import pyvisa
    import numpy as np
    from gtts import gTTS
    import sys
    from playsound import playsound
    import pandas as pd
    from openpyxl import Workbook
    import openpyxl
    from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
    from openpyxl.utils import get_column_letter
    import os
    import matplotlib.pyplot as plt


except:
    import pip
    # pip.main(['install','pyqt5'])
    # pip.main(['install','pyinstaller'])
    # pip.main(['install','pyautogui'])
    # pip.main(['install','pyfirmata'])
    pip.main(['install', 'pyvisa'])
    pip.main(['install','pandas'])
    pip.main(['install','openpyxl'])
    pip.main(['install','opencv-python'])
    pip.main(['install','matplotlib'])
    pip.main(['install','numpy'])
    pip.main(['install', 'gTTS'])
    pip.main(['install', 'playsound'])

    # from pyfirmata import Arduino, util
    # import pyfirmata
    import pyvisa
    import numpy as np
    pass


## FOR FORMATTING WHEN TRANSFERRING DF TO EXCEL
from openpyxl.styles import colors
from openpyxl.styles import Font, Color
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from openpyxl.styles import NamedStyle, Font, Border, Side
highlight = NamedStyle(name="highlight")
highlight.font = Font(name='Calibri', bold=False, size=11)
bd = Side(style='thin', color="000000")
highlight.alignment = Alignment(horizontal='center', vertical='center')
highlight.border = Border(left=bd, top=bd, right=bd, bottom=bd)




GPIB_NO = 0
PORT = 0

type_to_address = {
    'gpib': f'GPIB{GPIB_NO}',
    'lan': 'TCPIP',
    'usb': 'USB',
    'serial': 'ASRL'
    }

def reject_nan(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        for _ in range(10):
            response = func(*args, **kwargs)
            if not isnan(response):
                return response
            sleep(0.2)
        return None
    return wrapped

class Equipment(ABC):
    def __init__(self, address, comm_type='gpib', timeout=10000):
        rm = pyvisa.ResourceManager()
        print(rm.list_resources())

        if comm_type == 'serial':
            self.address = f'{type_to_address[comm_type]}{address}'
            print(self.address)
        else:
            self.address = f'{type_to_address[comm_type]}::{address}'
        self.timeout = timeout
        try:
            self.device = rm.open_resource(self.address)
            print(self.device.query('*IDN?'))
            self.device.timeout = self.timeout
            atexit.register(self.cleanup)
        except Exception as e:
            raise pyvisa.VisaIOError(e)
            
        self._id = 0

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                 '(address={self.address}, timeout={self.timeout})')

    @abstractmethod
    def cleanup(self):
        pass

    @property
    def id(self):
        self._id = self.write('*IDN?')
        return self._id

    def close(self):
        self.device.close()
    
    def write(self, command):
        response = None
        reply_available = False # CDO
        try:
            if "BDMM" in command: # CDO
                reply_available = True
                command = command.split(':')[1]

            if "?" in command:
                response = self.device.query(command).strip()
            else:
                self.device.write(command)

            if reply_available: # CDO
                self.device.read()
                reply_available = False

        except Exception as e:
            raise pyvisa.VisaIOError(e)

        return response


class PowerMeter(Equipment):
    def __init__(self, address, comm_type='gpib', timeout=10000):
        super().__init__(address, comm_type, timeout)

        self._voltage = 0
        self._current = 0
        self._power = 0
        self._pf = 0
        self._thd = 0
        self._integtime = 0
        # self.reset()

    def integrate(self, integration_time=60):
        self.write('INTEGRATE:RESET')
        self.write('INTEGRATE:MODE NORMAL')
        self.write(f'INTEGRATE:TIMER 0, {integration_time // 60}, {integration_time%60} ')
        self.write('INTEGRATE:START')
        self._integtime = integration_time

    def integration_done(self):
        return self.write('INTEGRATE:STATE?') == 'TIM'

    @property
    def integtime(self, integtime):
        return self._integtime
    
    @integtime.setter
    def integtime(self, integtime):
        self._integtime = integtime

    @property
    @reject_nan
    def voltage(self):
        self.write('NUMERIC:ITEM1 U, 1')
        self._voltage = float(self.write('NUM:NORM:VAL? 1'))
        return self._voltage
        
    @property
    @reject_nan
    def current(self):
        self.write('NUMERIC:ITEM2 I, 1')
        self._current = float(self.write('NUM:NORM:VAL? 2'))
        return self._current
    
        if self._integtime == 0:
            self.write('NUMERIC:ITEM2 I, 1')
            self._current = float(self.write('NUM:NORM:VAL? 2'))
        else:
            while not self.integration_done:
                sleep(0.5)
            # print("integration successful")
            self.write('NUMERIC:ITEM8 AH, 1')
            self._current = float(self.write('NUM:NORM:VAL? 8'))
            # print(self._current)
            self.write('INTEGRATE:RESET')
            
            self._integtime = 0        
        return self._current

    @property
    @reject_nan
    def power(self):
        if self._integtime == 0:
            self.write('NUMERIC:ITEM3 P, 1')
            self._power = float(self.write('NUM:NORM:VAL? 3'))
        else:
            while not self.integration_done:
                sleep(0.5)
            print("integration successful")
            self.write('NUMERIC:ITEM6 WH, 1')
            self._power = float(self.write('NUM:NORM:VAL? 6')) * 3600 / self._integtime
            self.write('INTEGRATE:RESET')
            self._integtime = 0       
            print(f"{self._power}")
        return self._power

    @property
    @reject_nan
    def pf(self):
        self.write('NUMERIC:ITEM4 lambda, 1')
        self._pf = float(self.write('NUM:NORM:VAL? 4'))
        return self._pf

    @property
    @reject_nan
    def thd(self):
        self.write('NUMERIC:ITEM5 ITHD, 1')
        self._thd = float(self.write('NUM:NORM:VAL? 5'))
        return self._thd

    def set_current_range(self, amps):
        self.write(f':INPUT:CURRENT:RANGE {amps}A')


    def get_harmonics(self):
        """
            returns: list of float harmonic content (mA)
            
            PS. Not fully tested please refer to the standard.
        """
        self.write("HARMONICS:DISPLAY ON")
        self.write("NUMERIC:LIST:CLEAR ALL")
        self.write("NUMERIC:LIST:ITEM2 I,1")
        sleep(3)
        a = self.write("NUMeric:LIST:VALue? 2").split(',NAN,')[1].split(',')
        sleep(3)
        harmonic_content = []
        for i in a:
            harmonic_content.append(float(i)*1000)

        percent_content = []
        for i in range(len(harmonic_content)):
            percent_content.append(float(f"{(harmonic_content[i]*100/harmonic_content[0]):2f}"))
        print(percent_content)

        pin = float(f"{self.power:.6f}")

        return harmonic_content, percent_content

    def voltage_range(self, max=150):
        """
        Function
            Sets or queries the voltage range.
        Syntax
            [:INPut]:VOLTage:RANGe {<Voltage>}
            [:INPut]:VOLTage:RANGe?
            • When the crest factor is set to 3
                <Voltage> = 15, 30, 60, 150, 300, 600(V)
            • When the crest factor is set to 6 or 6A
                <Voltage> = 7.5, 15, 30, 75, 150, 300(V)
        Example :INPUT:VOLTAGE:RANGE 600V
            :INPUT:VOLTAGE:RANGE?
            -> :INPUT:VOLTAGE:RANGE 600.0E+00
        """
        self.write(f":INPUT:VOLTAGE:RANGe {max}V")


    def current_range(self, max=2):
        """
        <Current> = 5, 10, 20, 50, 100, 200, 500(mA),
        1, 2, 5, 10, 20(A) (WT310E)
        """
        self.write(f":INPut:CURRent:RANGe {max}")

    

    def reset(self):
        self.write('*RST')
        # self.current_range()

    def cleanup(self):
        self.close()










if __name__ == '__main__':
    pass


