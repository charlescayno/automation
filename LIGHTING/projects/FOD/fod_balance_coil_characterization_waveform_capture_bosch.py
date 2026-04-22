import sys, os
_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
# from misc_codes.scope_setter import scope_settings
# from misc_codes.scope_settings_fod import SCOPE_CONFIG
# scope_settings(SCOPE_CONFIG)
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [120]
unit = 1
channel_list = [1,3,4]

vout = 18
iout = 3

# PROJECT DETAILS
project = "DER-999"
test = f"FOD Characterization for BOSCH"
FO_list = ['Coin', 'Paper Clip (Parallel)','Paper Clip (Perp)', '1x0.67x10mils Cu (Parallel)', '1x0.67x10mils Cu (Perp)']
FO_list = ['Paper Clip']
condition_list = ['(-1, 0)', '(+1, 0)', '(0, +1)', '(0, -1)', '(0, 0)']
condition_list = ['off-center', 'centered']

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################
def main():
    FO_index = 0
    for FO in FO_list:
        excel_name = f"{FO}"
        create_header_for_df()
        EQUIPMENT_FUNCTIONS().AC_TURN_OFF()
        for vin in vin_list:
            
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            soak(10)

            fod_test(excel_name, vin, condition="NA", foreign_object=FO, type='No FO')

            for condition in condition_list:
                fod_test(excel_name, vin, condition, foreign_object=FO, type=FO)
                
        GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
        EQUIPMENT_FUNCTIONS().AC_TURN_OFF()
        FO_index += 1
        try:
            input(f">> Press ENTER to continue to the next FO ({FO_list[FO_index]})...")
        except:
            pass



def fod_test(excel_name, vin, condition, foreign_object, type='No FO'):
    """
        condition: No FO or FO orientation on XY axis
        foreign_object: foreign object used for the test
        type: user-define whether to get No FO condition or not
    """

    scope.run()
    
    if type == 'No FO':
        input(f">> No FO. Press ENTER to continue...")
        filename = f"No FO"
        
    else:
        input(f">>{foreign_object} at {condition}. Press ENTER to continue...")
        filename = f"{foreign_object} at {condition}"
    
    scope.stop()

    
    path = path_maker(waveforms_folder + f'/{foreign_object}')
    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)

    output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_SCOPE(vin, vout, iout, filename, channel_list)
    export_to_excel(df, path, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="B2")

def create_header_for_df():
    global df
    """CREATING HEADER LIST"""
    header_list = ['CC (A)', 'Vin (rms)', 'Freq (Hz)', 'Vac (VAC)', 'Iin (mA)', 'Pin (W)', 'PF', 'THD (%)', 'Vo (V)', 'Io1 (A)', 'Po (W)', 'Vreg (%)', 'Ireg (%)', 'Eff (%)']
    header_list.append("Conditions")
    for channel in channel_list:
        header_list = EQUIPMENT_FUNCTIONS().APPEND_SCOPE_LABELS(header_list, channel)
    header_list.append("C1 Y1")
    header_list.append("C1 Y2")
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)
    print(header_list)

if __name__ == "__main__":
 
    headers(test)
    main()
    footers(waveform_counter)
