# Import Python-native modules
import sys
from PyQt5 import QtWidgets

# Import custom modules
from pozyx_helpers.PozyxPlot import QtDoubleWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtDoubleWindow()
    window.show()
    sys.exit(app.exec_())