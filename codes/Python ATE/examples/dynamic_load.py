from piph.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from time import sleep

acsource = ACSource(address=5)
powermeter_source = PowerMeter(address=1)
powermeter_load = PowerMeter(address=2)
eload = ElectronicLoad(address=8)
scope = Oscilloscope(address="169.254.159.200")

sleep(2)

eload.channel[3].t1 = 0.0005        # Seconds
eload.channel[3].t2 = 0.0005        # Seconds
eload.channel[3].l1 = 1.25          # Amps
# eload.channel[3].l2 = 0.625          # Amps
eload.channel[3].l2 = 0.0          # Amps
eload.channel[3].on()

voltage_list = [90, 115, 230, 265]
frequency_list = [60, 60, 50, 50]
for voltage, frequency in zip(voltage_list, frequency_list):
    acsource.voltage = voltage
    acsource.frequency = frequency
    acsource.on()
    sleep(2)

    scope.stop()
    sleep(2)
    scope.save_screenshot(filename=f"DER717_DynamicLoad_{voltage}VAC_0to100 Load.png", path="waveforms")
    scope.run()
    sleep(2)

acsource.off()


