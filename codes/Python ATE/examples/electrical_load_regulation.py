from piph.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope

import time

def headers(test_name):
    print("*"*50)
    print(f"Test: {test_name}")

def footers(time_elapsed):
    print("Finished")
    if time_elapsed<60:
        print(f"Time Elapsed: {time_elapsed} second(s)")
    elif time_elapsed<3600:
        print(f"Time Elapsed: {time_elapsed/60:.2f} minute(s)")
    else:
        print(f"Time Elapsed: {time_elapsed/3600:.2f} hour(s)")
    print("*"*50)
    print("")

def soak(soak_time):
    for seconds in range(soak_time, 0, -1):
        time.sleep(1)
        print(f"{seconds:5d}s", end="\r")
    print("       ", end="\r")

def reset():
    ac.off()
    eload.channel[1].cc = 0.5
    eload.channel[1].on()
    time.sleep(5)
    eload.channel[1].off()

def test_load_regulation(input_list, load_percent_list, line_soak_time, load_soak_time):
    headers("Load Regulation")
    start_time = time.time()
    for voltage, frequency in input_list:
        ac.voltage = voltage
        ac.frequency = frequency
        ac.on()
        eload.channel[1].cc = 1.25
        eload.channel[1].on()
        soak(line_soak_time)
        for load_percent in load_percent_list:
            eload.channel[1].cc = 1.25 * (load_percent / 100)
            eload.channel[1].on()
            soak(load_soak_time)

            # create output list
            vac = str(voltage)
            freq = str(frequency)
            vin = f"{pm1.voltage:.2f}"
            iin = f"{pm1.current*1000:.2f}"
            pin = f"{pm1.power:.3f}"
            pf = f"{pm1.pf:.4f}"
            thd = f"{pm1.thd:.2f}"
            vo1 = f"{pm2.voltage:.3f}"
            io1 = f"{pm2.current*1000:.2f}"
            po1 = f"{pm2.power:.3f}"
            vreg1 = f"{100*(float(vo1)-12)/12:.4f}"
            eff = f"{100*(float(po1))/float(pin):.4f}"

            output_list = [vac, freq, vin, iin, pin, pf, thd, vo1, io1, po1, vreg1, eff]

            print(','.join(output_list))
        print("")
    end_time = time.time()
    reset()
    footers(end_time-start_time)

ac = ACSource(address=5)
pm1 = PowerMeter(address=1)
pm2 = PowerMeter(address=2)
eload = ElectronicLoad(address=8)

# User inputs start here
input_list = [(90, 60), (115, 60), (230, 50), (265, 50)]   # (voltage, frequency)
line_soak_time = 10                     # seconds
load_soak_time = 6
large_load_step = range(100, -10, -10)
light_load_step = range(10, -1, -1)
# User inputs end here

test_load_regulation(input_list, large_load_step, line_soak_time, load_soak_time)
test_load_regulation(input_list, light_load_step, line_soak_time, load_soak_time)