import pandas as pd
import os
import openpyxl
from openpyxl.chart import ScatterChart, Reference, Series

def main():
    # prompt user for excel file path and display list of available files
    path = input("Please enter the path of the Excel file: ")
    files = [f for f in os.listdir(path) if f.endswith('.xlsx')]
    print("Available Excel files:")
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    # prompt user for which file to use
    while True:
        try:
            file_choice = int(input("Please choose a file (enter the number): "))
            if 1 <= file_choice <= len(files):
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    file_name = os.path.join(path, files[file_choice-1])

    # load the excel file and use the default active sheet
    df = pd.read_excel(file_name, header=1)

    # drop rows and columns with NaN or empty values
    df = df.dropna()  # remove rows and columns with NaN or empty values

    # get the headers of the dataframe and remove columns with 'Unnamed' in header name
    headers = [col for col in df.columns if 'Unnamed' not in col]

    # drop the 'Unnamed' columns from the dataframe
    df = df[headers]

    # create worksheet object
    wb = openpyxl.load_workbook(file_name)
    ws = wb.active

    # get the chart title
    chart_title = input("Please enter the chart title: ")

    print("Available columns for x-axis:")
    for i, h in enumerate(headers):
        print(f"{i+1}. {h}")

    while True:
        try:
            x_axis_choice = int(input("Please choose a column for the x-axis (enter the number): "))
            if 1 <= x_axis_choice <= len(headers):
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    x_axis_column = headers[x_axis_choice-1]

    # prompt user for y-axis column(s)
    print("Available columns for y-axis:")
    for i, h in enumerate(headers):
        if h != x_axis_column: # exclude the x-axis column from the options
            print(f"{i+1}. {h}")

    y_axis_columns = []
    while True:
        try:
            y_axis_choice = int(input("Please choose a column for the y-axis (enter the number): "))
            if 1 <= y_axis_choice <= len(headers):
                y_axis_column = headers[y_axis_choice-1]
                if y_axis_column == x_axis_column:
                    print("Invalid choice. The column is already chosen for the x-axis. Please choose another column.")
                else:
                    y_axis_columns.append(y_axis_column)
                    print(f"{y_axis_column} added to y-axis.")
                    choice = input("Do you want to add another y-axis column? (y/n): ")
                    if choice.lower() != "y":
                        break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    chart = ScatterChart()

    # add x-axis data
    x_data = Reference(ws, min_col=x_axis_choice, min_row=2, max_row=len(df)+1)
    x_series = Series(x_data, title=x_axis_column)
    chart.append(x_series)

    # add y-axis data
    for y_axis_column in y_axis_columns:
        y_axis_choice = headers.index(y_axis_column) + 1
        y_data = Reference(ws, min_col=y_axis_choice, min_row=2, max_row=len(df)+1)
        y_series = Series(y_data, title=y_axis_column)
        chart.append(y_series)

    # set chart title and axis labels
    chart.title = f"{x_axis_column} vs {', '.join(y_axis_columns)}"
    chart.x_axis.title = x_axis_column
    chart.y_axis.title = ", ".join(y_axis_columns)

    # insert the chart into the worksheet
    chart_cell = ws.cell(row=1, column=len(headers)+3)
    ws.add_chart(chart, chart_cell)

    # save the workbook
    wb.save(file_name)
    print("Chart added to the worksheet.")


main()