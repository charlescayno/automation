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

class ElectronicLoad(Equipment):
    def __init__(self, address, comm_type='gpib', timeout=10000):
        super().__init__(address, comm_type, timeout)
        self.channel = [None] + [self.Channel(self, i) for i in range(1, 9)]

    def turn_on_all(self):
        for i in range(1, 9):
            self.channel[i].turn_on()

    def turn_off_all(self):
        for i in range(1, 9):
            self.channel[i].turn_off()

    

    def cleanup(self):
        self.turn_off_all()
        self.close()

    class Channel:
        def __init__(self, load, channel):
            self.load = load
            self.channel = channel
            self._cv = 0
            self._cc = 0
            self._cr = 0
            self._led_voltage = 0
            self._led_current = 0
            self._von = 0
            self._voltage = 0
            self._current = 0

        def dynamic(self, low, high, ton, toff, rise, fall): 
            self.load.write(f'CHAN {self.channel}')     
            self.load.write(f'CURR:DYN:L1 {low}')
            self.load.write(f'CURR:DYN:L2 {high}')
            self.load.write(f'CURR:DYN:RISE {rise}')
            self.load.write(f'CURR:DYN:FALL {fall}')
            self.load.write(f'CURR:DYN:T1 {ton}')
            self.load.write(f'CURR:DYN:T2 {toff}')

        @property
        def voltage(self):
            self.load.write(f'CHAN {self.channel}')
            self._voltage = float(self.load.write('FETC:VOLT?'))
            return self._voltage

        @property
        def current(self):
            self.load.write(f'CHAN {self.channel}')
            self._current = float(self.load.write('FETC:CURR?'))
            return self._current        

        @property
        def cv(self):
            return self._cv

        @property
        def cc(self):
            return self._cc

        @property
        def cr(self):
            return self._cr

        @property
        def led_voltage(self):
            return self._led_voltage
        
        @property
        def led_current(self):
            return self._led_current

        @property
        def von(self):
            return self._von


        @von.setter
        def von(self, voltage):
            self._von = voltage
            self.load.write(f'CHAN {self.channel}')
            self.load.write(f'CONF:VOLT:ON {self._von}')

        @cv.setter
        def cv(self, voltage):
            self._cv = voltage
            self.load.write(f'CHAN {self.channel}')
            self.load.write(f'VOLTAGE:L1 {self._cv}')
            self.load.write('MODE CV')

        @cc.setter
        def cc(self, current):
            self._cc = current
            self.load.write(f'CHAN {self.channel}')
            self.load.write(f'CURRENT:STATIC:L1 {self._cc}')
            self.load.write('MODE CCH')
            
        @cr.setter
        def cr(self, resistance):
            self._cr = resistance
            self.load.write(f'CHAN {self.channel}')
            self.load.write(f'RESISTANCE:L1 {self._cr}')
            self.load.write(f'RESISTANCE:L2 {self._cr}')
            self.load.write('MODE CRH')

        @led_voltage.setter
        def led_voltage(self, voltage):
            self._led_voltage = voltage
            # not supported yet...
            self.load.write(f'CHAN {self.channel}')
            self.load.write(f'LED:VO {self._led_voltage}')
            self.load.write('MODE LEDH')

        @led_current.setter
        def led_current(self, current):
            self._led_current = current
            # not supported yet...
            self.load.write(f'CHAN {self.channel}')
            self.load.write(f'LED:IO {self._led_current}')
            self.load.write('MODE LEDH')

        def turn_on(self):
            self.load.write(f'CHAN {self.channel}')
            self.load.write('LOAD ON')

        def turn_off(self):
            self.load.write(f'CHAN {self.channel}')
            self.load.write('LOAD OFF')

        def short_on(self):
            self.load.write(f'CHAN {self.channel}')
            self.load.write('LOAD:SHOR ON')

        def short_off(self):
            self.load.write(f'CHAN {self.channel}')
            self.load.write('LOAD:SHOR OFF')
