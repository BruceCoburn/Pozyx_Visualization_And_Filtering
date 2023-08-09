import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

class QtSinglePlotWindow(QtWidgets.QWidget):
    """
    A Qt window that plots data from a .csv file (input filename within the script).
    """

    def __init__(self):
        super().__init__()

        self.button_width = 150
        self.button_height = 40

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
        self.data_button = QtWidgets.QPushButton("Select Data CSV File")
        self.data_button.setFixedSize(self.button_width, self.button_height)
        self.data_button.clicked.connect(
            lambda: self.loadCsvFile(1)
        )  # Connect the button to a function

        self.ground_truth_button = QtWidgets.QPushButton("Select Ground Truth CSV File")
        self.ground_truth_button.setFixedSize(self.button_width, self.button_height)
        self.ground_truth_button.clicked.connect(
            lambda: self.loadCsvFile(2)
        )

        # Create a button to clear the plot
        self.clear_button = QtWidgets.QPushButton("Clear Plot")
        self.clear_button.setFixedSize(self.button_width, self.button_height)
        self.clear_button.clicked.connect(
            lambda: self.clearPlots()
        )

        # Create a button to save the plot
        self.save_button = QtWidgets.QPushButton("Save Plot")
        self.save_button.setFixedSize(self.button_width, self.button_height)
        self.save_button.clicked.connect(
            lambda: self.savePlot()
        )

        # Create a vertical box layout
        layout = QtWidgets.QVBoxLayout()

        """
        layout.addWidget(self.data_button)
        layout.addWidget(self.ground_truth_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.canvas)
        """
        topButtonLayout = QtWidgets.QHBoxLayout()
        topButtonLayout.addWidget(self.data_button)
        topButtonLayout.addWidget(self.ground_truth_button)

        bottomButtonLayout = QtWidgets.QHBoxLayout()
        bottomButtonLayout.addWidget(self.clear_button)
        bottomButtonLayout.addWidget(self.save_button)

        layout.addLayout(topButtonLayout)
        layout.addLayout(bottomButtonLayout)

        layout.addWidget(self.canvas)

        # Set the layout of the window
        self.setLayout(layout)

        # Add large and bold title
        self.ax.set_title("1-D Pozyx Data", fontsize=16, fontweight="bold")

        # Set the x and y labels
        self.ax.set_xlabel("Timesteps (ms)")
        self.ax.set_ylabel("Distance (mm)")

    def savePlot(self):
        """
        Saves the plot as a .png file.
        """
        options = QFileDialog.Options()

        # Open a file dialog to select a .csv file, filters for .csv files
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Plot", "", "PNG Files (*.png)", options=options
        )

        # Save the plot
        if filename:
            self.figure.savefig(filename)

    def clearPlots(self):
        """
        Clears the plots.
        """
        self.ax.clear()

        # Add large and bold title
        self.ax.set_title("1-D Pozyx Data", fontsize=16, fontweight="bold")

        # Set the x and y labels
        self.ax.set_xlabel("Timesteps (ms)")
        self.ax.set_ylabel("Distance (mm)")

        self.canvas.draw()

    def loadCsvFile(self, button_type):
        """
        Opens a file dialog to select a .csv file.
        """
        options = QFileDialog.Options()

        # Open a file dialog to select a .csv file, filters for .csv files
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)", options=options
        )

        # Plot the .csv file
        if filename and button_type == 1:
            self.plotDataCsvFile(filename)
        elif filename and button_type == 2:
            self.plotGroundTruthCsvFile(filename)

        # Add a legend
        self.ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize='large')




    def plotDataCsvFile(self, filename):
        """
        Plots the data from a .csv file.
        """
        df = pd.read_csv(filename)

        # Calculate the mean of the data
        data_mean = df[df.columns[1]].mean()

        # Calculate the data which deviates the most from the mean
        data_max_deviation = df[df.columns[1]].max() - data_mean
        data_min_deviation = data_mean - df[df.columns[1]].min()
        data_deviation_diff = max(data_max_deviation, data_min_deviation)

        print(f"Data mean: {data_mean:.2f}")
        print(f"Data max deviation: {data_max_deviation:.2f}")
        print(f"Data min deviation: {data_min_deviation:.2f}")
        print(f"Data deviation diff: {data_deviation_diff:.2f}")

        # Plot the mean and the max deviation lines
        self.ax.axhline(y=data_mean, color='green', label='Mean', linewidth=1)

        # Determine whether the max or min deviation is greater (used to plot line above or below the mean)
        if data_max_deviation < data_min_deviation:
            diff_line = data_mean - data_deviation_diff
        else:
            diff_line = data_mean + data_deviation_diff

        self.ax.axhline(y=diff_line, color='red', label='Max Deviation', linewidth=1)

        # Annotate the mean and max deviation lines
        self.ax.annotate(f'Mean: {data_mean:.2f}', xy=(1, data_mean), xycoords=('axes fraction', 'data'), textcoords='offset points', xytext=(-10,-10), ha='right')
        self.ax.annotate(f'Deviation Value: {diff_line:.2f} || Difference: {data_deviation_diff:.2f}', xy=(1, diff_line), xycoords=('axes fraction', 'data'), textcoords='offset points', xytext=(-10,10), ha='right')

        # Plot the data
        self.ax.plot(df[df.columns[0]], df[df.columns[1]], color='blue', label='Pozyx Data', linewidth=1)

        # Draw the plot
        self.canvas.draw()

    def plotGroundTruthCsvFile(self, filename):
        """
        Plots the data from a .csv file.
        """
        df = pd.read_csv(filename)

        # Calculate the mean of GT
        gt_mean = df[df.columns[1]].mean()

        # Plot the mean line
        self.ax.axhline(y=gt_mean, color='purple', label='GT Mean', linewidth=1)

        # Annotate the mean line
        self.ax.annotate(f'GT Mean: {gt_mean:.2f}', xy=(1, gt_mean), xycoords=('axes fraction', 'data'), textcoords='offset points', xytext=(-10,-10), ha='right')

        # Plot the data
        self.ax.plot(df[df.columns[0]], df[df.columns[1]], color='orange', label='Ground Truth', linewidth=3)

        # Draw the plot
        self.canvas.draw()