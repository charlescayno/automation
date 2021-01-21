import xlsxwriter


def write_date(row, column):
    worksheet.write(row, column, "Date")


def write_start(row, column):
    worksheet.write(row, column, "Start")


def write_end(row, column):
    worksheet.write(row, column, "Finish")


def write_efficiency(row, column):
    worksheet.write(row, column, "Efficiency")


def write_input(row, column):
    worksheet.merge_range(row, column, row, column + 1, "Input", centered)
    worksheet.write_row(row + 1, column, ["Vac (rms)", "Freq (Hz)"])


def write_input_measurement(row, column):
    worksheet.merge_range(row, column, row, column + 4, "Input Measurement", centered)
    worksheet.write_row(
        row + 1, column, ["Vin (rms)", "Iin (mA)", "Pin (W)", "PF", "% THD"],
    )


def write_output_measurement(row, column, number=""):
    worksheet.merge_range(
        row, column, row, column + 3, f"Output {number} Measurement", centered
    )
    worksheet.write_row(
        row + 1, column, ["Vo (V)", "Io (mA)", "Po (W)", "%V Reg"],
    )


def write_headers(num_output=1):
    write_date(0, 4)
    write_start(1, 4)
    write_end(2, 4)
    write_input(3, 4)
    write_input_measurement(3, 6)
    col = 11
    for i in range(num_output):
        if num_output > 1:
            write_output_measurement(3, col, i + 1)
        else:
            write_output_measurement(3, col)
        col += 4
    write_efficiency(4, col)


workbook = xlsxwriter.Workbook("Expenses01.xlsx")
worksheet = workbook.add_worksheet()

centered = workbook.add_format({"align": "center", "valign": "center"})

write_headers(1)

workbook.close()
