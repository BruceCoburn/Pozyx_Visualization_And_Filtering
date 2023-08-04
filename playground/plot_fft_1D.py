import sys
from pozyx_helpers.PozyxPlot import QtPlotFftMagnitudePhase
from pozyx_helpers.qt_style_sheet import set_dark_mode
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(set_dark_mode)
    ex = QtPlotFftMagnitudePhase()
    sys.exit(app.exec_())
