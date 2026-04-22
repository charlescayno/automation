from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [230]

# OUTPUT
""" LED """
vout_nom_1 = 36
iout_nom_1 = 0.6
""" CV2 """
vout_nom_2 = 24
iout_nom_2 = 0
""" CV1 """
vout_nom_3 = 5
iout_nom_3 = 0

short = False
pause_to_adjust_scope = True

start = 1
end = 2
step = 1

how_many_cycle = 5

# PROJECT DETAILS
project = "DER-1050"
test = f"AC Cycling"
unit = "BPP 200R"
excel_name = f'{project}_{unit}'

from datetime import datetime
now = datetime.now()
print("now =", now)
dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
print("date and time =", dt_string)

waveforms_folder = f"C:/Users/ccayno/Documents/Charles/Work/DER/{project}/5 - Test Data/{test}/{unit}/{dt_string}"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path

########################################## USER INPUT ##########################################
def main():

    
    
    no_of_iterations = ((end + step - start)/step) + 1
    no_of_iterations = EQUIPMENT_FUNCTIONS().two_sig_fig(no_of_iterations)
    print(f"no of iterations = {no_of_iterations}")

    for i in np.arange(start, end+step, step):
        
        i = EQUIPMENT_FUNCTIONS()._sigfig(i, 3)
        print(f"\n{i} s short")

        if i != 1213:
            soak_for_short = i
            EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(0, 0, 0)
            CV2_load = EQUIPMENT_FUNCTIONS().two_sig_fig(vout_nom_2*iout_nom_2)
            CV1_load = EQUIPMENT_FUNCTIONS().two_sig_fig(vout_nom_3*iout_nom_3)
            LED_load = EQUIPMENT_FUNCTIONS().two_sig_fig(vout_nom_1*iout_nom_1)

            """ INITIAL LOADING """        
            EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(0, 0, 0.5)
            # EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(7, 0)
            scope.run_single()
            sleep(1)

            """ INITIAL POWER """
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
            soak(3)

            for i in range(how_many_cycle):


                """ TURN OFF AC """
                EQUIPMENT_FUNCTIONS().AC_TURN_OFF()

                """ SHORT FOR <soak_for_short> s """
                if short:
                    EQUIPMENT_FUNCTIONS().ANALOG_DC_ON(1, 5, 0.02)
                    sleep(0.5)
                    EQUIPMENT_FUNCTIONS().ANALOG_DC_OFF()
                    filename = f"{vin_list[0]}Vac, CV1 load={CV1_load}W, CV2 load={CV2_load}W, LED load={LED_load}W, {unit} short for {EQUIPMENT_FUNCTIONS()._sigfig(soak_for_short*1000, 0)}ms"
                else:
                    sleep(0.5)
                    filename = f"{vin_list[0]}Vac, CV1 load={CV1_load}W, CV2 load={CV2_load}W, LED load={LED_load}W, off for {EQUIPMENT_FUNCTIONS()._sigfig(soak_for_short*1000, 0)}ms"

                sleep(1)

                """ TURN BACK THE POWER """
                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
                sleep(1)

            """ WAIT  """
            soak(5)
            

            """ CAPTURE SCREENSHOT"""
            scope.stop()
            if pause_to_adjust_scope:
                input("Capture waveform?")
            EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
            EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(3)
            for i in range(5):
                EQUIPMENT_FUNCTIONS().ANALOG_DC_ON(1, 5, 0.02)
                sleep(0.2)
                EQUIPMENT_FUNCTIONS().ANALOG_DC_OFF()
                sleep(0.2)


if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(3)
    for i in range(5):
        EQUIPMENT_FUNCTIONS().ANALOG_DC_ON(1, 5, 0.02)
        sleep(0.2)
        EQUIPMENT_FUNCTIONS().ANALOG_DC_OFF()
        sleep(0.2)
    headers(test)
    main()
    footers(waveform_counter)
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
