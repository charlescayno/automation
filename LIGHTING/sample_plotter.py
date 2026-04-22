import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


class DataFrameGrapher(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DataFrame Grapher")
        self.resize(800, 600)

        # Create a layout for the main window
        layout = QtGui.QVBoxLayout(self)

        # Create a PlotWidget
        self.plot = pg.PlotWidget()
        layout.addWidget(self.plot)

        # Create a DataFrame
        self.df = self.generate_initial_dataframe()

        # Start the main loop
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_dataframe)
        self.timer.start(1000)  # Update every second

    def generate_initial_dataframe(self):
        # Generate a random initial dataframe for demonstration
        data = np.random.rand(10, 2)
        df = pg.DataFrame(data, columns=['Column 1', 'Column 2'])
        return df

    def update_dataframe(self):
        # Simulate updating the dataframe with new data
        new_data = np.random.rand(10, 2)
        self.df.setData(new_data)

        # Clear the plot and replot the updated dataframe
        self.plot.clear()
        self.plot.addLegend()
        self.plot.plot(self.df['Column 1'], pen='b', name='Column 1')
        self.plot.plot(self.df['Column 2'], pen='r', name='Column 2')


# Start the application
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    grapher = DataFrameGrapher()
    grapher.show()
    sys.exit(app.exec_())
