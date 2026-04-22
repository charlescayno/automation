from openpyxl import Workbook
from openpyxl.chart import ScatterChart, Reference, Series

# Create a new workbook and select the active worksheet
wb = Workbook()
ws = wb.active

# Add sample data to the worksheet
ws.append(['x', 'y'])
ws.append([1, 2])
ws.append([2, 4])
ws.append([3, 6])
ws.append([4, 8])
ws.append([5, 10])

# Create a scatter chart
chart = ScatterChart()
chart.title = "Scatter Chart"

# Add data to the chart
xdata = Reference(ws, min_col=1, min_row=2, max_row=6)
ydata = Reference(ws, min_col=2, min_row=2, max_row=6)
series = Series(ydata, xdata)
chart.series.append(series)

# Add the chart to the worksheet
ws.add_chart(chart, "A7")

# Save the workbook
wb.save("scatter_chart.xlsx")
