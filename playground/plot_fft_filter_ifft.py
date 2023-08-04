import sys
from pozyx_helpers.QtPlotFftThruIfft import QtPlotFftThruIfft
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = QtPlotFftThruIfft()
    sys.exit(app.exec_())
