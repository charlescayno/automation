from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl, Keithley_DC_2230G
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list
from time import time, sleep
import pyautogui
from playsound import playsound


dc = Keithley_DC_2230G('1')
ac = ACSource(30)

vin_list = [120,230,277]
led_list = [46,36,24]
dim_list = [0,1,2,3,4,5,6,7,8,9,10]
soaktime = 10

condition_list = ['UNCASED']
condition_list = ['3D_PRINTED_CASE']
condition_list = ['METAL_CASE']

test = f'Audible Noise'
waveforms_folder = f'waveforms/{test}'


def set_dim(dim):
    print(f'Dim: {dim}V')
    dc.set_volt_curr(channel ='CH1', voltage = dim, current = 1.0)
    dc.channel_state(channel ='CH1', state = 'ON')
    soak(soaktime)

def get_noise_floor():
    playsound("Press START to get Noise Floor.mp3")
    input(">> Press START to get Noise Floor")

def get_audible_noise():
    playsound("Get Audible Noise.mp3")
    # input(f">> Press Enter to continue")
    soak(8)

def save_data():
    playsound("Save RMS Level graph.mp3")
    sleep(6)
    playsound("Export xlsx file.mp3")
    sleep(5)
    playsound("Save project file.mp3")
    sleep(5)
    playsound("Clear all data.mp3")
    sleep(5)
    playsound("press_enter_to_continue.mp3")
    input("Press ENTER to continue")

def reset():
    ac.turn_off()
    dc.channel_state_all(state='OFF')
    playsound("Discharge output.mp3")
    input(">> Discharge output.")
    print()

def set_freq(vin):
    if vin >= 180 and vin <= 265: ac_freq = 50
    else: ac_freq = 60
    return ac_freq

def main():
    reset()
    for condition in condition_list:
        print(f'\nCondition: {condition}\n')
        for led in led_list:
            playsound("Change LED load.mp3")
            input(f">> Change LED load to {led}V")
            for vin in vin_list:

                print(f'[{led}V {vin}Vac {condition}]')
                
                get_noise_floor()
                
                ac.write(f"VOLT:AC {vin}")
                ac_freq = set_freq(vin)
                ac.write(f"FREQ {ac_freq}")
                ac.turn_on()
                
                sleep(2)
                for dim in dim_list:
                    set_dim(dim)
                    get_audible_noise()
                save_data()
                reset()

if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter) 
