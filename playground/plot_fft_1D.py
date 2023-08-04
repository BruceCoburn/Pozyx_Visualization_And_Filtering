# Import Python-native modules
import sys
from PyQt5.QtWidgets import QApplication

# Import custom modules
from pozyx_helpers.QtPlotFftMagnitudePhase import QtPlotFftMagnitudePhase

if __name__ == "__main__":
    """
    Launch a Qt application that plots the magnitude and phase of the FFT of a 1D signal.
    """
    app = QApplication(sys.argv)
    ex = QtPlotFftMagnitudePhase()
    sys.exit(app.exec_())
