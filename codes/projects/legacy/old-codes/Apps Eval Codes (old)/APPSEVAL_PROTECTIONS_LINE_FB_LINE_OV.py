print("CMC | 07OCT2021")
print("CHANNEL 1: IOUT")
print("CHANNEL 2: VR")
print("CHANNEL 3: VIN")
print("CHANNEL 4: VOUT")

"""LIBRARIES"""
from time import time, sleep
import sys
import os
import math
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt
import winsound as ws
from playsound import playsound
waveform_counter = 0

"""COMMS"""
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2    
eload_address = 8
scope_address = "10.125.11.0"

"""EQUIPMENT INITIALIZE"""
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)
led = LEDControl()

"""USER INPUT"""
led_list = [46,36,24]
# led_list = [46,36,24,0]
IOUT = 0.35 #A
start = 100
mid = 0
end = 100

slew_rate = 1
frequency = 60

test = "Line Foldback (LYT8365C)"
waveforms_folder = f'waveforms/{test}'
"""DO NOT EDIT BELOW THIS LINE"""


"""GENERIC FUNCTIONS"""
def discharge_output():
    ac.turn_off()
    for i in range(1,9):
        eload.channel[i].cc = 1
        eload.channel[i].turn_on()
        eload.channel[i].short_on()
    sleep(2)
    for i in range(1,9):
        eload.channel[i].turn_off()
        eload.channel[i].short_off()
    sleep(1)



def scope_settings():
    scope.remove_zoom()
    scope.position_scale(time_position = 50, time_scale = 2) # initial setting
    scope.edge_trigger(1, 0.5, 'POS')
    scope.trigger_mode('AUTO')

    scope.channel_settings(state='ON', channel=1, scale=0.1, position=-2, label="IOUT", color='PINK', rel_x_position=20, bandwidth=500, coupling='DCLimit', offset=0)
    scope.channel_settings(state='ON', channel=2, scale=10, position=-3, label="VR", color='LIGHT_BLUE', rel_x_position=40, bandwidth=500, coupling='DCLimit', offset=0)
    scope.channel_settings(state='ON', channel=3, scale=40, position=0, label="VIN", color='YELLOW', rel_x_position=60, bandwidth=500, coupling='AC', offset=0)
    scope.channel_settings(state='ON', channel=4, scale=10, position=-2, label="VOUT", color='GREEN', rel_x_position=80, bandwidth=500, coupling='DCLimit', offset=0)


def browning(start, end, slew, frequency):

    if start > end:
        # print(f"brownout: {start} -> {end} Vac")
        for voltage in range(start, end+1, -slew):
            ac.voltage = voltage
            ac.frequency = frequency
            ac.turn_on()
            sleep(1)
    if start < end:
        # print(f"brownin: {start} -> {end} Vac")
        for voltage in range(start, end+1, slew):
            ac.voltage = voltage
            ac.frequency = frequency
            ac.turn_on()
            sleep(1)

def fixvoltage(voltage, soak):
    ac.voltage = voltage
    ac.frequency = ac.set_freq(voltage)
    ac.turn_on()
    sleep(soak)

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

def line_foldback(start, mid, end, slew_rate, frequency, led):

    global waveform_counter

    if led != 0:

        scope_settings()
        print(f"\n>> {start}-{mid}-{end} Vac, {slew_rate}V_s, {led}V")

        # SETTING TIME SCALE AND DELAYS
        test_time = (abs(mid-start)/slew_rate)+(abs(end-mid)/slew_rate)
        delay1 = 20
        delay2 = 20
        scope_time = test_time + delay1 + delay2
        time_scale = scope_time/10
        scope.time_scale(time_scale)

        # INITIAL POWERUP
        ac.voltage = start
        ac.frequency = frequency
        ac.turn_on()
        soak(5)

        # LINE FOLDBACK OPERATION
        scope.run()
        soak(delay1)
        browning(start, mid, slew_rate, frequency)
        browning(mid, end, slew_rate, frequency)
        soak(delay2)
        scope.stop()

        filename = f"{start}-{mid}-{end} Vac, {slew_rate}V_s, {led}V.png"
        path = waveforms_folder + f'/Line Foldback (Line UV)'
        if not os.path.exists(path): os.mkdir(path)
        scope.get_screenshot(filename, path)
        waveform_counter += 1
        print(filename)

        discharge_output()

