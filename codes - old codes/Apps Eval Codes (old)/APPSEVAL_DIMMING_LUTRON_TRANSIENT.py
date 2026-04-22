print("CMC | 20NOV2021")

"""IMPORT DEPENDENCIES"""
from time import time, sleep
import sys
import os
import math
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt, sfx
from filemanager import path_maker, remove_file, move_file
import winsound as ws
from playsound import playsound
waveform_counter = 0

##################################################################################

"""COMMS"""
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.10.115"
"""EQUIPMENT INITIALIZE"""
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)
led = LEDControl()

"""USER INPUT"""
led_list = [24]
vin_list = [230]
dim_list = [1.2,3,4,10.7]

test = "Lutron Dimming Transient"
waveforms_folder = f'C:/Users/ccayno/Desktop/DER-945/Test Data/{test}'

"""DO NOT EDIT BELOW THIS LINE"""


"""GENERIC FUNCTIONS"""
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


def message():
    print(">> Setup Lutron Dimmer")
    print(">> Set CH1 to Iout")
    print(">> Set CH2 to VR")
    print(">> Set CH3 to Vout")
    print(">> Set CH4 to DIM+")
    input("Press enter to continue.")




def scope_settings():


    scope.stop()
    scope.remove_zoom()
    scope.position_scale(time_position = 10, time_scale = 2)
    scope.edge_trigger(4, 2.1, 'POS')

    scope.channel_settings(state='ON', channel=1, scale=0.250, position=-3, label="Iout", color='GREEN', rel_x_position=20, bandwidth=20, coupling='DCLimit', offset=0)
    scope.channel_settings(state='ON', channel=2, scale=10, position=-2, label="VR", color='BLUE', rel_x_position=40, bandwidth=20, coupling='DCLimit', offset=0)
    scope.channel_settings(state='ON', channel=3, scale=10, position=-2, label="Vout", color='PINK', rel_x_position=60, bandwidth=20, coupling='DCLimit', offset=0)
    scope.channel_settings(state='ON', channel=4, scale=3, position=-4, label="DIM+", color='YELLOW', rel_x_position=80, bandwidth=20, coupling='DCLimit', offset=0)



def main():

    global waveform_counter
    scope_settings()


    for LED in led_list:

        led.voltage(LED)
        discharge_output()

        for vin in vin_list:
            print(f"\n{LED}V, {vin}Vac\n")

            dim_list.sort()

            for i in range(len(dim_list)):
                for dim in dim_list:
                    if dim_list[i] < dim:

                        scope.position_scale(time_position = 10, time_scale = 2)

                        start = dim_list[i]
                        end = dim
                        if start==3 and end==4:
                            pass
                        else:
                            trig = (end+start)/2
                            scope.edge_trigger(4, trig, 'POS')
                            print(f"{start}-{end}V")

                            
                            ac.voltage = vin
                            ac.frequency = ac.set_freq(vin)
                            ac.turn_on()

                            sfx()
                            input(f"Set voltage to {start}V")


                            scope.run_single()
                            print(f"Set voltage to {end}V")
                            input("Capture waveform?")

                            filename = f'Lutron Transient - {LED}V, {vin}Vac, {start}-{end}V.png'
                            path = path_maker(f'{waveforms_folder}')
                            scope.get_screenshot(filename, path)
                            print(filename)
                            waveform_counter += 1
                            print()
            
            discharge_output()

            dim_list.sort(reverse=True)
            for i in range(len(dim_list)):
                for dim in dim_list:
                    if dim_list[i] > dim:

                        scope.position_scale(time_position = 20, time_scale = 2)

                        start = dim_list[i]
                        end = dim

                        if start==4 and end==3:
                            pass
                        else:

                            trig = (end+start)/2
                            scope.edge_trigger(4, trig, 'NEG')
                            print(f"{start}-{end}V")

                            
                            ac.voltage = vin
                            ac.frequency = ac.set_freq(vin)
                            ac.turn_on()

                            sfx()
                            input(f"Set voltage to {start}V")

                            scope.run_single()
                            print(f"Set voltage to {end}V")
                            input("Capture waveform?")
                            
                            filename = f'Lutron Transient - {LED}V, {vin}Vac, {start}-{end}V.png'
                            path = path_maker(f'{waveforms_folder}')
                            scope.get_screenshot(filename, path)
                            print(filename)
                            waveform_counter += 1
                            print()
            
            print()
            print()


#     for vin in vin_list:
#         for LED in led_list:
#             led.voltage(LED)
            
#             discharge_output()
#             print()
#             print(f"{LED}V, {vin}Vac")
#             print()

