# Import Python-native modules
import sys
from PyQt5 import QtWidgets

# Import custom modules
from pozyx_helpers.PozyxPlot import QtChooseDoubleWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtChooseDoubleWindow()
    window.show()
    sys.exit(app.exec_())
