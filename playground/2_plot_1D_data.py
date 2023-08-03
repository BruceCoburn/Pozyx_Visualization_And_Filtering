# Import Python-native modules
import sys
from PyQt5 import QtWidgets

# Import custom modules
from pozyx_helpers.PozyxPlot import plot_csv_data
from pozyx_helpers.PozyxPlot import QtPlotWindow



if __name__ == "__main__":
    """
    csv_file_path = (
        "pozyx_ranging_runs/data_2023-08-03_12-33-23_PRECISION.csv"
    )
    plot_csv_data(csv_file_path)
    """
    app = QtWidgets.QApplication(sys.argv)
    window = QtPlotWindow()
    window.show()
    sys.exit(app.exec_())
