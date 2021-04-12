# USER INPUT STARTS HERE
#########################################################################################
## TEST PARAMETERS

test = "sample"

# comms
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.10.112"

# scope settings
# vin_channel = 3
# vout_channel = 1
# iout_channel = 2
# position = -2


# trigger settings
trigger_level = 10   # V
trigger_source = 2
trigger_slope = 'POS'

# eload settings
eload_channel = 1

## INPUT
vin = [90, 115, 230, 265]
freq = [60, 60, 50, 50]

## OUTPUT
vout = 20
Iout_max = 3.25 # A
Iout = [Iout_max, 0.75*Iout_max, 0.50*Iout_max, 0.25*Iout_max]
Iout_name = [100, 75, 50, 25, 10, 0]
#########################################################################################
# USER INPUT ENDS HERE

# from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from powi.equipment import Oscilloscope
# from powi.equipment import headers, create_folder, footers, waveform_counter
from time import sleep, time
import os

# initialize equipment
# ac = ACSource(ac_source_address)
# pms = PowerMeter(source_power_meter_address)
# pml = PowerMeter(load_power_meter_address)
# eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)
start = time()

scope.run()


# scope.resolution(1E-16)
sleep(5)

scope.stop()

data = scope.get_chan_data(channel = 2)
print("length of data: "+ str(len(data)))
# print(data)



import matplotlib.pyplot as plt
x = range(0, len(data))
plt.figure()
plt.plot(x, data)  

plt.xlabel("data")
plt.ylabel("Vout")
plt.title("Output Voltage Ripple")

plt.show()







end = time()
total_time = end-start
print(f'test time: {total_time:.2f} secs. / {total_time/60:.2f} mins.')

