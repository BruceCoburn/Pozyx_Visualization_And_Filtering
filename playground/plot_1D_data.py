# Import Python-native modules
import sys
from PyQt5 import QtWidgets

# Import custom modules
from pozyx_helpers.PozyxPlot import QtSinglePlotWindow


if __name__ == "__main__":
    # Create a Qt application
    app = QtWidgets.QApplication(sys.argv)
    window = (
        QtSinglePlotWindow()
    )  # QtSinglePlotWindow() will plot the data from a .csv file

    # Show the Qt application
    window.show()

    # On exit, close the Qt application
    sys.exit(app.exec_())
