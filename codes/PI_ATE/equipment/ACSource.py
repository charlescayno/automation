from powi.equipment import Equipment, reject_nan
from functools import wraps
from math import isnan
from time import sleep, time
from abc import ABC, abstractmethod
import atexit
import os
import sys
import shutil
# from pyfirmata import Arduino, util
# import pyfirmata
import pyvisa
import numpy as np
# from gtts import gTTS
# from playsound import playsound

class ACSource(Equipment):
    def __init__(self, address, comm_type='gpib', timeout=10000):
        super().__init__(address, comm_type, timeout)

        self._voltage = 0
        self._frequency = 0
        self._coupling = 'AC'

    def turn_on(self, phase=None):
        if self._coupling == 'AC':
            self.write(f'VOLT {self._voltage}')
            self.write('OUTP:COUP AC')
            self.write('VOLT:OFFS 0')

        elif self._coupling == 'DC':
            self.write('VOLT 0')
            self.write('OUTP:COUP DC')
            self.write(f'VOLT:OFFS {self._voltage}')
        
        self.write('OUTP ON')

    def turn_off(self):
        self.write('OUTP OFF')

    def set_freq(self, voltage):
        if voltage >= 180 and voltage <= 265: ac_freq = 50
        else: ac_freq = 60
        return ac_freq

    @property
    def voltage(self):
        return self._voltage

    @property
    def frequency(self):
        return self._frequency
    
    @property
    def coupling(self):
        return self._coupling

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        """automatic frequency setting"""
        self._frequency = self.set_freq(self._voltage)
        self.write(f'FREQ {self._frequency}')

    @frequency.setter
    def frequency(self, frequency):
        self._frequency = frequency # manual setting
        self.write(f'FREQ {self._frequency}')

    @coupling.setter
    def coupling(self, type):
        if type.upper() == 'DC':
            self._coupling = 'DC'
        else:
            self._coupling = 'AC'

    def ac_cycling(self, pulse_count, vin, start_soak, off_time, on_time, end_soak):
    
        freq = self.set_freq(vin)
        self.write(f"TRIG:TRAN:SOUR BUS")
        
        a = f"LIST:DWELL {start_soak}, "
        for i in range(pulse_count):
            a = a + f"{off_time}, {on_time}, "
        a = a + f"{off_time}, {end_soak}"
        # print(a)
        self.write(f"{a}")

        self.write(f"VOLT:MODE LIST")
        
        b = f"LIST:VOLT {vin}, "
        for i in range(pulse_count):
            b = b + f"0, {vin}, "
        b = b + f"0, {vin}"
        # print(b)
        self.write(b)

        self.write(f"VOLT:SLEW:MODE LIST")

        c = f"LIST:VOLT:SLEW 9.9e+037, "
        for i in range(pulse_count):
            c = c + f"9.9e+037, 9.9e+037, "
        c = c + f"9.9e+037, 9.9e+037"
        # print(c)
        self.write(c)

        self.write(f"FREQ:MODE LIST")
        d = f"LIST:FREQ {freq}, "
        for i in range(pulse_count):
            d = d + f"{freq}, {freq}, "
        d = d + f"{freq}, {freq}"
        # print(d)
        self.write(d)

        self.write(f"FREQ:SLEW:MODE LIST")

        e = f"LIST:FREQ:SLEW 9.9e+037, "
        for i in range(pulse_count):
            e = e + f"9.9e+037, 9.9e+037, "
        e = e + f"9.9e+037, 9.9e+037"
        # print(e)
        self.write(e)

        self.write(f"VOLT:OFFS:MODE FIX")
        self.write(f"VOLT:OFFS:SLEW:MODE FIX")
        self.write(f"PHAS:MODE LIST")

        f = f"LIST:PHAS 270, "
        for i in range(pulse_count):
            f = f + f"270, 270, "
        f = f + f"270, 270"
        # print(f)
        self.write(f)

        self.write(f"CURR:PEAK:MODE LIST")

        g = f"LIST:CURR 40.4, "
        for i in range(pulse_count):
            g = g + f"40.4, 40.4, "
        g = g + f"40.4, 40.4"
        # print(g)
        self.write(g)

        self.write(f"FUNC:MODE FIX")

        h = f"LIST:TTLT ON, "
        for i in range(pulse_count):
            h = h + f"OFF, OFF, "
        h = h + f"OFF, OFF"
        # print(h)
        self.write(h)

        self.write(f"LIST:STEP AUTO")
        self.write(f"OUTP:TTLT:STAT ON")
        self.write(f"OUTP:TTLT:SOUR LIST")
        self.write(f"TRIG:SYNC:SOUR PHASE")
        self.write(f"TRIG:SYNC:PHAS 0.0")
        self.write(f"TRIG:TRAN:DEL 0")
        self.write(f"Sens:Swe:Offs:Poin 0")
        self.write(f"TRIG:ACQ:SOUR TTLT")
        self.write(f"INIT:IMM:SEQ3")
        self.write(f"LIST:COUN 1")
        self.write(f"INIT:IMM:SEQ1")
        self.write(f"TRIG:TRAN:SOUR BUS")
        self.write(f"TRIG:IMM")

        delay = start_soak + end_soak + (pulse_count*(off_time + on_time)) + off_time
        sleep(delay)

    def cleanup(self):
        self.turn_off()
        self.close()
