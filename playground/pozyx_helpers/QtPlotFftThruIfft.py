# Import Python-native modules
import os
import numpy as np
from scipy.fftpack import fft
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QLabel,
    QHBoxLayout,
    QTabWidget,
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Import custom modules
# from .supplemental_functions import create_two_figs_in_tab


class QtPlotFftThruIfft(QMainWindow):
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
        
        # Create tab0 - raw data and PSD
        tab0 = QWidget()
        tab0Layout = QHBoxLayout()
        self.createPlots(tab0Layout, 0)
        tab0.setLayout(tab0Layout)
        self.tabs.addTab(tab0, "Raw Data and PSD")

        # Create tab1 - magnitude, phase w/ DC component
        tab1 = QWidget()
        tab1Layout = QHBoxLayout()
        self.createPlots(tab1Layout, 1)
        tab1.setLayout(tab1Layout)
        self.tabs.addTab(tab1, "With DC Offset")

        # Create tab2 - magnitude, phase w/o DC component
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
        ax = self.canvas_raw_data_tab0.figure.subplots()
        ax.set_title("Raw Pozyx Data")
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Distance (mm)")
        ax.plot(timesteps, data[:, 1])
        self.canvas_raw_data_tab0.draw()

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
            frequencies[:positive_freq_components],
            magnitudes_w_dc[:positive_freq_components],
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
            frequencies[:positive_freq_components],
            phase_w_dc[:positive_freq_components],
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
            frequencies[:positive_freq_components],
            phase_wo_dc[:positive_freq_components],
        )
        ax.set_title("Phase Spectrum w/o DC Offset")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Phase (radians)")
        self.canvas_phase_tab2.draw()

        ########################################
        # Compute the Power Spectral Density (PSD)
        ########################################
        # The PSD is the square of the magnitude spectrum
        psd_wo_dc = np.square(magnitudes_wo_dc)

        # Plot the PSD
        ax = self.canvas_PSD_tab0.figure.subplots()
        ax.plot(
            frequencies[:positive_freq_components],
            psd_wo_dc[:positive_freq_components],
        )
        ax.set_title("Power Spectral Density (w/o DC Offset)")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("PSD")
        self.canvas_PSD_tab0.draw()

        ################################################################
        # Find the maximum magnitude and the corresponding frequency
        ################################################################
        max_magnitude_w_dc = np.max(magnitudes_w_dc[:positive_freq_components])
        max_magnitude_wo_dc = np.max(magnitudes_wo_dc[:positive_freq_components])
        max_magnitude_index_w_dc = np.argmax(magnitudes_w_dc[:positive_freq_components])
        max_magnitude_index_wo_dc = np.argmax(
            magnitudes_wo_dc[:positive_freq_components]
        )

        print(f"max_magnitude_index_w_dc: {max_magnitude_index_w_dc}")
        print(f"max_magnitude_index_wo_dc: {max_magnitude_index_wo_dc}")

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
        L = np.arange(
            1, np.floor(n / 2), dtype="int"
        )  # Only plot the first half of freqs
        return PSD

    def createPlots(self, layout, tabNumber):

        figure_plot0 = Figure()
        canvas_plot0 = FigureCanvas(figure_plot0)
        layout.addWidget(canvas_plot0)

        figure_plot1= Figure()
        canvas_plot1 = FigureCanvas(figure_plot1)
        layout.addWidget(canvas_plot1)

        # Store the canvases and figures
        if tabNumber == 0:
            self.canvas_raw_data_tab0 = canvas_plot0
            self.canvas_PSD_tab0 = canvas_plot1
        elif tabNumber == 1:
            self.canvas_magnitude_tab1 = canvas_plot0
            self.canvas_phase_tab1 = canvas_plot1
        elif tabNumber == 2:
            self.canvas_magnitude_tab2 = canvas_plot0
            self.canvas_phase_tab2 = canvas_plot1
        else:
            raise ValueError("Invalid tab number")
