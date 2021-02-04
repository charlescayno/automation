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

def test_no_load(input_list, soak_time, integration_time):
    headers("No Load")
    start_time = time.time()
    for voltage, frequency in input_list:
        ac.voltage = voltage
        ac.frequency = frequency
        ac.on()

        soak(soak_time)
        pm1.integrate(integration_time)

        # create output list
        vac = str(voltage)
        freq = str(frequency)
        vin = f"{pm1.voltage:.2f}"
        iin = f"{pm1.current*1000:.2f}"
        pin = f"{pm1.power:.5f}"
        pf = f"{pm1.pf:.4f}"
        output_list = [vac, freq, vin, iin, pin, pf]

        print(','.join(output_list))
    end_time = time.time()
    reset()
    footers(end_time-start_time)

ac = ACSource(address=5)
pm1 = PowerMeter(address=1)

# User inputs start here
input_list = [
    (90, 60), (100, 60), (115, 60), (130, 60), (150, 60), (180, 60),
    (200, 50), (220, 50), (230, 50), (240, 50), (250, 60), (265, 50),
]   # (voltage, frequency)
soak_time = 10                     # seconds
integration_time = 10               # seconds
# User inputs end here


test_no_load(input_list, soak_time, integration_time)