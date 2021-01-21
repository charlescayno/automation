from piph.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from time import sleep

acsource = ACSource(address=5)
powermeter_source = PowerMeter(address=1)
powermeter_load = PowerMeter(address=2)
eload = ElectronicLoad(address=8)
scope = Oscilloscope(address="169.254.159.200")

def startup_zero_angle(voltage, frequency):
    acsource.voltage = 0
    acsource.frequency = frequency
    acsource.on()
    acsource.ac.conn.write("VOLT:MODE PULS")
    acsource.ac.conn.write(f"VOLT:TRIG {voltage}")
    acsource.ac.conn.write("PULS:WIDT 1")
    acsource.ac.conn.write("TRIG:SOUR BUS")
    acsource.ac.conn.write("TRIG:SYNC:SOUR PHAS")
    acsource.ac.conn.write("TRIF:SYNC:PHAS 0")
    acsource.ac.conn.write("INIT:SEQ1")
    sleep(1)
    acsource.ac.conn.write("*TRG")


full_load = 1.25
voltage_list = [90, 115, 230, 265]
frequency_list = [60, 60, 50, 50]

for voltage, frequency in zip(voltage_list, frequency_list):
    for percent_load in [0, 100]:
        if percent_load==0:
            eload.channel[1].off()
        else:
            eload.channel[1].cc = full_load * (percent_load/100)
            # eload.channel[1].cr = full_load * (percent_load/100)
            eload.channel[1].on()
        sleep(2)

        startup_zero_angle(voltage, frequency)
        sleep(2)

        # filename = f"DER877_Startup Vo_{voltage}VAC_CR {percent_load}% Load.png"
        filename = f"DER877_Startup Vds Ids_{voltage}VAC_CC {percent_load}% Load.png"
        path = "waveforms\\"
        scope.save_screenshot(filename, path)
        sleep(2)

        
        eload.channel[1].cc = full_load
        # eload.channel[1].cr = full_load
        eload.channel[1].on()
        sleep(2)

        scope.run_single()