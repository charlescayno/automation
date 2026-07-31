# COMMS
ac_source_address = 5
source_power_meter_address = 1
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.10.148"
# scope2_address = "10.125.10.227"

"""IMPORT DEPENDENCIES"""
import sys
import pyautogui
from time import sleep, time
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list
import os
from powi.equipment import LEDControl
waveform_counter = 0


"""INITIALIZE EQUIPMENT"""
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)
# led = LEDControl()

### USER INPUT STARTS HERE ###
########################################################################
led_list = [46,36,24]
# led_list = convert_argv_to_int_list(sys.argv[1])

vin_list = [90,115,230,277, 300]
# vin_list = convert_argv_to_int_list(sys.argv[2])

pulse_time_list = [0.3, 1, 5] #s

test = f"AC Cycling"
waveforms_folder = f'waveforms/{test}'
########################################################################
### USER INPUT ENDS HERE ###

"""DEFAULT FUNCTIONS"""

def discharge_output():
    ac.turn_off()
    eload.channel[1].cr = 100
    eload.channel[1].turn_on()
    eload.channel[2].cr = 100
    eload.channel[2].turn_on()
    eload.channel[3].cr = 100
    eload.channel[3].turn_on()
    
    sleep(1)
    
    eload.channel[1].turn_off()
    eload.channel[2].turn_off()
    eload.channel[3].turn_off()

    eload.channel[1].cc = 1
    eload.channel[1].turn_on()
    eload.channel[2].cc = 1
    eload.channel[2].turn_on()
    eload.channel[3].cc = 1
    eload.channel[3].turn_on()
    
    sleep(1)

    eload.channel[1].turn_off()
    eload.channel[2].turn_off()
    eload.channel[3].turn_off()

def ac_cycle(vin, dwell):

    ac.write("TRIG:TRAN:SOUR BUS")
    ac.write("ABORT")
    ac.write("ABORT")
    if dwell > 1: init_dwell = 15
    else: init_dwell = 5
    ac.write(f"LIST:DWEL {init_dwell}, {dwell}, {dwell}, {dwell}, {dwell}, {dwell}, {dwell}, {dwell}, {dwell}, 14")
    ac.write("VOLT:MODE LIST")
    ac.write(f"LIST:VOLT {vin}, 0, {vin}, 0, {vin}, 0, {vin}, 0, {vin}, {vin}")
    ac.write("VOLT:SLEW:MODE LIST")
    ac.write("LIST:VOLT:SLEW 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037")
    ac.write("FREQ:MODE LIST")

    freq = ac.set_freq(vin)

    ac.write(f"LIST:FREQ {freq}, {freq}, {freq}, {freq}, {freq}, {freq}, {freq}, {freq}, {freq}, {freq}")
    ac.write("FREQ:SLEW:MODE LIST")
    ac.write("LIST:FREQ:SLEW 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037")
    ac.write("VOLT:OFFS:MODE LIST")
    ac.write("LIST:VOLT:OFFS 0, 0, 0, 0, 0, 0, 0, 0, 0, 0")
    ac.write("VOLT:OFFS:SLEW:MODE LIST")
    ac.write("LIST:VOLT:OFFS:SLEW 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037, 9.9e+037")
    ac.write("PHAS:MODE LIST")
    ac.write("LIST:PHAS 0, 0, 0, 0, 0, 0, 0, 0, 0, 0")
    ac.write("CURR:PEAK:MODE LIST")
    ac.write("LIST:CURR 13, 13, 13, 13, 13, 13, 13, 13, 13, 13")
    ac.write("FUNC:MODE LIST")
    ac.write("LIST:SHAP SINUSOID, SINUSOID, SINUSOID, SINUSOID, SINUSOID, SINUSOID, SINUSOID, SINUSOID, SINUSOID, SINUSOID")
    ac.write("LIST:TTLT ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF")
    ac.write("LIST:STEP AUTO")
    ac.write("OUTP:TTLT:STAT ON")
    ac.write("OUTP:TTLT:SOUR LIST")
    ac.write("TRIG:SYNC:SOUR PHASE")
    ac.write("TRIG:SYNC:PHAS 0.0")
    ac.write("TRIG:TRAN:DEL 0")
    ac.write("Sens:Swe:Offs:Poin 0")
    ac.write("TRIG:ACQ:SOUR TTLT")
    ac.write("INIT:IMM:SEQ3")
    ac.write("LIST:COUN 1")
    ac.write("INIT:IMM:SEQ1")
    ac.write("TRIG:TRAN:SOUR BUS")
    ac.write("TRIG:IMM")


def scope_settings():


    scope.stop()
    scope.position_scale(time_position = 10, time_scale = 0.2)
    scope.edge_trigger(2, 50, 'POS')

    scope.channel_settings(1, 0.25, -4, 'Iout')
    scope.channel_settings(2, 100, -4, 'Vds')
    scope.channel_state(3, 'OFF')
    scope.channel_state(4, 'OFF') # if you wanna off the channel
    scope.add_zoom(rel_pos = 15.5, rel_scale = 15)


def main():

    global waveform_counter

    for LED in led_list:

        # led.voltage(LED)
        input("Change LED load.")

        for vin in vin_list:

            for pulse_time in pulse_time_list:

                if pulse_time > 1:
                    scope.time_scale(pulse_time)
                else:
                    scope.time_scale(2)

                if LED == 'NL':
                    scope.timeout_trigger(trigger_source=2, timeout_range='LOW', timeout_time=12E-3)
                    # scope.cursor(channel=4, cursor_set=1, X1=pulse_time, X2=2*pulse_time, Y1=vr_min, Y2=vr_max, type='HOR')
                else:
                    scope.edge_trigger(1, 0.15, 'NEG')
                    scope.cursor(channel=4, cursor_set=1, X1=pulse_time, X2=2*pulse_time, Y1=12.7, Y2=17.403, type='PAIR')
                # div = float(scope.get_horizontal()['scale'])

                ac.voltage = vin
                ac.frequency = ac.set_freq(vin)
                ac.turn_on()

                if LED == "NL": sleep(5)
                else: sleep(1)

                scope.run_single()
                
                ac_cycle(vin, pulse_time)

                if pulse_time > 1: sleep(60)
                else: sleep(25)

                if LED == "NL": input("Adjust cursor before capturing waveform.")
                
                filename = f"{LED}, {vin}Vac, {pulse_time}s on-off.png"
                path = waveforms_folder + f'/{LED}V'
                if not os.path.exists(path): os.mkdir(path)
                scope.get_screenshot(filename, path)
                print(filename)
                waveform_counter += 1

if __name__ == "__main__":
    discharge_output()
    headers(test)
    scope.stop()
    main()
    discharge_output()