def line_foldback_step_input(start, mid, end, frequency, led):

    global waveform_counter

    if led != 0:

        scope_settings()
        scope.trigger_mode('NORM')
        iout_trigger = IOUT/2
        scope.edge_trigger(1, iout_trigger, 'POS')


        print(f"\n>> {start}-{mid}-{end} Vac, Step Input, {led}V")

        # SETTING TIME SCALE AND DELAYS
        scope_time = 100
        time_scale = scope_time/10
        scope.time_scale(time_scale)

        # LINE FOLDBACK STEP-INPUT OPERATION
        scope.run()
        soak(int(2*time_scale))
        fixvoltage(start, soak=2*time_scale)
        fixvoltage(mid, soak=3*time_scale)
        fixvoltage(end, soak=3*time_scale)
        scope.stop()

        # SCOPE CAPTURE
        filename = f"{start}-{mid}-{end} Vac, Step Input, {led}V.png"
        path = waveforms_folder + f'/Line Foldback (Line UV) - Step Input'
        if not os.path.exists(path): os.mkdir(path)
        scope.get_screenshot(filename, path)
        waveform_counter += 1
        print(filename)

        discharge_output()


def line_ov(start, end, slew_rate, frequency, led):
    global waveform_counter

    if led != 0:

        # print("Change CH1 to IOUT.")
        
        scope_settings()
        scope.trigger_mode('NORM')
        iout_trigger = IOUT/2
        scope.edge_trigger(1, iout_trigger, 'POS')
        scope.channel_settings(state='ON', channel = 1, scale = 0.1, position = -2, label="IOUT", color='PINK', rel_x_position=20, bandwidth=500, coupling='DCLimit', offset=0)
        scope.channel_settings(state='ON', channel=3, scale=100, position=0, label="VIN", color='YELLOW', rel_x_position=60, bandwidth=500, coupling='AC', offset=0)
        slew_rate = 1

        print(f"\n>> {start}-{end} Vac, Vin Sweep, {led}V")

        # SETTING TIME SCALE AND DELAYS
        scope_time = 100
        time_scale = scope_time/10
        scope.time_scale(time_scale)

        # LINE OV
        scope.run()
        sleep(2*time_scale)
        fixvoltage(start, soak=2*time_scale)
        browning(start, end, slew_rate, frequency)
        fixvoltage(end, soak=5*time_scale)
        scope.stop()

        # SCOPE CAPTURE
        filename = f"{start}-{end} Vac, Vin Sweep, {led}V.png"
        path = waveforms_folder + f'/Line OV (Vin Sweep)'
        if not os.path.exists(path): os.mkdir(path)
        scope.get_screenshot(filename, path)
        waveform_counter += 1
        print(filename)

        discharge_output()
    
    if led == 0:

        # print("Change CH1 to IPRI.")

        scope_settings()
        scope.trigger_mode('NORM')
        scope.edge_trigger(1, 1, 'POS') # IPRI
        scope.channel_settings(state='ON', channel = 1, scale = 1, position = -4, label="IOUT", color='PINK', rel_x_position=20, bandwidth=500, coupling='DCLimit', offset=0)
        scope.channel_settings(state='ON', channel = 3, scale = 100, position = 0, label="VIN", color='YELLOW', rel_x_position=60, bandwidth=500, coupling='AC', offset=0)
        slew_rate = 1

        print(f"\n>> {start}-{end} Vac, Vin Sweep, NL")

        # SETTING TIME SCALE AND DELAYS
        scope_time = 100
        time_scale = scope_time/10
        scope.time_scale(time_scale)

        # LINE OV
        scope.run()
        sleep(2*time_scale)
        fixvoltage(start, soak=2*time_scale)
        browning(start, end, slew_rate, frequency)
        fixvoltage(end, soak=5*time_scale)
        scope.stop()

        # input("Capture waveform?")

        # SCOPE CAPTURE
        filename = f"{start}-{end} Vac, Vin Sweep, NL.png"
        path = waveforms_folder + f'/Line OV (Vin Sweep)'
        if not os.path.exists(path): os.mkdir(path)
        scope.get_screenshot(filename, path)
        waveform_counter += 1
        print(filename)

        discharge_output()

