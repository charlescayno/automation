import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
print("CH2 - Input Current")
print("CH3 - LED Iout")
# input(">> Setup scope. Press ENTER to continue... ")

from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# PROJECT DETAILS
project = "DER-1050"
test = f"PF investigation - SR FET Trim Option 2"
unit = "layout 41"

excel_name = f'{unit}'
waveforms_folder = f"C:/Users/ccayno/Documents/Charles/Work/DER/{project}/5 - Test Data/{test}/"
path = path_maker(f'{waveforms_folder}')
########################################## USER INPUT ##########################################

def main():
 
    EQUIPMENT_FUNCTIONS().SCOPE().RECALL_SAVESET('C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2024/Iin-Iled.dfl')
    EQUIPMENT_FUNCTIONS().SCOPE().CHANNEL_SCALE(2, 2)
    input(">> Set SVF disabled...")
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(cc1=0.6, cc2=2.4, cc3=0.5)
    EQUIPMENT_FUNCTIONS().AC_TURN_ON(230)
    sleep(3)
    EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
    input(">> Press ENTER to capture waveform... ")
    
    sleep(3)
    EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
    sleep(3)
    vo1, io1, po1 = EQUIPMENT_FUNCTIONS()._pm_measurements1()
    io1 = EQUIPMENT_FUNCTIONS()._sigfig(io1, 2)
    vac, iin, pin, pf, thd = EQUIPMENT_FUNCTIONS()._pm_measurements_source()
    filename = f"{unit}_230Vac_SVFdis_nominal_power_LED={io1}mA"
    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(cc1=0.6, cc2=0, cc3=0.5)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    
    
    EQUIPMENT_FUNCTIONS().SCOPE().RECALL_SAVESET('C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2024/Iin-Iled.dfl')
    EQUIPMENT_FUNCTIONS().SCOPE().CHANNEL_SCALE(2, 2)
    input(">> Set SVF disabled...")
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(cc1=0.6, cc2=2.4, cc3=0.5)
    sleep(3)
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(cc1=0.6, cc2=5.8, cc3=0.5)
    EQUIPMENT_FUNCTIONS().AC_TURN_ON(230)
    sleep(3)
    EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
    input(">> Press ENTER to capture waveform... ")
    EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
    sleep(3)
    vo1, io1, po1 = EQUIPMENT_FUNCTIONS()._pm_measurements1()
    io1 = EQUIPMENT_FUNCTIONS()._sigfig(io1, 2)
    vac, iin, pin, pf, thd = EQUIPMENT_FUNCTIONS()._pm_measurements_source()
    filename = f"{unit}_230Vac_SVFdis_peak_power_LED={io1}mA"
    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(cc1=0.6, cc2=0, cc3=0.5)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)



    EQUIPMENT_FUNCTIONS().SCOPE().RECALL_SAVESET('C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2024/Iin-Iled-200mA.dfl')
    EQUIPMENT_FUNCTIONS().SCOPE().CHANNEL_SCALE(2, 0.2)
    input(">> Set SVF enabled...")
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(cc1=0.6, cc2=0, cc3=0.5)
    EQUIPMENT_FUNCTIONS().AC_TURN_ON(230)
    sleep(3)
    EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
    input(">> Press ENTER to capture waveform... ")
    EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
    sleep(4)
    vo1, io1, po1 = EQUIPMENT_FUNCTIONS()._pm_measurements1()
    io1 = EQUIPMENT_FUNCTIONS()._sigfig(io1, 2)
    vac, iin, pin, pf, thd = EQUIPMENT_FUNCTIONS()._pm_measurements_source()
    filename = f"{unit}_230Vac_SVFen_LED+CV1_PF={pf}_LED={io1}mA"
    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(cc1=0.6, cc2=0, cc3=0.5)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)



if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(4)
    headers(test)
    main()
    footers(waveform_counter)