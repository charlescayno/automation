##################################################################################
"""IMPORT DEPENDENCIES"""
from time import sleep
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl, Keithley_DC_2230G
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt

from itertools import permutations
##################################################################################

class EQUIPMENT_ADDRESS():
    SCOPE = "10.125.10.101"
    AC_SOURCE = 5
    POWER_METER_SOURCE = 30
    POWER_METER_LOAD_1 = 2
    POWER_METER_LOAD_2 = 2
    POWER_METER_DIM = 21
    ELOAD = 8
    SIG_GEN = '11'
    ELOAD_CHANNEL = 1

ac = ACSource(EQUIPMENT_ADDRESS.AC_SOURCE)
pms = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_SOURCE)
pml = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_LOAD_1)
eload = ElectronicLoad(EQUIPMENT_ADDRESS.ELOAD)
# scope = Oscilloscope(EQUIPMENT_ADDRESS.SCOPE)
try: led_ctrl = LEDControl()
except: pass


class EQUIPMENT_FUNCTIONS():

    def __init__(self):
        pass

    def ELOAD_CR_ON(self, channel, cr_load):
        eload.channel[channel].cr = cr_load
        eload.channel[channel].turn_on()

    def ELOAD_CC_ON(self, channel, cc_load):
        eload.channel[channel].cc = cc_load
        eload.channel[channel].turn_on()
    
    def ELOAD_OFF(channel):
        eload.channel[channel].turn_off()
    
    def AC_TURN_ON(self, voltage, type='AC'):
        ac.voltage = voltage
        ac.turn_on()

    def AC_TURN_OFF(self):
        ac.turn_off()

    def DISCHARGE_OUTPUT(self, times):    
        ac.turn_off()
        for i in range(times):
            for i in range(1,9):
                eload.channel[i].cr = 10
                eload.channel[i].turn_on()
            sleep(0.5)
            for i in range(1,9):
                eload.channel[i].turn_off()
                eload.channel[i].short_off()
            sleep(1)

            for i in range(1,9):
                eload.channel[i].cc = 1
                eload.channel[i].short_on()
                eload.channel[i].turn_on()
            sleep(0.5)

            for i in range(1,9):
                eload.channel[i].turn_off()
                eload.channel[i].short_off()
            sleep(0.5)


    def _sigfig(self, number, sigfig):
        try: a = float(f"{number:.{sigfig}f}")
        except: a = "NaN"
        return 

    def _pm_measurements(self):

        vac = self._sigfig(pms.voltage, 6)
        iin = self._sigfig(pms.current*1000, 6)
        pin = self._sigfig(pms.power, 6)
        pf = self._sigfig(pms.pf, 6)
        thd = self._sigfig(pms.thd, 6)
        vo1 = self._sigfig(pml.voltage, 6)
        io1 = self._sigfig(pml.current, 6)
        po1 = self._sigfig(pml.power, 6)
        
        return vac, iin, pin, pf, thd, vo1, io1, po1

    def COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD(self, vin, vout, iout):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-vout)/vo1, 6)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-iout)/io1, 6)
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 6)
        except: eff = "NaN"

        output_list = [vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff]

        return output_list

    def COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD(self, vin, led, iout):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-led)/vo1, 6)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-iout)/io1, 6)
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 6)
        except: eff = "NaN"

        output_list = [led, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff]

        return output_list

    def SET_LED(led):
        led_ctrl.voltage(led)