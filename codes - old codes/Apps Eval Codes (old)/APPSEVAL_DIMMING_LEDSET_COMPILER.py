import pandas as pd
from openpyxl import Workbook, load_workbook

data = pd.read_csv('24V, 120Vac, RSET Dimming.txt', sep=",", header=None)
data.columns = ["RSET", "VAC", "FREQ", "VIN", "IIN", "PIN", "PF", "THD", "V01", "I01", "P01", "IREG1", "EFF"]

print(data["I01"])