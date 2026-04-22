from powi1.data_manager import *
import pandas as pd
import math

## USER INPUT
input_folder = "C:\\Users\\ccayno\\Desktop\\Compiler\\Data\\" # enter folder path here where raw data is located
output_folder = "C:\\Users\\ccayno\\Desktop\\Compiler\\" # enter folder path here where final output will be located
file_name_list = ["Analog", "Eff"] #
output_filename = f"AAA.xlsx"

def main():

    for file_name in file_name_list:

        filename = f"{file_name}.xlsx"
        input_filename = filename
        
        # adjusting path folders
        input_path = path_maker(f'{input_folder}')
        output_path = input_path + output_filename    
        input_file = input_folder + input_filename

        # determining no of sheets and list of sheet names
        a = get_number_of_sheets(input_folder, input_filename)
        sheet_name_list = get_sheet_names(input_folder, input_filename)

        # creating dictionary of dataframe to access 1 sheet_name = 1 df
        df = {}
        start_anchor = "B2"
        for sheet_name in sheet_name_list:
            df_raw = pd.read_excel(input_file, sheet_name) # reading dataframe from excel raw file
            df_raw = clean_dataframe(df_raw) # clean up NaN values    
            df[sheet_name] = df_raw # adding dataframe to dictonary of dataframe
            df1 = df[sheet_name]
            export_df_to_excel(df1, input_folder, output_filename, file_name, anchor=start_anchor) # exporting dataframe to new excel
            start_anchor = change_anchor(start_anchor, row_increment=0, col_increment=get_df_col_len(df1)+1) # changing anchor for next set of dataframe


        # adding chart to the dataframe
        wb = load_workbook(output_path)

        chart_sheet = reset_chartsheet(wb)

        chart_title = "Power Factor"
        chart_x_axis_title = "Dim (V)"
        chart_y_axis_title = "PF"

        x_axis_label = "Dim"
        y_axis_label = "PF"

        worksheet_name = file_name
        
        # x-axis settings
        chart_x_axis_min_value = df1[x_axis_label].min()
        chart_x_axis_max_value = df1[x_axis_label].max()
        chart_x_axis_major_unit = math.floor((chart_x_axis_max_value-chart_x_axis_min_value)/10)
        chart_x_axis_minor_unit = chart_x_axis_major_unit
        # y-axis settings
        chart_y_axis_min_value = df1[y_axis_label].min()
        chart_y_axis_max_value = df1[y_axis_label].max()
        chart_y_axis_major_unit = 0.1
        chart_y_axis_minor_unit = chart_y_axis_major_unit

        chart = create_scatter_chart(title=chart_title, style=2, x_title=chart_x_axis_title, y_title=chart_y_axis_title,
                                x_min_scale = chart_x_axis_min_value, x_max_scale = chart_x_axis_max_value,
                                x_major_unit = chart_x_axis_major_unit, x_minor_unit = chart_x_axis_minor_unit,
                                y_min_scale = chart_y_axis_min_value, y_max_scale = chart_y_axis_max_value,
                                y_major_unit = chart_y_axis_major_unit, y_minor_unit = chart_y_axis_minor_unit)

        # adding each dataframe to the chart
        start_anchor = "B2"
        for sheet_name in sheet_name_list:
            series_title = sheet_name
            append_df_to_series(path = output_path,
                                wb = wb,
                                ws_name = worksheet_name,
                                anchor = start_anchor,
                                x_axis_label = x_axis_label,
                                y_axis_label = y_axis_label,
                                df = df1,
                                series_title=series_title,
                                chart=chart)
            start_anchor = change_anchor(start_anchor, row_increment=0, col_increment=get_df_col_len(df1)+1) # changing anchor for next set of dataframe
        
        save_chartsheet(chart_sheet, chart, chart_position="B2")
        wb.save(output_path)




if __name__ == "__main__":
    main()