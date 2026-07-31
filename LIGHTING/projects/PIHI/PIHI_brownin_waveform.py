import sys, os
_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
from battery_discharge import main_battery_discharge
import numpy as np
########################################## USER INPUT ##########################################
# INPUT
vin = [90]

start_voltage = 0
end_voltage = 150
slew_rate = 1
frequency = 60
time_fixvoltage = 60 # s

# PROJECT DETAILS
project = "AF"
# excel_name = "DER-999"
test = f"Brown-out Brown-in asdasd"
excel_name = f"{project} {test}"
channel_list=[2,3,4] # select channels to capture data, 2-Vsense, 3-Icoil, 4-PWM

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def brown_in_brown_out():

    test_time = 2*((end_voltage-start_voltage)/slew_rate)
    scope_time = roundup(test_time)
    delay = scope_time-test_time
    time_scale = scope_time/10
    print(f"Estimated time: {scope_time/60} mins.")
    scope.time_scale(time_scale)
    scope.run()
    soak(int(delay/2))
    # start of test
    browning(start_voltage, end_voltage, slew_rate, frequency)
    browning(end_voltage, start_voltage, slew_rate, frequency)
    soak(int(delay/2))
    scope.stop()

    filename = f"{start_voltage}-{end_voltage}-{start_voltage} Vac, {slew_rate}V per s"
    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)

def fixvoltage(voltage, soak):
    ac.voltage = voltage
    ac.frequency = ac.set_freq(voltage)
    ac.turn_on()
    sleep(soak)

def brown_out_brown_in():

    test_time = 2*((end_voltage-start_voltage)/slew_rate)
    scope_time = roundup(test_time)
    delay = scope_time-test_time
    time_scale = scope_time/10
    print(f"Estimated time: {scope_time/60} mins.")
    scope.time_scale(time_scale)
    scope.run()
    t_fixvoltage = int(delay/2)
    # start of test
    fixvoltage(end_voltage, t_fixvoltage)
    browning(end_voltage, start_voltage, slew_rate, frequency)
    browning(start_voltage, end_voltage, slew_rate, frequency)
    fixvoltage(end_voltage, t_fixvoltage)
    scope.stop()

    filename = f"{end_voltage}-{start_voltage}-{end_voltage} Vac, {slew_rate}V per s"
    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)

def brown_in():

    # test_time = ((end_voltage-start_voltage)/slew_rate)+time_fixvoltage
    # scope_time = roundup(test_time)
    # delay = scope_time-test_time
    # time_scale = scope_time/10
    # print(f"Estimated time: {scope_time/60} mins.")
    # scope.time_scale(time_scale)
    # scope.run()
    # soak(int(delay))

    # start of test
    browning(start_voltage, end_voltage, slew_rate, frequency)
    fixvoltage(end_voltage,time_fixvoltage)
    scope.stop()

    filename = f"{start_voltage}-{end_voltage} Vac, {slew_rate}V per s.png"
    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)

def brown_out():

    test_time = ((end_voltage-start_voltage)/slew_rate)+time_fixvoltage
    scope_time = roundup(test_time)
    delay = scope_time-test_time
    time_scale = scope_time/10
    print(f"Estimated time: {scope_time/60} mins.")
    scope.time_scale(time_scale)
    scope.run()
    
    # start of test
    fixvoltage(end_voltage, time_fixvoltage)
    browning(end_voltage, start_voltage, slew_rate, frequency)
    soak(int(delay))
    scope.stop()

    filename = f"{end_voltage}-{start_voltage} Vac, {slew_rate}V per s.png"
    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)

def browning(start, end, slew, frequency):

    if start > end:
        print(f"brownout: {start} -> {end} Vac")
        for vin in np.arange(start, end+1, -slew):
            ac.voltage = vin
            ac.coupling = 'DC'
            ac.frequency = frequency
            ac.turn_on()
            sleep(1)
    if start < end:
        print(f"brownin: {start} -> {end} Vac")
        for vin in np.arange(start, end+1, slew):
            ac.voltage = vin
            ac.coupling = 'DC'
            ac.frequency = frequency
            ac.turn_on()
            sleep(1)

def main():
    # brown_in_brown_out()
    # brown_out_brown_in()
    brown_in()
    # brown_out()
    

    

if __name__ == "__main__":
 
    headers(test)
    main()
    footers(waveform_counter)
