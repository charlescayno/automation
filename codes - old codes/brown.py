

# untested code




































# @cfcayno
# date created: 12/03/2020
# last modified: 12/03/2020
# FEATURES:
#   - semi-automatic: meaning cursor from the oscilloscope needs to be change
#                     every iteration
#   - auto-capture and auto-naming of filenames
# TODO:
#   - User must load the dfl preset on the oscilloscope since
#     this code doesn't include remote oscilloscope modification

from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from time import sleep, time

# USER INPUT STARTS HERE
################################################################################
ac_source_address = 5
source_power_meter_address = 1
load_power_meter_address = 2
eload_address = 8
eload_channel = 1
scope_address = '10.125.10.152' #charles

# INITIALIZE
waveform_counter = 0

# TRIGGER SETTINGS
trigger_level = 30          # set initial trigger level
trigger_source = 3            # trigger source CHANNEL

# BROWN IN SETTINGS
slew_rate = 0.1

# OUTPUT
Imax = 1.5
Vo = 30
Rload = int(Vo/Imax)

# IC SELECTION

# IC = ''
# IC = ''

waveforms_folder = 'waveforms/Brown-in and Brown-out'
print()
print('Brown-in and Brown-out Test:')

################################################################################
# USER INPUT ENDS HERE

start = time()

# Equipment Address
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)

# Trigger Settings
scope.edge_trigger(trigger_source=trigger_source, trigger_level=trigger_level, trigger_slope='POS')
scope.trigger_mode(mode='NORM')

# BROWN IN FULL LOAD CR
print('==================== BROWN IN 100LoadCR ===============================')
scope.run()

eload.channel[eload_channel].cr = Rload
eload.channel[eload_channel].turn_on()
ac.voltage = 0
ac.frequency = 60
ac.turn_on()

x = 0 # initial voltage

while x != 90:
	ac.voltage = x
	x += slew_rate # brown-in
	sleep(1)

# 0-90Vac w/ 0.1V/s slew rate takes 900s
sleep(100)

scope.stop()

print("Perform oscilloscope duties.")
input("Press ENTER to capture waveform...")

scope.get_screenshot(filename=f'{IC} 0-90Vac 100LoadCR.png', path=f'{waveforms_folder}')
print(f'{IC} 0-90Vac 100LoadCR.png')
waveform_counter += 1
sleep(2)

# BROWN OUT FULL LOAD CR
print('==================== BROWN OUT 100LoadCR ==============================')
scope.run()

eload.channel[eload_channel].cr = Rload
eload.channel[eload_channel].turn_on()
ac.voltage = 90
ac.frequency = 60
ac.turn_on()

x = 90 # initial voltage

while x != 0:
	ac.voltage = x
	x -= slew_rate # brown-out
	sleep(1)

# 90-0Vac w/ 0.1V/s slew rate takes 900s
sleep(100)

scope.stop()

print("Perform oscilloscope duties.")
input("Press ENTER to capture waveform...")

scope.get_screenshot(filename=f'{IC} 90-0Vac 100LoadCR.png', path=f'{waveforms_folder}')
print(f'{IC} 90-0Vac 100LoadCR.png')
waveform_counter += 1
sleep(2)

# BROWN IN NO LOAD
print('==================== BROWN IN 0Load ===================================')
scope.run()

eload.channel[eload_channel].cr = Rload
eload.channel[eload_channel].turn_off()
ac.voltage = 0
ac.frequency = 60
ac.turn_on()

x = 0 # initial voltage

while x != 90:
	ac.voltage = x
	x += slew_rate # brown-in
	sleep(1)

# 0-90Vac w/ 0.1V/s slew rate takes 900s
sleep(100)

scope.stop()

print("Perform oscilloscope duties.")
input("Press ENTER to capture waveform...")

scope.get_screenshot(filename=f'{IC} 0-90Vac 0Load.png', path=f'{waveforms_folder}')
print(f'{IC} 0-90Vac 0Load.png')
waveform_counter += 1
sleep(2)

# BROWN OUT NO LOAD
print('==================== BROWN OUT 0Load ==================================')
scope.run()

eload.channel[eload_channel].cr = Rload
eload.channel[eload_channel].turn_off()
ac.voltage = 90
ac.frequency = 60
ac.turn_on()

x = 90 # initial voltage

while x != 0:
	ac.voltage = x
	x -= slew_rate # brown-out
	sleep(1)

# 90-0Vac w/ 0.1V/s slew rate takes 900s
sleep(100)

scope.stop()

print("Perform oscilloscope duties.")
input("Press ENTER to capture waveform...")

scope.get_screenshot(filename=f'{IC} 90-0Vac 0Load.png', path=f'{waveforms_folder}')
print(f'{IC} 90-0Vac 0Load.png')
waveform_counter += 1
sleep(2)

print('=======================================================================')
print('=======================================================================')

print(f'{waveform_counter} waveforms captured.')
print('test complete.')
end = time()
print()
print(f'test time: {(end-start)/60} mins.')