def startup_at_high_input(vin, led):

    global waveform_counter

    print("Change CH1 to IPRI.")

    scope_settings()
    scope.trigger_mode('NORM')
    scope.edge_trigger(1, 1, 'POS') # IPRI

    scope.channel_settings(state='ON', channel = 1, scale = 1, position = -4, label="IOUT", color='PINK', rel_x_position=20, bandwidth=500, coupling='DCLimit', offset=0)
    scope.channel_settings(state='ON', channel=3, scale=100, position=0, label="VIN", color='YELLOW', rel_x_position=60, bandwidth=500, coupling='AC', offset=0)

    scope.remove_zoom()

    # SETTING TIME SCALE AND DELAYS
    scope_time = 20
    time_scale = scope_time/10
    scope.time_scale(time_scale)

    if led != 0:
        print(f"\n>> Startup at High Input ({vin}Vac), {led}V")

        # STARTUP AT HIGH INPUT
        scope.run()
        sleep(3*time_scale)
        fixvoltage(vin, soak=8*time_scale)
        scope.stop()

        # SCOPE CAPTURE
        filename = f"Startup at High Input ({vin}Vac), {led}V.png"
        path = waveforms_folder + f'/Line OV (Startup at High Input)'
        if not os.path.exists(path): os.mkdir(path)
        scope.get_screenshot(filename, path)
        waveform_counter += 1
        print(filename)

        # SCOPE CAPTURE (w/ zoom)
        scope.remove_zoom()
        scope.add_zoom(rel_pos = 21, rel_scale = 1)
        sleep(5)
        filename = f"Startup at High Input ({vin}Vac), {led}V (zoomed).png"
        path = waveforms_folder + f'/Line OV (Startup at High Input)'
        if not os.path.exists(path): os.mkdir(path)
        scope.get_screenshot(filename, path)
        waveform_counter += 1
        print(filename)
        scope.remove_zoom()

        discharge_output()

    if led == 0:
        print(f"\n>> Startup at High Input ({vin}Vac), NL")

        # STARTUP AT HIGH INPUT
        scope.run()
        sleep(3*time_scale)
        fixvoltage(vin, soak=8*time_scale)
        scope.stop()

        # SCOPE CAPTURE
        filename = f"Startup at High Input ({vin}Vac), NL.png"
        path = waveforms_folder + f'/Line OV (Startup at High Input)'
        if not os.path.exists(path): os.mkdir(path)
        scope.get_screenshot(filename, path)
        waveform_counter += 1
        print(filename)

        # SCOPE CAPTURE (w/ zoom)
        scope.remove_zoom()
        scope.add_zoom(rel_pos = 21, rel_scale = 1)
        sleep(5)
        filename = f"Startup at High Input ({vin}Vac), NL (zoomed).png"
        path = waveforms_folder + f'/Line OV (Startup at High Input)'
        if not os.path.exists(path): os.mkdir(path)
        scope.get_screenshot(filename, path)
        waveform_counter += 1
        print(filename)
        scope.remove_zoom()

        discharge_output()


def line_foldback_test(LED, slew_rate):
    line_foldback(start=100, mid=0, end=100, slew_rate=slew_rate, frequency=frequency, led=LED)
    line_foldback(start=100, mid=70, end=100, slew_rate=slew_rate, frequency=frequency, led=LED)
    line_foldback(start=100, mid=60, end=100, slew_rate=slew_rate, frequency=frequency, led=LED)
    line_foldback(start=100, mid=50, end=100, slew_rate=slew_rate, frequency=frequency, led=LED)

def line_foldback_test_step_input(LED):
    line_foldback_step_input(start=100, mid=0, end=100, frequency=frequency, led=LED)
    line_foldback_step_input(start=100, mid=70, end=100, frequency=frequency, led=LED)
    line_foldback_step_input(start=100, mid=60, end=100, frequency=frequency, led=LED)
    line_foldback_step_input(start=100, mid=50, end=100, frequency=frequency, led=LED)

def line_ov_test(LED, slew_rate):
    line_ov(270, 296, slew_rate, frequency, LED)
    line_ov(286, 260, slew_rate, frequency, LED)

def startup_at_high_input_test(LED):
    
    startup_at_high_input(280, LED)
    startup_at_high_input(275, LED)
    startup_at_high_input(270, LED)
    startup_at_high_input(260, LED)

def main():

    global waveform_counter
    scope_settings()

    prompt("Change Channel 1 to Drain Current")

    for LED in led_list:
        led.voltage(LED)
        sleep(2)

        line_foldback_test(LED, slew_rate=1)
        line_foldback_test(LED, slew_rate=5)
        line_foldback_test_step_input(LED)

        print("Make sure to change RLS to 7.1 Mohms for 282Vac Line OV Setpoint.")
        line_ov_test(LED, slew_rate=1)
    
    prompt("Change Channel 1 from Output Current to Drain Current")

    input(">> CH1: IOUT -> IPRI")
    print("Make sure to change RLS to 7.1 Mohms for 282Vac Line OV Setpoint.")
    line_ov_test(0, slew_rate=1)
    startup_at_high_input_test(0)
    for LED in led_list:
        led.voltage(LED)
        sleep(2)
        startup_at_high_input_test(LED)



    




        

        




if __name__ == "__main__":
    headers(test)
    discharge_output()
    main()
    discharge_output()
    footers(waveform_counter)
    ws.PlaySound("dingding.wav", ws.SND_ASYNC)
    sleep(2)    
