#########################################################################################
# COMMS
ac_source_address = 5
source_power_meter_address = 2 
load_power_meter_address = 1
eload_address = 8
# scope_address = "10.125.10.112"
#########################################################################################

from powi.equipment import ACSource, DCSource, PowerMeter, ElectronicLoad, Oscilloscope
from powi.equipment import headers, create_folder, footers, waveform_counter
from time import sleep, time
import os

# initialize equipment
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
# scope = Oscilloscope(scope_address)

def ac_reset():
    ac.turn_off()
    eload.channel[1].cc = 1
    eload.channel[1].turn_on()
    eload.channel[2].cc = 1
    eload.channel[2].turn_on()
    sleep(1)

def soak(soak_time):
    for seconds in range(soak_time, 0, -1):
        sleep(1)
        print(f"{seconds:5d}s", end="\r")
    print("       ", end="\r")

def test_line_regulation(input_list, soak_time=5, integration_time=10):
    headers("Line Regulation")
    
    print("vdc, vin, iin, pin, pf, thd, vo1, io1, po1, eff")
    print()
    
    for voltage in input_list:
        ac.cv = voltage
        ac.turn_on()

        soak(soak_time)
        pms.integrate(integration_time)

        # create output list
        vdc = str(voltage)
        vin = f"{pms.voltage:.2f}"
        iin = f"{pms.current*1000:.2f}"
        pin = f"{pms.power:.3f}"
        pf = f"{pms.pf:.4f}"
        thd = f"{pms.thd:.2f}"
        vo1 = f"{pml.voltage:.3f}"
        io1 = f"{pml.current*1000:.2f}"
        po1 = f"{pml.power:.3f}"
        vreg1 = f"{100*(float(vo1)-vout)/vout:.4f}"
        eff = f"{100*(float(po1))/float(pin):.4f}"


        output_list = [vdc, vin, iin, pin, pf, thd, vo1, io1, po1, vreg1, eff]
        # print(output_list)

        print(','.join(output_list))

    ac_reset()

def test_load_regulation(input_list, load_percent_list, line_soak_time, load_soak_time, integration_time=10):
    headers("Load Regulation")

    print("vdc, vin, iin, pin, pf, thd, vo1, io1, po1, eff")
    print()

    for voltage in input_list:
        ac.voltage = voltage
        ac.turn_on()

        eload.channel[1].cc = 1.25
        eload.channel[1].turn_on()
        soak(line_soak_time)

        for load_percent in load_percent_list:
            eload.channel[1].cc = Iout_max * (load_percent / 100)
            eload.channel[1].turn_on()
            soak(load_soak_time)
            pms.integrate(integration_time)

            # create output list
            vdc = str(voltage)
            vin = f"{pms.voltage:.2f}"
            iin = f"{pms.current*1000:.2f}"
            pin = f"{pms.power:.3f}"
            pf = f"{pms.pf:.4f}"
            thd = f"{pms.thd:.2f}"
            vo1 = f"{pml.voltage:.3f}"
            io1 = f"{pml.current*1000:.2f}"
            po1 = f"{pml.power:.3f}"
            vreg1 = f"{100*(float(vo1)-vout)/vout:.4f}"
            eff = f"{100*(float(po1))/float(pin):.4f}"

            output_list = [vdc, vin, iin, pin, pf, thd, vo1, io1, po1, vreg1, eff]

            print(','.join(output_list))
        print("")

    ac_reset()

def test_no_load(input_list, soak_time=5, integration_time=10):
    headers("No Load")
    print("vdc, vin, iin, pin, pf")
    print()
    
    for voltage in input_list:
        ac.cv = voltage
        ac.turn_on()

        soak(soak_time)
        pms.integrate(integration_time)

        # create output list
        vdc = str(voltage)
        vin = f"{pms.voltage:.2f}"
        iin = f"{pms.current*1000:.2f}"
        pin = f"{pms.power:.3f}"
        pf = f"{pms.pf:.4f}"


        output_list = [vdc, vin, iin, pin, pf]

        print(','.join(output_list))

    ac_reset()


## main code ##

## OUTPUT
vout = 48
Iout_max = 780 # A

input_list = [90,115,230,265]  # dc voltages
load_percent_list = [100, 75, 50, 25]

integration_time = 120 #s
soak_time = 1 #s
load_soak_time = 1 #s


# test_line_regulation(input_list, soak_time, integration_time)
print()

test_load_regulation(input_list, load_percent_list, soak_time, load_soak_time, integration_time)
print()

# test_no_load(input_list, soak_time, integration_time)
print()


































footers(waveform_counter)