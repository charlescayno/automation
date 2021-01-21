import xlsxwriter

efficiency = [80, 80.5, 81, 81.5, 82, 82.5, 83, 82.5, 80, 75]
voltages = [90, 100, 115, 130, 150, 180, 200, 230, 240, 265]

workbook = xlsxwriter.Workbook("Charts.xlsx")
worksheet = workbook.add_worksheet()

worksheet.write_column("A1", voltages)
worksheet.write_column("B1", efficiency)

chart = workbook.add_chart({"type": "line"})

workbook.close()
