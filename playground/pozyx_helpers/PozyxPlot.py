import csv
import matplotlib.pyplot as plt

import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QFileDialog

def plot_csv_data(csv_file):
    x_data = []
    y_data = []

    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip the header row

        for row in reader:
            try:
                x_value = float(row[0])  # Second column (x-axis)
                y_value = float(row[1])  # First column (y-axis)
                x_data.append(x_value)
                y_data.append(y_value)
            except ValueError:
                print(f"Invalid row data: {row}")

    plt.plot(x_data, y_data, marker="o")
    plt.xlabel(headers[0])  # x-axis label from the header
    plt.ylabel(headers[1])  # y-axis label from the header
    plt.title(f"1-D Pozyx Data")
    plt.grid(True)
    plt.show()

class QtPlotWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setWindowTitle('Pozyx 1-D Plotter')

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.button = QtWidgets.QPushButton('Select CSV File')
        self.button.clicked.connect(self.loadCsvFile)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def loadCsvFile(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)', options=options)

        if filename:
            self.plotCsvFile(filename)

    def plotCsvFile(self, filename):
        df = pd.read_csv(filename)
        self.ax.clear()
        self.ax.plot(df[df.columns[0]], df[df.columns[1]])
        self.ax.set_title('1-D Pozyx Data')
        self.canvas.draw()
