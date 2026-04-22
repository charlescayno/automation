# COMMS
ac_source_address = 5
source_power_meter_address = 1
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.10.148"

"""IMPORT DEPENDENCIES"""
import sys
import pyautogui
from time import sleep, time
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list
import os
from powi.equipment import LEDControl
waveform_counter = 0
import winsound as ws
from filemanager import path_maker, remove_file, move_file


"""INITIALIZE EQUIPMENT"""
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
# scope = Oscilloscope(scope_address)
led = LEDControl()

def discharge_output():
    ac.turn_off()
    for i in range(1,9):
        eload.channel[i].cc = 1
        eload.channel[i].turn_on()
        eload.channel[i].short_on()
    sleep(2)
    for i in range(1,9):
        eload.channel[i].turn_off()
        eload.channel[i].short_off()
    sleep(1)

def sfx():
    ws.PlaySound("dingding.wav", ws.SND_ASYNC)
    sleep(2)

### USER INPUT #######################################
led_list = [46,36,24]
# led_list = convert_argv_to_int_list(sys.argv[1])

vin_list = [120,230,277]
# vin_list = convert_argv_to_int_list(sys.argv[2])

rset_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] 

# rset_list = [24]

IOUT_REG = 1660

test = f"LEDSET Dimming"
waveforms_folder = f'waveforms/{test}'


######################################################

def ledset_line_regulation(soak_time=10):

    for rset in rset_list:
        
        sfx()
        input(f"change RSET >> {rset}kOhms\n")
    
        for LED in led_list:

            led.voltage(LED)        

            for vin in vin_list:

                sleep(2)

                ac.voltage = vin
                freq = ac.set_freq(vin)
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
                ireg1 = f"{100*(float(io1)-IOUT_REG)/IOUT_REG:.4f}"
                eff = f"{100*(float(po1))/float(pin):.4f}"

                output_list = [str(rset), vac, freq, vin, iin, pin, pf, thd, vo1, io1, po1, ireg1, eff]
                print(','.join(output_list))

                file = f'{LED}V, {vac}Vac, RSET Dimming.txt'
                with open(file, 'a+') as f:
                    f.write(','.join(output_list))
                    f.write('\n')
                
                path = path_maker(f'{waveforms_folder}')
                source_path = f'{os.getcwd()}/{file}'
                destination_path = f'{path}/{file}'
                move_file(source_path, destination_path)

                discharge_output()

            
            print()
        
        discharge_output()

def main():
    ledset_line_regulation(soak_time=10)
    
if __name__ == "__main__":
    headers(test)
    discharge_output()
    main()
    discharge_output()
    footers(waveform_counter)