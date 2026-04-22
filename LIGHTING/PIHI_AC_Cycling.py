from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
from misc_codes.equipment_settings import EQUIPMENT_FUNCTIONS as EF
from battery_discharge import main_battery_discharge
########################################## USER INPUT ##########################################
# INPUT
vin_list = [90,100,120,132]
# vin_list = [120]
# OUTPUT

pulse_count = 10
pulse_list = [0.1, 0.3, 0.5, 1]
adc_sampling_time = 300     # us sampling time
line_transient_limit = 3    # VAC

# PROJECT DETAILS
project = "DER-999"
test = f"AC Cycling During Fully Charged"
excel_name = f"{project} {test}"

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################
from math import ceil, floor
def round_to_multiple(number, multiple, direction='nearest'):
    if direction == 'nearest':
        return multiple * round(number / multiple)
    elif direction == 'up':
        return multiple * ceil(number / multiple)
    elif direction == 'down':
        return multiple * floor(number / multiple)
    else:
        return multiple * round(number / multiple)

def _set_time_scale(pulse):
    time_division = pulse
    time_scale = 2*time_division
    start_soak_time = 3*time_scale
    off_time = pulse
    on_time = pulse
    # end_soak_time = 20
    end_soak_time = 20
    delay = start_soak_time + end_soak_time + (pulse_count*(off_time + on_time)) + off_time
    computed_time_scale = round_to_multiple(delay, 5, 'up')/10
    print(computed_time_scale)
    # input()
    scope.time_scale(computed_time_scale)

    return start_soak_time, off_time, on_time, end_soak_time


def main():
    for pulse in pulse_list:
        start_soak_time, off_time, on_time, end_soak_time = _set_time_scale(pulse)

        for vin in vin_list:
            EF().AC_TURN_ON(vin)
            scope.run()
            soak(60)
            EF().AC_CYCLING(pulse_count, vin, start_soak_time, off_time, on_time, end_soak_time)
            scope.stop()
            filename  = f"{pulse}s AC cycling at {vin}VAC - sampled every {adc_sampling_time} us, {line_transient_limit} VAC"
            EF().AC_TURN_OFF()
            # input(">> Adjust cursors. Capture waveform?")
            EF().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)
            

    

if __name__ == "__main__":
 
    headers(test)
    main()
    footers(waveform_counter)
