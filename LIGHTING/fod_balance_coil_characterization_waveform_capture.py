from misc_codes.scope_setter import scope_settings
from misc_codes.scope_settings_fod import SCOPE_CONFIG
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [120]
unit = 1
channel_list = [1,2,3,4]

vout = 24
iout = 2.7

# PROJECT DETAILS
project = "DER-999"
test = f"FOD Balance Coil (Clover Config) Rf_30k"
FO_list = ['Paper Clip (Parallel)','Paper Clip (Perp)', '1x0.67x10mils Cu (Parallel)', '1x0.67x10mils Cu (Perp)', 'Coin']
condition_list = ['-X 0Y', '+X 0Y', '0x +Y', '0X -Y', '0X 0Y']

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################
def main():

    for FO in FO_list:
        excel_name = f"{FO}"
        create_header_for_df()
        EQUIPMENT_FUNCTIONS().AC_TURN_OFF()
        for vin in vin_list:
            
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            soak(10)

            for condition in condition_list:

                fod_test(excel_name, vin, condition, foreign_object=FO, type='No FO')
                fod_test(excel_name, vin, condition, foreign_object=FO, type=FO)
                
        GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
        EQUIPMENT_FUNCTIONS().AC_TURN_OFF()
        input(">> Press ENTER to continue to the next FO...")


def fod_test(excel_name, vin, condition, foreign_object, type='No FO'):
    """
        condition: No FO or FO orientation on XY axis
        foreign_object: foreign object used for the test
        type: user-define whether to get No FO condition or not
    """

    scope.run()
    
    if type == 'No FO':
        input(f">> No FO at {condition}. Press ENTER to continue...")
        filename = f"{condition} - No FO"
        
    else:
        input(f">>{foreign_object} at {condition}. Press ENTER to continue...")
        filename = f"{condition} - {foreign_object}"
    
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
    scope_settings(SCOPE_CONFIG)
    main()
    footers(waveform_counter)