#             dim_list.sort()
#             for i in range(len(dim_list)):
#                 for dim in dim_list:
#                     if dim_list[i] < dim:

#                         start = dim_list[i]
#                         end = dim
#                         if start==3 and end==4:
#                             pass
#                         else:
#                             trig = (end+start)/2
#                             scope.edge_trigger(4, trig, 'POS')
#                             print(f"{start}-{end}V")

#                             input(f"Set voltage to {start}V")
#                             ac.voltage = vin
#                             ac.frequency = ac.set_freq(vin)
#                             ac.turn_on()
#                             scope.run_single()
#                             print(f"Set voltage to {end}V")
#                             input("Capture waveform?")

#                             filename = f'{LED}V, {vin}Vac, {start}-{end}V.png'
#                             path = waveforms_folder + f'/{LED}V'
#                             if not os.path.exists(path): os.mkdir(path)
#                             scope.get_screenshot(filename, path)
#                             print(filename)
#                             waveform_counter += 1
#                             print()

#             discharge_output()

#             dim_list.sort(reverse=True)
#             for i in range(len(dim_list)):
#                 for dim in dim_list:
#                     if dim_list[i] > dim:

#                         start = dim_list[i]
#                         end = dim

#                         if start==4 and end==3:
#                             pass
#                         else:

#                             trig = (end+start)/2
#                             scope.edge_trigger(4, trig, 'NEG')
#                             print(f"{start}-{end}V")

#                             input(f"Set voltage to {start}V")
#                             ac.voltage = vin
#                             ac.frequency = ac.set_freq(vin)
#                             ac.turn_on()
#                             scope.run_single()
#                             print(f"Set voltage to {end}V")
#                             input("Capture waveform?")
                            
#                             filename = f'{LED}V, {vin}Vac, {start}-{end}V.png'
#                             path = waveforms_folder + f'/{LED}V'
#                             if not os.path.exists(path): os.mkdir(path)
#                             scope.get_screenshot(filename, path)
#                             print(filename)
#                             waveform_counter += 1
#                             print()
            
#             print()
#             print()

# def slow_transient_main():

#     global waveform_counter
#     scope_settings()
#     scope.position_scale(time_position = 10, time_scale = 4)
#     dim_list = [1.2,5]

#     for LED in led_list:
#         led.voltage(LED)
#         for vin in vin_list:

            
#             discharge_output()
#             print()
#             print(f"{LED}V, {vin}Vac")
#             print()

#             dim_list.sort()
#             for i in range(len(dim_list)):
#                 for dim in dim_list:
#                     if dim_list[i] < dim:

#                         start = dim_list[i]
#                         end = dim
#                         if start==3 and end==4:
#                             pass
#                         else:
#                             trig = 2
#                             scope.edge_trigger(4, trig, 'POS')
#                             print(f"{start}-{end}V")

#                             input(f"Set voltage to {start}V")
#                             ac.voltage = vin
#                             ac.frequency = ac.set_freq(vin)
#                             ac.turn_on()
#                             scope.run_single()
#                             print(f"Set voltage to {end}V")
#                             input("Capture waveform?")

#                             filename = f'{LED}V, {vin}Vac, {start}-{end}V (slow transient).png'
#                             path = waveforms_folder + f'/{LED}V'
#                             if not os.path.exists(path): os.mkdir(path)
#                             scope.get_screenshot(filename, path)
#                             print(filename)
#                             waveform_counter += 1
#                             print()

#             discharge_output()

#             dim_list.sort(reverse=True)
#             # scope.position_scale(time_position = 90, time_scale = 4)
#             for i in range(len(dim_list)):
#                 for dim in dim_list:
#                     if dim_list[i] > dim:

#                         start = dim_list[i]
#                         end = dim

#                         if start==4 and end==3:
#                             pass
#                         else:

#                             trig = 4.5
#                             scope.edge_trigger(4, trig, 'NEG')
#                             print(f"{start}-{end}V")

#                             input(f"Set voltage to {start}V")
#                             ac.voltage = vin
#                             ac.frequency = ac.set_freq(vin)
#                             ac.turn_on()
#                             scope.run_single()
#                             print(f"Set voltage to {end}V")
#                             input("Capture waveform?")
                            
#                             filename = f'{LED}V, {vin}Vac, {start}-{end}V (slow transient).png'
#                             path = waveforms_folder + f'/{LED}V'
#                             if not os.path.exists(path): os.mkdir(path)
#                             scope.get_screenshot(filename, path)
#                             print(filename)
#                             waveform_counter += 1
#                             print()
            
#             print()
#             print()


if __name__ == "__main__":
    headers(test)
    discharge_output()
    main()
    discharge_output()
    footers(waveform_counter)