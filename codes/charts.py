import xlsxwriter
import os

def exists(filename):
    return os.path.isfile(filename)

if exists("Charts.xlsx"):
    print("chart already exist")

efficiency = [80, 80.5, 81, 81.5, 82, 82.5, 83, 82.5, 80, 75]
voltages = [90, 100, 115, 130, 150, 180, 200, 230, 240, 265]

workbook = xlsxwriter.Workbook("Charts.xlsx")
worksheet = workbook.add_worksheet()

worksheet.write_column("F4", voltages)
worksheet.write_column("G4", efficiency)

chart = workbook.add_chart({"type": "line"})

workbook.close()
