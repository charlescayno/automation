from powi1.data_manager import *
import pandas as pd

def export_raw_df_to_another_excel(unit, input_folder, output_foler, input_filename, output_filename, sheet_name):

    # adjusting path folders
    input_path = path_maker(f'{input_folder}')
    output_path = input_path + output_filename    
    input_file = input_folder + input_filename

    # reading dataframe from excel raw file
    df = pd.read_excel(input_file, sheet_name)
    df = clean_dataframe(df)

    # exporting dataframe to a final excel file
    export_df_to_excel(df, input_folder, output_filename, sheet_name, anchor="B2")


unit_list = [6, 7] # enter unit list to compilse here
sheet_name_list = ["Analog Dimming", "DALI"] # enter the sheetname here


for unit in unit_list:
    for sheet_name in sheet_name_list: 
        
        input_folder = f"C:/Users/{username}/Documents/Charles/Work/DER/DER-727/Marketing Samples/1103/{unit}/"
        output_folder = f"C:/Users/{username}/Documents/Charles/Work/DER/DER-727/Marketing Samples/1103/"

        input_filename = f"{sheet_name}_{unit}.xlsx"
        output_filename = f"DER727_UNIT_{unit}.xlsx"
        export_raw_df_to_another_excel(unit, input_folder, output_folder, input_filename, output_filename, sheet_name)