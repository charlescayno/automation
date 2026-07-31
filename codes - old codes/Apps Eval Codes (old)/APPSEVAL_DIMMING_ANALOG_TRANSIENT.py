print("Charles Cayno | 08-Aug-2021")

test = "Analog Dimming Transient"
waveforms_folder = f'waveforms/{test}'

"""LIBRARIES"""
from powi.MULTIPROTOCOL_CONTROL import MultiprotocolControl
from time import time, sleep
import sys
import os
# from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list
waveform_counter = 0

"""COMMS"""
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.10.166"

"""EQUIPMENT INITIALIZE"""
# ac = ACSource(ac_source_address)
# pms = PowerMeter(source_power_meter_address)
# pml = PowerMeter(load_power_meter_address)
# eload = ElectronicLoad(eload_address)
# scope = Oscilloscope(scope_address)
control = MultiprotocolControl()

"""USER INPUT"""
led_list = convert_argv_to_int_list(sys.argv[1]) # 46, 36, 24
vin_list = convert_argv_to_int_list(sys.argv[2]) # 120, 230, 277
end_list = [10, 7, 5, 4, 3, 2, 1]
test_list = [1, 2] # 1 - Transient Up, 2 - Transient Down
dim_trigger_source = 3


"""GENERIC FUNCTIONS"""
def discharge_output():
    # ac.turn_off()
    # eload.channel[1].cc = 1
    # eload.channel[1].turn_on()
    # eload.channel[2].cc = 1
    # eload.channel[2].turn_on()
    # sleep(3)
    pass
    # eload.channel[1].turn_off()
    # eload.channel[2].turn_off()



"""SPECIAL FUNCTIONS FOR THIS TEST"""

def analog_dimming(start=0, end=10, voltage=120, LED=46,
                    condition="First Power Up Discharged Cout"):
    global waveform_counter

    # ac.voltage = voltage
    # ac.frequency = ac.set_freq(voltage)
    # ac.turn_on()

    control.manual_set_analog(start)
    
    # sleep(1)

    # scope.run()

    # sleep(1)
    
    control.manual_set_analog(end)
    
    # sleep(6)
    
    # scope.stop()
    
    # sleep(1)

    filename = f'{LED}V, {voltage}Vac, {start}-{end}V Analog, {condition}.png'
    path = waveforms_folder + f'/{LED}V, {voltage}Vac'
    if not os.path.exists(path): os.mkdir(path)    
    # scope.get_screenshot(filename, path)
    print(filename)
    waveform_counter += 1



def main():
    for LED in led_list:
        for vin in vin_list:
            for end in end_list:
                # scope.position_scale(10, 0.5)
                # control.manual_set_analog(0) # 0V initial dim

                # sleep(5)
                
                test = 1 # TRANSIENT UP
                for test in test_list:
                    dim_trigger_level = end - 0.5
                    # scope.edge_trigger(dim_trigger_source, dim_trigger_level, 'POS')
                    for start in range(0, end, 1):
                        # control.manual_set_analog(start)

                        analog_dimming(start, end, vin, LED, "First Power Up (Discharged Cout)")
                        analog_dimming(start, end, vin, LED, "No AC reset (Not Discharged Cout)")

                        discharge_output()

                test = 2 # TRANSIENT DOWN
                for test in test_list:
                    """TRANSIENT DOWN"""
                    # scope.edge_trigger(dim_trigger_source, dim_trigger_level, "NEG")
                    for start in range(0, end, 1):
                        analog_dimming(end, start, vin, LED, "Transient Down")


if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)



