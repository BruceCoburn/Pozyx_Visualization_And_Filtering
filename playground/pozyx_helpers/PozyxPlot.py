# Import Python-native modules
import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QLabel,
    QHBoxLayout,
    QGridLayout,
    QSizePolicy,
    QTabWidget,
)


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
    plt.show()


class QtSinglePlotWindow(QtWidgets.QWidget):
    """
    A Qt window that plots data from a .csv file (input filename within the script).
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


class QtChooseDoubleWindow(QtWidgets.QWidget):
    def __init__(self):
        """
        A Qt window that plots data from two .csv files (prefereably unfiltered and filtered data).
        """
        super().__init__()

        # Set fixed button width and height
        self.button_width = 150
        self.button_height = 40

        # Initialize the plot index dictionary (used for naming subplots)
        self.plot_index_dict = {0: "Unfiltered", 1: "Filtered"}

        # Initialize the UI
        self.initUI()

    def initUI(self):
        """
        Initializes the UI of the Qt window.
        """
        self.figure, self.ax = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvas(self.figure)

        # Create two buttons to select .csv files

        # First csv file
        self.button1 = QtWidgets.QPushButton("Select CSV File 1")
        self.button1.clicked.connect(lambda: self.loadCsvFile(0))
        self.button1.setFixedSize(self.button_width, self.button_height)

        # Second csv file
        self.button2 = QtWidgets.QPushButton("Select CSV File 2")
        self.button2.clicked.connect(lambda: self.loadCsvFile(1))
        self.button2.setFixedSize(self.button_width, self.button_height)

        # Create a title label (custom font)
        title_label = QtWidgets.QLabel("Pozyx Unfiltered / Filtered Data")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignCenter)

        # Create a button layout (side-by-side)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)

        # Layout our window widgets: title, buttons, and plot
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(button_layout)
        layout.addWidget(self.canvas)

        # Stretch factors for the layout during resizing
        layout.setStretch(0, 1)  # Title stretch factor
        layout.setStretch(1, 1)  # Button layout stretch factor
        layout.setStretch(2, 8)  # Plot stretch factor

        # Set the layout and title of the window
        self.setLayout(layout)
        self.setWindowTitle("Pozyx Unfiltered/Filtered 1-D Data")

    def loadCsvFile(self, plot_index):
        """
        Opens a file dialog to select a .csv file.
        """
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)", options=options
        )

        # Plot the .csv file
        if filename:
            self.plotData(filename, plot_index)

    def plotData(self, filename, plot_index):
        """
        Plots the data from a .csv file.
        """

        # Read the .csv file and plot the data
        df = pd.read_csv(filename)
        self.ax[plot_index].clear()
        self.ax[plot_index].plot(df[df.columns[0]], df[df.columns[1]])
        self.ax[plot_index].set_title(
            f"1-D Pozyx {self.plot_index_dict[plot_index]} Data"
        )
        self.canvas.draw()


class QtPlotFftMagnitudePhase(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_width = 150
        self.button_height = 40

        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        ########################################
        # Title label
        ########################################
        titleLabel = QLabel("FFT Magnitude and Phase")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        titleLabel.setFont(font)
        titleLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(titleLabel)
        self.titleLabel = titleLabel

        ########################################
        # Load CSV button and label
        ########################################
        # Button to load CSV file
        loadCsvLayout = QHBoxLayout()
        loadCsvLayout.addStretch(
            1
        )  # Add stretchable space before button and label to center it

        self.label_max_magnitude = QLabel("Max Magnitude: \tMax Magnitude Frequency: ")
        loadCsvLayout.addWidget(self.label_max_magnitude)

        btnLoadCSV = QPushButton("Load CSV")
        btnLoadCSV.setFixedSize(self.button_width, self.button_height)
        btnLoadCSV.clicked.connect(self.loadCSV)
        loadCsvLayout.addWidget(btnLoadCSV)

        # Label to display the loaded CSV file
        self.filenameLabel = QLabel("No CSV file loaded")
        loadCsvLayout.addWidget(self.filenameLabel)

        loadCsvLayout.addStretch(
            1
        )  # Add stretchable space after button and label to center it

        mainLayout.addLayout(loadCsvLayout)

        # Create tab widget
        self.tabs = QTabWidget()
        mainLayout.addWidget(self.tabs)

        # Create tab1 - raw data, magnitude, phase w/ DC component
        tab1 = QWidget()
        tab1Layout = QHBoxLayout()
        self.createPlots(tab1Layout, 1)
        tab1.setLayout(tab1Layout)
        self.tabs.addTab(tab1, "With DC Offset")

        # Create tab2 - raw data, magnitude, phase w/o DC component
        tab2 = QWidget()
        tab2Layout = QHBoxLayout()
        self.createPlots(tab2Layout, 2)
        tab2.setLayout(tab2Layout)
        self.tabs.addTab(tab2, "Without DC Offset")

        # Add tabs to tab widget
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

        # Set stretch factors
        mainLayout.setStretch(0, 1)  # Stretch factor for title
        mainLayout.setStretch(1, 1)  # Stretch factor for button
        mainLayout.setStretch(2, 8)  # Stretch factor for plots

        self.show()

    def loadCSV(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)", options=options
        )
        if filepath:
            filename = os.path.basename(filepath)  # Extract filename from filepath
            self.filenameLabel.setText(filename)  # Set the filename label
            self.plotFFT(filepath)


    def plotFFT(self, filePath):
        # Load the data from the CSV file
        data = np.genfromtxt(filePath, delimiter=",", skip_header=1)
        timesteps = data[:, 0]

        # Define the frequencies
        frequencies = np.fft.fftfreq(len(timesteps), np.diff(timesteps)[0])

        # When performing FFT on real-valued input, the output is symmetric about the zero frequency
        # Therefore, we only need to plot the positive frequencies
        positive_freq_components = len(frequencies) // 2

        ########################################
        # Plot the raw data
        ########################################
        ax = self.canvas_raw_data_tab1.figure.subplots()
        ax.set_title("Raw Pozyx Data")
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Distance (mm)")
        ax.plot(timesteps, data[:, 1])
        self.canvas_raw_data_tab1.draw()
        ax = self.canvas_raw_data_tab2.figure.subplots()
        ax.set_title("Raw Pozyx Data")
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Distance (mm)")
        ax.plot(timesteps, data[:, 1])
        self.canvas_raw_data_tab2.draw()

        ########################################
        # Plot the Magnitude w/ DC Offset
        ########################################
        distances_w_dc = data[:, 1]
        
        # Perform the FFT using SciPy FFT
        transformed_w_dc = fft(distances_w_dc)

        # We normalize the magnitudes by dividing by the number of samples
        # This is because the magnitude is proportional to the number of samples
        magnitudes_w_dc = np.abs(transformed_w_dc) / len(distances_w_dc)
        phase_w_dc = np.angle(transformed_w_dc)

        # Plot the normalized magnitude
        ax = self.canvas_magnitude_tab1.figure.subplots()
        ax.plot(
            frequencies[:positive_freq_components], magnitudes_w_dc[:positive_freq_components]
        )
        ax.set_title("Magnitude w/ DC Offset")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        self.canvas_magnitude_tab1.draw()

        ########################################
        # Plot the Phase w/ DC Offset
        ########################################
        ax = self.canvas_phase_tab1.figure.subplots()
        ax.plot(
            frequencies[:positive_freq_components], phase_w_dc[:positive_freq_components]
        )
        ax.set_title("Phase w/ DC Offset")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Phase (radians)")
        self.canvas_phase_tab1.draw()

        ########################################
        # Plot the Magnitude w/o DC Offset
        ########################################
        # Since there is a significant DC offset, we need to remove it by subtracting the mean
        distances_wo_dc = data[:, 1] - np.mean(data[:, 1])

        # Perform the FFT using SciPy FFT
        transformed_wo_dc = fft(distances_wo_dc)

        # We normalize the magnitudes by dividing by the number of samples
        # This is because the magnitude is proportional to the number of samples
        magnitudes_wo_dc = np.abs(transformed_wo_dc) / len(distances_wo_dc)
        phase_wo_dc = np.angle(transformed_wo_dc)

        # Plot the normalized magnitude
        ax = self.canvas_magnitude_tab2.figure.subplots()
        ax.plot(
            frequencies[:positive_freq_components],
            magnitudes_wo_dc[:positive_freq_components],
        )
        ax.set_title("Magnitude Spectrum w/o DC Offset")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        self.canvas_magnitude_tab2.draw()

        ########################################
        # Plot the Phase w/o DC Offset
        ########################################
        ax = self.canvas_phase_tab2.figure.subplots()
        ax.plot(
            frequencies[:positive_freq_components], phase_wo_dc[:positive_freq_components]
        )
        ax.set_title("Phase Spectrum w/o DC Offset")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Phase (radians)")
        self.canvas_phase_tab2.draw()

        ################################################################
        # Find the maximum magnitude and the corresponding frequency
        ################################################################
        max_magnitude_w_dc = np.max(magnitudes_w_dc[:positive_freq_components])
        max_magnitude_wo_dc = np.max(magnitudes_wo_dc[:positive_freq_components])
        max_magnitude_index_w_dc = np.argmax(magnitudes_w_dc[:positive_freq_components])
        max_magnitude_index_wo_dc = np.argmax(magnitudes_wo_dc[:positive_freq_components])

        print(f'max_magnitude_index_w_dc: {max_magnitude_index_w_dc}')
        print(f'max_magnitude_index_wo_dc: {max_magnitude_index_wo_dc}')

        """
        # This code block is leading to the code freezing up for some reason...
        # Check that the maximum magnitude indices match
        print(f'checking that the maximum magnitude indices match...')
        if max_magnitude_index_w_dc != max_magnitude_index_wo_dc:
            raise ValueError("The maximum magnitude indices do not match between data with and without DC offset!")
        """

        # Get the corresponding frequency
        max_magnitude_freq = frequencies[max_magnitude_index_wo_dc]

        # Update the label
        self.label_max_magnitude.setText(
            f"Max Magnitude (w/o DC): {max_magnitude_wo_dc:.2f}\n"
            + f"Max Magnitude (w DC): {max_magnitude_w_dc:.2f}\n"
            + f"Frequency: {max_magnitude_freq:.2f} Hz"
        )

    def computeFFT(self, timesteps, data):
        """
        Compute the FFT using numpy of the data and return the magnitudes, phases, and PSD
        """
        n = len(timesteps)  # Number of samples
        dt = np.diff(timesteps)[0]  # Time step size
        fhat = np.fft.fft(data, n)  # Compute the FFT
        PSD = fhat * np.conj(fhat) / n  # Power spectrum (power per freq)
        freq = (1 / (dt * n)) * np.arange(n)  # Create x-axis of frequencies in Hz
        L = np.arange(1, np.floor(n / 2), dtype="int")  # Only plot the first half of freqs
        return PSD, freq, L

    def createPlots(self, layout, tabNumber):
        figure_raw_data = Figure()
        canvas_raw_data = FigureCanvas(figure_raw_data)
        layout.addWidget(canvas_raw_data)

        figure_magnitude = Figure()
        canvas_magnitude = FigureCanvas(figure_magnitude)
        layout.addWidget(canvas_magnitude)

        figure_phase = Figure()
        canvas_phase = FigureCanvas(figure_phase)
        layout.addWidget(canvas_phase)

        # Store the canvases and figures
        if tabNumber == 1:
            self.canvas_raw_data_tab1 = canvas_raw_data
            self.canvas_magnitude_tab1 = canvas_magnitude
            self.canvas_phase_tab1 = canvas_phase
        elif tabNumber == 2:
            self.canvas_raw_data_tab2 = canvas_raw_data
            self.canvas_magnitude_tab2 = canvas_magnitude
            self.canvas_phase_tab2 = canvas_phase



