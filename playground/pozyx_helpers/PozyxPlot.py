# Import Python-native modules
import csv
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


def plot_csv_data(csv_file):
    """
    Plots the data from a .csv file using a Matplotlib popup window.
    """

    x_data = []
    y_data = []

    # Read data from csv file
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip the header row

        for row in reader:
            try:
                x_value = float(row[0])  # First column (x-axis)
                y_value = float(row[1])  # Second column (y-axis)
                x_data.append(x_value)
                y_data.append(y_value)
            except ValueError:
                print(f"Invalid row data: {row}")

    # Plot data
    plt.plot(x_data, y_data, marker="o")
    plt.xlabel(headers[0])  # x-axis label from the header
    plt.ylabel(headers[1])  # y-axis label from the header
    plt.title(f"1-D Pozyx Data")
    plt.grid(True)
    plt.show()


class QtSinglePlotWindow(QtWidgets.QWidget):
    """
    A Qt window that plots data from a .csv file.
    """

    def __init__(self):
        super().__init__()

        self.initUI()  # Initialize the UI

    def initUI(self):
        """
        Initializes the UI of the Qt window.
        """

        # Set window title
        self.setWindowTitle("Pozyx 1-D Plotter")

        # Create a figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # Create a button to select a .csv file
        self.button = QtWidgets.QPushButton("Select CSV File")
        self.button.clicked.connect(
            self.loadCsvFile
        )  # Connect the button to a function

        # Create a vertical box layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.canvas)

        # Set the layout of the window
        self.setLayout(layout)

    def loadCsvFile(self):
        """
        Opens a file dialog to select a .csv file.
        """
        options = QFileDialog.Options()

        # Open a file dialog to select a .csv file, filters for .csv files
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)", options=options
        )

        # Plot the .csv file
        if filename:
            self.plotCsvFile(filename)

    def plotCsvFile(self, filename):
        """
        Plots the data from a .csv file.
        """
        df = pd.read_csv(filename)
        self.ax.clear()
        self.ax.plot(df[df.columns[0]], df[df.columns[1]])
        self.ax.set_title("1-D Pozyx Data")
        self.canvas.draw()


class QtDoubleWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button_width = 150
        self.button_height = 40

        self.initUI()

        self.plot_index_dict = {0: "Unfiltered", 1: "Filtered"}

    def initUI(self):
        self.figure, self.ax = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvas(self.figure)

        self.button1 = QtWidgets.QPushButton("Select CSV File 1")
        self.button1.clicked.connect(lambda: self.loadCsvFile(0))
        self.button1.setFixedSize(self.button_width, self.button_height)

        self.button2 = QtWidgets.QPushButton("Select CSV File 2")
        self.button2.clicked.connect(lambda: self.loadCsvFile(1))
        self.button2.setFixedSize(self.button_width, self.button_height)

        title_label = QtWidgets.QLabel("Pozyx Unfiltered / Filtered Data")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignCenter)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(button_layout)
        layout.addWidget(self.canvas)

        layout.setStretch(0, 1) # Title stretch factor
        layout.setStretch(1, 1) # Button layout stretch factor
        layout.setStretch(2, 8) # Plot stretch factor

        self.setLayout(layout)
        self.setWindowTitle("Pozyx Unfiltered/Filtered 1-D Data")

    def loadCsvFile(self, plot_index):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)", options=options
        )

        if filename:
            self.plotData(filename, plot_index)

    def plotData(self, filename, plot_index):
        df = pd.read_csv(filename)
        self.ax[plot_index].clear()
        self.ax[plot_index].plot(df[df.columns[0]], df[df.columns[1]])
        self.ax[plot_index].set_title(
            f"1-D Pozyx {self.plot_index_dict[plot_index]} Data"
        )
        self.canvas.draw()
