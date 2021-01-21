from piph.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from time import sleep

acsource = ACSource(address=5)
powermeter_source = PowerMeter(address=1)
powermeter_load = PowerMeter(address=2)
eload = ElectronicLoad(address=8)
scope = Oscilloscope(address="169.254.159.200")

full_load = 1.25
voltage_list = [90, 115, 230, 265]
frequency_list = [60, 60, 50, 50]

for voltage, frequency in zip(voltage_list, frequency_list):
    acsource.voltage = voltage
    acsource.frequency = frequency
    acsource.on()
    sleep(2)
    
    for percent_load in range(100,-25,-25):
        if percent_load==0:
            eload.channel[1].off()
        else:
            eload.channel[1].cc = full_load * (percent_load/100)
            eload.channel[1].on()
        sleep(10)

        filename = f"DER717_Ripple_{voltage}VAC_CC {percent_load}% Load.png"
        path = "waveforms\\"
        scope.save_screenshot(filename, path)
        sleep(2)