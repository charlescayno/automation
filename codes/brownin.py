test = "Brown-In"

# comms
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.10.165"

start_voltage = 120
end_voltage = 130
slew_rate = 1
frequency = 60
time_fixvoltage = 0

from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from powi.equipment import headers, create_folder, footers, waveform_counter
from time import sleep, time
import os
import math

# # initialize equipment
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)

def reset():
    ac.turn_off()
    eload.channel[1].cc = 1
    eload.channel[1].turn_on()
    eload.channel[2].cc = 1
    eload.channel[2].turn_on()
    sleep(1)

def brownin(start=start_voltage, end=end_voltage, slew=slew_rate, frequency=frequency):
    print(f"brownin: {start_voltage} -> {end_voltage} Vac")
    for voltage in range(start, end+1, slew):
        ac.voltage = voltage
        ac.frequency = frequency
        ac.turn_on()
        # print(voltage)
        sleep(1)
    
def brownout(start=start_voltage, end=end_voltage, slew=slew_rate, frequency=frequency):
    print(f"brownout: {end_voltage} -> {start_voltage} Vac")
    for voltage in range(end, start-1, -slew):
        ac.voltage = voltage
        ac.frequency = frequency
        ac.turn_on()
        # print(voltage)
        sleep(1)

def fixvoltage(end=end_voltage, time=time_fixvoltage):
    print(f"fixvoltage: {end_voltage} Vac")
    ac.voltage = end
    ac.frequency = frequency
    ac.turn_on()
    sleep(time)

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

def soak(soak_time=30):
    for seconds in range(soak_time, 0, -1):
        sleep(1)
        print(f"{seconds:5d}s", end="\r")
    print("       ", end="\r")

## main code ##
headers(test)

# setup time scale for the oscilloscope
test_time = 2*(end_voltage-start_voltage)*slew_rate+time_fixvoltage
scope_time = roundup(test_time)
delay = scope_time-test_time
time_scale = scope_time/10
scope.time_scale(time_scale)
scope.run()
soak(int(delay/2))

# start of test
brownin()
fixvoltage()
brownout()

reset()


soak(int(delay/2))
scope.stop()

footers(waveform_counter)
