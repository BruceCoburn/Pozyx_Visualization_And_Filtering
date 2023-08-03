import csv
import matplotlib.pyplot as plt

import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QFileDialog


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


class QtPlotWindow(QtWidgets.QWidget):
    """
    A Qt window that plots data from a .csv file.
    """
    def __init__(self):
        super().__init__()

        self.initUI() # Initialize the UI

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
        self.button.clicked.connect(self.loadCsvFile) # Connect the button to a function

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
