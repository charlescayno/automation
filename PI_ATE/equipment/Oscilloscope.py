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

class Oscilloscope(Equipment):
    def __init__(self, address, comm_type='lan', timeout=1E6):
        super().__init__(address, comm_type, timeout)

        self.write('SYST:DISP:UPD 1')


    def _extract_png(self, raw):
        offset = int(raw[1])-ord('0')
        return raw[offset+2:]

    def get_screenshot(self, filename="default.png", path=os.path.dirname(os.path.realpath(__file__))):
        self.write("HCOP:DEST \'MMEM\'")
        self.write("HCOP:DEV:LANG PNG")
        self.write("HCOP:DEV:INV ON")
        self.write("MMEM:NAME \'C:\\HCOPY.png\'")
        self.write("HCOP:IMMediate; *OPC?")

        self.device.write("MMEM:DATA? \'C:\\HCOPY.png\'")
        raw_image = self.device.read_raw()
        image = self._extract_png(raw_image)

        with open(path + "\\" + filename, "wb") as f:
            f.write(image)
            
    def _extract_channel_data(self, channel, raw):
        scale = self.channel[channel].scale
        position = self.channel[channel].position
        offset = self.channel[channel].offset
        factor = scale * 10 / (253 * 256)
        border = self.device.read("FORM:BORD?").strip()

        num_digits = raw[1] - 48
        num_values = int(raw[2 : 2 + num_digits])
        data = raw[2 + num_digits : 2 + num_digits + num_values]
        if border == "LSBF":
            adc = np.array(
                [
                    int.from_bytes(data[i : i + 2], "little")
                    for i in range(0, len(data), 2)
                ],
                dtype=np.int16,
            )
        else:
            adc = np.array(
                [
                    int.from_bytes(data[i : i + 2], "big")
                    for i in range(0, len(data), 2)
                ],
                dtype=np.int16,
            )
        channel_data = adc * factor - scale * position + offset
        return channel_data

    
    def save_channel_data(self, channel=1):
        self.write("EXPort:WAVeform:MULTIchannel ON")
        self.write("EXP:WAV:INCX OFF")
        for i in range(1, 5):
            if i == channel:
                self.write(f"CHANnel{i}:EXPortstate ON")
            else:
                self.write(f"CHANnel{i}:EXPortstate OFF")
        self.write("FORM:DATA INT,16")
        self.write("FORM ASC")
        a=self.write(f"CHAN{channel}:WAV1:DATA?")
        return a
        # input("tama naalskjdflakjsdfljkasdf")
        # raw_data = self.device.read()
        # print(raw_data)
        # return self._extract_channel_data(channel, raw_data)

    def probe_state(self, channel=1):
        return self.write(f'PROBe{channel}:SETup:STATe?')

    def probe_type(self, channel=1):   
        return self.write(f'PROBe{channel}:SETup:TYPE?')

    def probe_name(self, channel=1):
        return self.write(f'PROBe{channel}:SETup:NAME?')

    def probe_bandwidth(self, channel=1):
        return self.write(f'PROBe{channel}:SETup:BANDwidth?')

    def probe_attenuation(self, channel=1):
        return self.write(f'PROBe{channel}:SETup:ATTenuation[:AUTO]?')


    def auto_zero(self, channel):
        self.write(f"PROBe{channel}:SETup:OFFSet:AZERo")


    def get_measure(self, channel=1):
        channel_state = self.write(f'MEAS{channel}:ENAB?')
        if channel_state == '0':
            return None, None
        labels = []
        values = []
        self.write(f'MEAS{channel}:ARN ON')
        for item in self.write(f'MEAS{channel}:ARES?').split(','):
            label, value = item.split(':')
            labels.append(label.strip())
            values.append(float(value.strip()))        

        return labels, values

    def get_measure_all(self):
        result = []
        for i in range(1, 9):
            labels, values = self.get_measure(i)
            result.append({
                "channel": i,
                "labels": labels,
                "values": values
            })
        return result

    def get_vertical(self, channel=1):
        channel_state = self.write(f'CHAN{channel}:STAT?')
        if channel_state == '0':
            return None

        result = {
            "channel": str(channel),
            "scale": float(self.write(f'CHAN{channel}:SCAL?')),
            "position": float(self.write(f'CHAN{channel}:POS?')),
            "offset": float(self.write(f'CHAN{channel}:OFFS?')),
            "coupling": self.write(f'CHAN{channel}:COUP?'),
            "bandwidth": self.write(f'CHAN{channel}:BAND?')
        }
        return result

    def get_horizontal(self):
        result = {
            "scale": float(self.write('TIM:SCAL?')),
            "position": float(self.write('TIM:HOR:POS?')),
            "resolution": float(self.write('ACQ:RES?')),
            "sample rate": float(self.write('ACQ:SRAT?'))
        }
        return result

    def get_cursor(self, cursor=1):
        cursor_state = self.write(f'CURS{cursor}:STAT?')
        if cursor_state == '0':
            return None

        result = {
            "x1 position": self.write(f'CURS{cursor}:X1P?'),
            "x2 position": self.write(f'CURS{cursor}:X2P?'),
            "y1 position": self.write(f'CURS{cursor}:Y1P?'),
            "y2 position": self.write(f'CURS{cursor}:Y2P?'),
            "delta x": self.write(f'CURS{cursor}:XDEL?'),
            "delta y": self.write(f'CURS{cursor}:YDEL?'),
            "source": self.write(f'CURS{cursor}:SOUR?')
        }
        return result

    def run(self):
        self.write('RUN')
        self.write('DISP:TRIG:LIN OFF')

    def run_single(self):
        self.trigger_mode(mode='NORM')
        # self.trigger_mode(mode='AUTO')
        self.write('RUNS')
        self.write('DISP:TRIG:LIN OFF')

    def stop(self):
        self.write('STOP')
        self.write('DISP:TRIG:LIN OFF')

    # CMC Code Update #################

    def record_length(self, record_length):
        """
            record_length : 1000 to 1 000 000 000
        """
        self.write(f'ACQ:POIN {record_length}')
        # print('Record Length: '+ str(record_length) + ' Sa') 

    def resolution(self, resolution):
        self.write(f'ACQ:RES {resolution}')
        #print('Resolution: '+ str(resolution) + ' s') # 1E-15 to 0.5

    def time_position(self, time_position):
        self.write(f'TIM:REF {time_position}')
        self.write('TIM:HOR:POS 0')
    
    def time_scale(self, time_scale):
        """
        Parameters:
        <TimeScale> Range: 25E-12 to 50
                    Increment: 1E-12
                    *RST: 10E-9
                    Default unit: s/div
        """
        self.write(f'TIM:SCAL {time_scale}')

    def position_scale(self, time_position, time_scale):
        self.time_position(time_position)
        self.time_scale(time_scale)

    def remove_zoom(self):
        self.write("LAYout:ZOOM:REM 'Diagram1', 'Zoom1'")
        self.write("LAYout:ZOOM:REM 'Diagram1', 'Zoom2'")
        # self.remove_zoom_gate()

    def remove_zoom_gate(self):
        self.write(f"MEASurement1:GATE:ZCOupling OFF")

    def add_zoom_gate(self):
        self.write("MEASurement1:GATE ON")
        self.write(f"MEASurement1:GATE:ZCOupling ON")


    def add_zoom(self, rel_pos=50, rel_scale=10,vert_scale=100):
        self.remove_zoom()
        for i in range(5):
            self.write(f"LAYout:ZOOM:ADD 'Diagram{i}', VERT, OFF, -100e-6, 100e-6, 0, 5, 'Zoom1'")
            time_span = float(self.get_horizontal()['scale'])*10
            # print(f"Zoom scale: {((rel_scale/100)*time_span)/10} s/div.")
            self.write(f"LAYout:ZOOM:HORZ:REL:SPAN 'Diagram{i}', 'Zoom1', {rel_scale}")
            self.write(f"LAYout:ZOOM:HORZ:REL:POS 'Diagram{i}', 'Zoom1', {rel_pos}")
            self.write(f"LAYout:ZOOM:VERT:REL:SPAN 'Diagram{i}', 'Zoom1', {vert_scale}")
            # self.write("MEASurement1:GATE ON")
            # self.write(f"MEASurement1:GATE:ZCOupling ON")
    
    def add_zoom_with_gate(self, rel_pos=50, rel_scale=10):
        self.remove_zoom()
        self.write("LAYout:ZOOM:ADD 'Diagram1', VERT, OFF, -100e-6, 100e-6, -0.1, 0.05, 'Zoom1'")
        time_span = float(self.get_horizontal()['scale'])*10
        # print(f"Zoom scale: {((rel_scale/100)*time_span)/10} s/div.")
        self.write(f"LAYout:ZOOM:HORZ:REL:SPAN 'Diagram1', 'Zoom1', {rel_scale}")
        self.write(f"LAYout:ZOOM:HORZ:REL:POS 'Diagram1', 'Zoom1', {rel_pos}")
        self.write("LAYout:ZOOM:VERT:REL:SPAN 'Diagram1', 'Zoom1', 100")
        self.add_zoom_gate()
        
    
    def add_zoom_1(self, rel_pos=50, zoom_scale=6):
        # self.remove_zoom()
        self.write("LAYout:ZOOM:ADD 'Diagram1', VERT, OFF, -100e-6, 100e-6, -0.1, 0.05, 'Zoom1'")
        time_span = float(self.get_horizontal()['scale'])*10
        #print(f"Zoom scale: {zoom_scale} s/div.")
        rel_scale = (zoom_scale/time_span)*100*10
        #print(f"Rel Scale: {rel_scale}")
        self.write(f"LAYout:ZOOM:HORZ:REL:SPAN 'Diagram1', 'Zoom1', {rel_scale}")
        self.write(f"LAYout:ZOOM:HORZ:REL:POS 'Diagram1', 'Zoom1', {rel_pos}")
        self.write("LAYout:ZOOM:VERT:REL:SPAN 'Diagram1', 'Zoom1', 100")
        # self.write("MEASurement1:GATE ON")
        # self.write(f"MEASurement1:GATE:ZCOupling ON")
    
    def add_zoom_2(self, rel_pos=50, zoom_scale=6):
        # self.remove_zoom()
        self.write("LAYout:ZOOM:ADD 'Diagram1', VERT, OFF, -100e-6, 100e-6, -0.1, 0.05, 'Zoom2'")
        time_span = float(self.get_horizontal()['scale'])*10
        #print(f"Zoom scale: {zoom_scale} s/div.")
        rel_scale = (zoom_scale/time_span)*100*10
        #print(f"Rel Scale: {rel_scale}")
        self.write(f"LAYout:ZOOM:HORZ:REL:SPAN 'Diagram1', 'Zoom2', {rel_scale}")
        self.write(f"LAYout:ZOOM:HORZ:REL:POS 'Diagram1', 'Zoom2', {rel_pos}")
        self.write("LAYout:ZOOM:VERT:REL:SPAN 'Diagram1', 'Zoom2', 100")
        # self.write("MEASurement1:GATE ON")
        # self.write(f"MEASurement1:GATE:ZCOupling ON")

    def edge_trigger(self, trigger_channel, trigger_level, trigger_edge):
        channel = 'CHAN' + str(trigger_channel) # 1 | 2 | 3 | 4

        self.trigger_mode(mode='NORM')
        
        # setting trigger to absolute without hysteresis
        self.write(f"TRIGger:LEVel{trigger_channel}:NOISe MANual")
        self.write(f'TRIGger:LEVel{trigger_channel}:NOISe:ABSolute 0')

        self.write(f'TRIG1:SOUR {channel}')
        self.write('TRIG1:TYPE EDGE')
        self.write(f'TRIG1:LEV{trigger_channel} {trigger_level}') # range: -10 to 10, increment: 1E-3
        self.write(f'TRIG1:EDGE:SLOP {trigger_edge}') # POS | NEG | EITH
    
    def width_trigger(self, trigger_channel, width_polarity='POS', width_range='LONG', width=100E-3, delta=0):
        channel = 'CHAN' + str(trigger_channel) # 1 | 2 | 3 | 4
        self.write(f'TRIG1:SOUR {channel}')
        self.write('TRIG1:TYPE WIDT')
        self.write(f'TRIG1:WIDT:POL {width_polarity}') # POS | NEG
        self.write(f'TRIG1:WIDT:RANG {width_range}') # WITHin | OUTSide | SHORter | LONGer
        self.write(f'TRIG1:WIDT:WIDT {width}')  ## Range: 100E-12 to 10000
                                                # Increment: 100E-9
                                                # *RST: 5E-9
                                                # Default unit: s
        self.write(f'TRIG1:WIDT:DELT {delta}')  ## Range: 0 to 432
                                                # Increment: 500E-12
                                                # *RST: 0
                                                # Default unit: s

    def timeout_trigger(self, trigger_channel, timeout_range='HIGH', timeout_time=1E-3):
        channel = 'CHAN' + str(trigger_channel) # 1 | 2 | 3 | 4
        self.write(f'TRIG1:SOUR {channel}')
        self.write(f'TRIG1:TYPE TIM')
        self.write(f'TRIG1:TIM:RANG {timeout_range}') # HIGH | LOW | EITHer
        self.write(f'TRIG1:TIM:TIME {timeout_time}') # Range: 100E-12 to 10000
                                                        # Increment: 100E-9
                                                        # *RST: 100E-9
                                                        # Default unit: s

    def trigger_level(self, trigger_channel, trigger_level):
        self.write(f'TRIG1:LEV{trigger_channel} {trigger_level}') # range: -10 to 10, increment: 1E-3

    def trigger_mode(self, mode):
        self.write(f'TRIG:MODE {mode}') # AUTO | NORMal | FREerun

    def force_trigger(self):
        self.write('TRIG:FORC')

    def trigger_status(self):
        status = self.write('ACQ:CURR?')
        status = int(status)
        return status
    def trigger_noise_status(self,trigger_channel,state):
        self.write(f'TRIG1:LEV{trigger_channel}:NOISe {state}')


    ### Channel Settings ###

    def channel_BW(self, channel, channel_BW):
        """
        500: 'FULL'
        20: 'B20'
        200: 'B200'
        """
        channel_state = self.write(f'CHAN{channel}:STAT?')
        if channel_state == '0':
            return None

        if channel_BW == 500:
            channel_BW = 'FULL'
        elif channel_BW == 20:
            channel_BW = 'B20'
        elif channel_BW == 200:
            channel_BW = 'B200'

        self.write(f'CHAN{channel}:BAND {channel_BW}')

    def channel_offset(self, channel, channel_offset):
        channel_state = self.write(f'CHAN{channel}:STAT?')
        if channel_state == '0':
            return None

        self.write(f'CHAN{channel}:OFFS {channel_offset}')

    def channel_position(self, channel, channel_position):
        self.channel_offset(channel, 0)

        channel_state = self.write(f'CHAN{channel}:STAT?')
        if channel_state == '0':
            return None

        self.write(f'CHAN{channel}:POS {channel_position}')

    def channel_coupling(self, channel, channel_coupling):
        channel_state = self.write(f'CHAN{channel}:STAT?')
        if channel_state == '0':
            return None

        self.write(f'CHAN{channel}:COUP {channel_coupling}') # DC | DCLimit | AC

    def channel_scale(self, channel, channel_scale):
        channel_state = self.write(f'CHAN{channel}:STAT?')
        if channel_state == '0':
            return None

        self.write(f'CHAN{channel}:SCAL {channel_scale}') # V/div

    def channel_state(self, channel, state='OFF'):
        self.write(f"CHANnel{channel}:STATe {state}")
        self.write(f"MEASurement{channel}:ENABle {state}")


    def channel_settings(self, state, channel=1, scale=1, position=0, label='IOUT', color='LIGHT_BLUE', rel_x_position=50, rel_y_position=50, bandwidth=500, coupling='DCLimit', offset=0):
        """
        COLOR OPTIONS:

        - LIGHT_BLUE
        - YELLOW
        - PINK
        - GREEN
        - BLUE
        - ORANGE


        returns : state of the channel ('ON' or 'OFF')
        """

        self.channel_state(channel, state)

        self.channel_position(channel, position)
        self.channel_scale(channel, scale)
        
        #if state == 'ON': print(f"CH{channel} - {label}")
        self.channel_label(channel, label, rel_x_position,rel_y_position)
        self.channel_color(channel, color)

        self.channel_BW(channel, bandwidth)
        
        self.channel_coupling(channel, coupling)
        self.channel_offset(channel, offset)
        
        self.display_intensity()

        self.measure_enable(channel, state)

        return state

    def channel_label(self, channel, label, rel_x_position,rel_y_position):
        self.write(f"DISPlay:SIGNal:LABel:REMove 'Label1', C{channel}W1")
        sleep(1)
        self.write(f"DISPlay:SIGNal:LABel:ADD 'Label1', C{channel}W1, '{label}', REL, {rel_x_position}, {rel_y_position}")
    
    def channel_color(self, channel, color):

        light_blue = int('ff26e9ff', 16)
        yellow = int('ffffff00', 16)
        pink = int('ffff49fb', 16)
        green = int('ff16e500', 16)
        blue = int('ff0080ff', 16)
        orange = int('ffff6000', 16)

        colors = {  'LIGHT_BLUE':light_blue,
                    'YELLOW': yellow,
                    'PINK': pink,
                    'GREEN': green,
                    'BLUE': blue,
                    'ORANGE': orange
        }

        signal = {
            '1': 2,
            '2': 5,
            '3': 8,
            '4': 11
        }

        self.write(f"DISPlay:COLor:SIGNal{signal[str(channel)]}:COLor {colors[color]}")
    
    def display_intensity(self, intensity=100):
        self.write(f"DISPlay:INTensity 0")
        self.write(f"DISPlay:INTensity {intensity}")

    def cursor(self, channel=1, cursor_set=1, X1=1, X2=1, Y1=0, Y2=0, type='VERT'):
        self.write(f"CURSor{cursor_set}:FUNCtion {type}") # HORizontal | VERTical | PAIRed
        self.write(f"CURS{cursor_set}:STAT ON")
        self.write(f"CURS{cursor_set}:SOUR C{channel}W1")
        self.write(f"CURS{cursor_set}:X1P {X1}")
        self.write(f"CURS{cursor_set}:X2P {X2}")
        self.write(f"CURS{cursor_set}:Y1P {Y1}")
        self.write(f"CURS{cursor_set}:Y2P {Y2}")

    """MEASURE"""

    def measure_enable(self, channel, state='ON'):
        self.write(f"MEASurement{channel}:ENABle {state}")

    def measure_source(self, channel):
        self.write(f"MEASurement{channel}:SOURce C{channel}W1")
        self.write(f"MEASurement{channel}:CATegory AMPTime")
    
    def measure_off(self, channel):
        self.write(f"MEASurement{channel}:AOFF")

    def measure(self, channel, measure_list):
        """
        HIGH | LOW | AMPLitude | MAXimum | MINimum | PDELta |
        MEAN | RMS | STDDev | POVershoot | NOVershoot | AREA |
        RTIMe | FTIMe | PPULse | NPULse | PERiod | FREQuency |
        PDCYcle | NDCYcle | CYCarea | CYCMean | CYCRms |
        CYCStddev | PULCnt | DELay | PHASe | BWIDth | PSWitching |
        NSWitching | PULSetrain | EDGecount | SHT | SHR | DTOTrigger |
        PROBemeter | SLERising | SLEFalling
        """

        # self.measure_enable(channel, state='ON')
        self.measure_source(channel)
        self.measure_off(channel)
        measure_list = measure_list.strip(" ").split(",")
        for type in measure_list:
            self.write(f"MEASurement{channel}:ADDitional {type}, ON")

    def cleanup(self):
        self.close()
