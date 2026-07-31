from powi.equipment import Equipment, reject_nan
from functools import wraps
from math import isnan
from time import sleep, time
from abc import ABC, abstractmethod
# import atexit
# import os
# # import sys
# import shutil
# from pyfirmata import Arduino, util
# import pyfirmata
import pyvisa
import numpy as np
# from gtts import gTTS
# from playsound import playsound

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
            self.write('INTEGRATE:RESET')
            self.write('NUMERIC:ITEM6 WH, 1')
            self._power = float(self.write('NUM:NORM:VAL? 6')) * 3600 / self._integtime        
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

    

    def reset(self):
        self.write('*RST')

    def cleanup(self):
        self.close()
