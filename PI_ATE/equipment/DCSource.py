from powi.equipment import Equipment, reject_nan
from functools import wraps
from math import isnan
from time import sleep, time
from abc import ABC, abstractmethod
import atexit
import os
import sys
import shutil
from pyfirmata import Arduino, util
import pyfirmata
import pyvisa
import numpy as np
from gtts import gTTS
from playsound import playsound
class DCSource(Equipment):
    def __init__(self, address, comm_type='gpib', timeout=10000):
        super().__init__(address, comm_type, timeout)

        self._voltage = 0
        self._current = 0
        self._cv = 0
        self._cc = 0

    def turn_on(self):
        self.write('CONF:OUTP ON')
        print("CONF:OUTP ON")

    def turn_off(self):
        self.write('CONF:OUTP OFF')
        print("CONF:OUTP OFF")

    @property
    def voltage(self):
        self._voltage = self.write('MEAS:VOLT?')
        return self._voltage

    @property
    def current(self):
        self._current = self.write('MEAS:CURR?')
        return self._current

    # @voltage.setter
    # def voltage(self, voltage):
    #     self._voltage = voltage

    @property
    def cv(self):
        return self._cv

    @property
    def cc(self):
        return self._cc

    @cv.setter
    def cv(self, cv):
        self._cv = cv
        self.write(f'VOLT {self._cv}')

    @cc.setter
    def cc(self, cc):
        self._cc = cc
        self.write(f'CURR {self._cc}')

    def cleanup(self):
        # self.turn_off()
        self.close()
