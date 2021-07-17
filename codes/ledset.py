from AUTOGUI_CONFIG import *
from time import sleep
ate_gui = AutoguiCalibrate()
# ate_gui.alt_tab()
# ate_gui.change_rheostat(3)

"""COMMS ADDRESS"""
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.10.170"

"""IMPORT DEPENDENCIES"""
import sys
import pyautogui
from time import sleep, time
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list
from powi.equipment import *
from time import sleep, time
import os
waveform_counter = 0

"""INITIALIZE EQUIPMENT"""


print("Intialize equipment.")
ac = ACSource(ac_source_address)
eload = ElectronicLoad(eload_address)
# scope = Oscilloscope(scope_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)


"""USER INPUT"""
LED = convert_argv_to_int_list(sys.argv[1]) # 46, 36, 24V
vin_list = convert_argv_to_int_list(sys.argv[2]) # [120, 230, 277] Vac
rset_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
# rset_list = [4]


from powi.equipment import *

board = pyfirmata.Arduino('COM8')
iterator = util.Iterator(board)
iterator.start()

RELAY1 = board.get_pin('d:10:o')
RELAY2 = board.get_pin('d:9:o')
RELAY3 = board.get_pin('d:8:o')



def led_46V():
    # print("46V LED")
    RELAY1.write(1)
    RELAY2.write(0)
    RELAY3.write(0)

def led_36V():
    # print("36V LED")
    RELAY1.write(0)
    RELAY2.write(1)
    RELAY3.write(0)

def led_24V():
    # print("24V LED")
    RELAY1.write(0)
    RELAY2.write(0)
    RELAY3.write(1)

def NL():
    # print("NL")
    RELAY1.write(0)
    RELAY2.write(0)
    RELAY3.write(0)


def discharge_output():
    for i in range(3):
        ac.turn_off()
        eload.channel[1].cc = 1
        eload.channel[1].turn_on()
        eload.channel[2].cc = 1
        eload.channel[2].turn_on()
        sleep(1)
        eload.channel[1].turn_off()
        eload.channel[2].turn_off()


def test_line_regulation(soak_time):
    headers("Line Regulation")
    for rset in rset_list:
        
        input(f"RSET: {rset}kOhms")
        # ate_gui.change_rheostat(rset)

        for load in LED:

            print(f"Change LED load to {load}V.")
            if load == 46: led_46V()
            elif load == 36: led_36V()
            elif load == 24: led_24V()
            elif load == 0: NL()
            else: print("Invalid LED.")    
            

            for vin in vin_list:
                vrms = vin

                print(f"{load}V, {vrms}Vac, RSET Dimming")

                if vin == 230: freq = 50
                else: freq = 60

                sleep(2)

                ac.voltage = vin
                ac.frequency = freq
                ac.turn_on()

                soak(soak_time)

                # create output list
                vac = str(vin)
                freq = str(freq)
                vin = f"{pms.voltage:.2f}"
                iin = f"{pms.current*1000:.2f}"
                pin = f"{pms.power:.3f}"
                pf = f"{pms.pf:.4f}"
                thd = f"{pms.thd:.2f}"
                vo1 = f"{pml.voltage:.3f}"
                io1 = f"{pml.current*1000:.2f}"
                po1 = f"{pml.power:.3f}"
                vreg1 = f"{100*(float(vo1)-12)/12:.4f}"
                eff = f"{100*(float(po1))/float(pin):.4f}"

                output_list = [vac, freq, vin, iin, pin, pf, thd, vo1, io1, po1, vreg1, eff, str(rset)]
                print(','.join(output_list))

                with open(f'{load}V, {vrms}Vac, RSET Dimming.txt', 'a+') as f:
                    f.write(','.join(output_list))
                    f.write('\n')

                discharge_output()



# User inputs start here
# ate_gui.alt_tab()
test_line_regulation(soak_time=10)