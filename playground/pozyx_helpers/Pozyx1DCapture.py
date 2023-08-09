# Import Python-native modules
import datetime
import os
import csv

# Import Pozyx-specific modules
from pypozyx import (
    PozyxConstants,
    version,
    SingleRegister,
    DeviceRange,
    POZYX_SUCCESS,
)

# Import custom modules
from .supplemental_functions import nice_print


class Pozyx1DCapture(object):
    """
    Continuously performs ranging between the Pozyx and a destination
    """

    def __init__(self,
                 pozyx,
                 destination_id,
                 protocol=PozyxConstants.RANGE_PROTOCOL_PRECISION,
                 remote_id=None,
                 data_dir='pozyx_ranging_runs/',
                 error_dir='pozyx_error_runs/',
    ):

        self.pozyx = pozyx      # Attach a PozyxSerial object to the Pozyx1DCapture object
        self.destination_id = destination_id        # ID of the Pozyx anchor
        self.protocol = protocol        # Pozyx ranging protocol (PRECISION or FAST)
        self.remote_id = remote_id      # ID of the Pozyx tag

        self.precision_dict = {0: '_PRECISION',
                               1: '_FAST',} # Dictionary to convert protocol to string (for file naming)
        self.protocol_name = self.precision_dict[protocol] # String to append to file names

        self.data_dir = data_dir    # Directory to save data files
        self.error_dir = error_dir  # Directory to save error files

        self.original_timestamp = 0
        self.run_timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') # Timestamp for file naming

        self.datafile = self.data_dir + 'data_' + self.run_timestamp + self.protocol_name + '.csv'
        self.errorfile = self.error_dir + 'error_' + self.run_timestamp + self.protocol_name + '.csv'
        self.num_data_samples = 0 # Used to track the number of data samples taken
        self.num_err_samples = 0 # Used to track the number of error samples taken
        self.num_pozyx_pulses = 0 # Used to track the number of Pozyx pulses (should align with data and error samples)

        self.timestamp_list = []
        self.data_list = []
        self.error_timestamp_list = []
        self.error_list = []

    def setup(self):
        """
        Sets up the Pozyx1DCapture object for ranging
        """
        print(f"---------- POZYX Version {version} ----------\n")

        # Print device information
        if self.remote_id is None:
            for device_id in [self.remote_id, self.destination_id]:
                self.pozyx.printDeviceInfo(device_id)
        else:
            for device_id in [self.remote_id, self.destination_id]:
                self.pozyx.printDeviceInfo(device_id)

        print(f"\n -------------------- START DATA RUN AT {datetime.datetime.now()} --------------------\n")

        # Set the ranging protocol
        self.pozyx.setRangingProtocol(self.protocol, self.remote_id)

        # Create the data and error directories if they don't exist
        self.create_directories_files()

    def create_directories_files(self):

        # Check if self.data_dir exists, otherwise create it
        if not os.path.exists(self.data_dir):
            print(f"Creating directory: '{self.data_dir}'")
            os.makedirs(self.data_dir)

        # Check if datafile exists, otherwise create it and write the header
        if not os.path.exists(self.datafile):
            print(f"Creating file: '{self.datafile}'")
            with open(self.datafile, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp (ms)', 'Distance (mm)'])

        # Check if self.error_dir exists, otherwise create it
        if not os.path.exists(self.error_dir):
            print(f"Creating directory: '{self.error_dir}'")
            os.makedirs(self.error_dir)

        # Check if errorfile exists, otherwise create it and write the header
        if not os.path.exists(self.errorfile):
            print(f"Creating file: '{self.errorfile}'")
            with open(self.errorfile, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp (ms)', 'Error Message'])


    def loop(self):
        """
        Performs continuous ranging and saves the data to a .csv file
        """

        # Create a DeviceRange object and perform ranging
        device_range = DeviceRange()
        status = self.pozyx.doRanging(self.destination_id, device_range, self.remote_id)

        if status == POZYX_SUCCESS:
            # If ranging was successful, save the data to a .csv file
            # self.write_data_to_csv(device_range)
            self.timestamp_list.append(device_range.timestamp)
            self.data_list.append(device_range.distance)
            self.num_data_samples += 1

            print(f"-----------------------------------------------------------------------------------")
            print(f"Timestamp (ms): {device_range.timestamp} \t Distance (mm): {device_range.distance}")

        else:
            # If ranging was unsuccessful, save the error to a .csv file
            error_code = SingleRegister()
            status = self.pozyx.getErrorCode(error_code)
            if status == POZYX_SUCCESS:
                error_msg = "ERROR Ranging, local %s" % self.pozyx.getErrorMessage(error_code)
                # self.write_error_to_csv(error_msg)
                self.error_timestamp_list.append(datetime.datetime.now())
                self.error_list.append(error_msg)
                self.num_err_samples += 1

                print(f"-----------------------------------------------------------------------------------")
                print(f"Timestamp (ms): {device_range.timestamp} \t Error Message: {error_msg}")

            else:
                error_msg = "ERROR Ranging, couldn't retrieve local error"
                # self.write_error_to_csv(error_msg)
                self.error_timestamp_list.append(datetime.datetime.now())
                self.error_list.append(error_msg)
                self.num_err_samples += 1

                print(f"-----------------------------------------------------------------------------------")
                print(f"Timestamp (ms): {device_range.timestamp} \t Error Message: {error_msg}")

        self.num_pozyx_pulses += 1

    def write_data_to_csv(self, device_range):
        """
        Writes the data to a .csv file
        """
        with open(self.datafile, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([device_range.timestamp, device_range.distance])

        # Increment the number of data samples
        self.num_data_samples += 1

    def write_error_to_csv(self, error_msg):
        """
        Writes the error message to a .csv file
        """
        with open(self.errorfile, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.datetime.now(), error_msg])

        # Increment the number of error samples
        self.num_err_samples += 1


def convertDataListsToCSV(timestamp_list, data_list, filename='data.csv'):
    """
    Converts the timestamp and data lists to a .csv file
    """
    if len(timestamp_list) != len(data_list):
        print(f"Timestamp list length: {len(timestamp_list)}")
        print(f"Data list length: {len(data_list)}")
        raise ValueError("The timestamp and data lists must be the same length.")

    # Save the value of the first entry in the timestamp list
    first_timestamp = timestamp_list[0]

    # Write the data to a .csv file (timestamp should be relative to the first timestamp)
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp (ms)', 'Distance (mm)', 'Timestamp Difference (ms)'])
        prior_timestamp = first_timestamp
        for i in range(len(timestamp_list)):
            writer.writerow([timestamp_list[i] - first_timestamp, data_list[i], timestamp_list[i] - prior_timestamp])
            prior_timestamp = timestamp_list[i]

def convertErrorListsToCSV(error_timestamp_list, error_list, filename='error.csv'):
    """
    Converts the error list to a .csv file
    """
    if len(error_timestamp_list) != len(error_list):
        print(f"Timestamp list length: {len(error_timestamp_list)}")
        print(f"Data list length: {len(error_list)}")
        raise ValueError("The timestamp and data lists must be the same length.")

    # Write the errors to a .csv file
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp (ms)', 'Error Message'])
        for i in range(len(error_timestamp_list)):
            writer.writerow([error_timestamp_list[i], error_list[i]])