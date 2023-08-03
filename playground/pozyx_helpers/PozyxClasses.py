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


class Pozyx1dCapture(object):
    """
    Continuously performs ranging between the Pozyx and a destination and sets their LEDs
    """

    def __init__(
        self,
        pozyx,
        destination_id,
        protocol=PozyxConstants.RANGE_PROTOCOL_PRECISION,
        remote_id=None,
        data_dir="pozyx_ranging_runs/",
        error_dir="pozyx_error_runs/",
    ):
        self.pozyx = pozyx
        self.destination_id = destination_id
        self.protocol = protocol
        self.remote_id = remote_id

        self.precision_dict = {
            0: "_PRECISION",
            1: "_FAST",
        }
        self.protocol_name = self.precision_dict[protocol]

        self.data_dir = data_dir
        self.error_dir = error_dir
        self.timestamp_difference = 0
        self.original_timestamp = datetime.datetime.now()
        self.old_timestamp = self.original_timestamp
        self.run_timestamp = self.original_timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        self.datafile = (
            self.data_dir + "data_" + self.run_timestamp + self.protocol_name + ".csv"
        )
        self.errorfile = (
            self.error_dir + "error_" + self.run_timestamp + self.protocol_name + ".csv"
        )

    def setup(self):
        """
        Sets up the Pozyx device for ranging.
        """
        print(f"------------ POZYX VERSION {version} -------------\n")

        if self.remote_id is None:
            for device_id in [self.remote_id, self.destination_id]:
                self.pozyx.printDeviceInfo(device_id)
        else:
            for device_id in [None, self.remote_id, self.destination_id]:
                self.pozyx.printDeviceInfo(device_id)

        print(f"\n ---------- START DATA RUN AT {self.original_timestamp} ----------\n")

        self.pozyx.setRangingProtocol(self.protocol, self.remote_id)

    def loop(self):
        """
        Performs ranging and saves the data to a .csv file.
        """

        device_range = DeviceRange()
        status = self.pozyx.doRanging(self.destination_id, device_range, self.remote_id)

        if status == POZYX_SUCCESS:
            # Get the current timestamp
            current_timestamp = datetime.datetime.now()

            # Get the timestamp difference from the initialization of ReadyToRange
            self.absolute_timestamp = self.get_timestamp_difference_ms(
                self.original_timestamp, current_timestamp
            )

            self.timestamp_difference = self.get_timestamp_difference_ms(
                self.old_timestamp, current_timestamp
            )

            self.old_timestamp = current_timestamp

            print(f"----------------------------")
            print(
                f"Timestep (ms): {self.absolute_timestamp:.4f} \t Distance (mm): {device_range.distance} \t"
                + f"Timestamp (ms): {current_timestamp} \t Timestamp difference (ms): {self.timestamp_difference:.4f}"
            )
            self.write_timestep_distance_to_csv(self.datafile, device_range.distance)
        else:
            error_code = SingleRegister()
            status = self.pozyx.getErrorCode(error_code)
            if status == POZYX_SUCCESS:
                error_msg = "ERROR Ranging, local %s" % self.pozyx.getErrorMessage(
                    error_code
                )

                print("")
                nice_print(error_msg)
                print("")

                self.write_error_msg_to_csv(self.errorfile, error_msg)
            else:
                error_msg = "ERROR Ranging, couldn't retrieve local error"
                print("")
                nice_print(error_msg)
                print("")

                self.write_error_msg_to_csv(self.errorfile, error_msg)

    def get_timestamp_difference_ms(self, timestamp1, timestamp2):
        """
        Returns the difference between two timestamps in milliseconds.
        """
        return (timestamp2 - timestamp1).total_seconds() * 1000

    def write_timestep_distance_to_csv(self, filename, distance):
        """
        Appends data to a .csv file.
        """

        # Check if self.data_dir exists, otherwise create it
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        file_exists = True
        try:
            with open(filename, "r"):
                pass
        except FileNotFoundError:
            file_exists = False

        # Write data to csv file
        with open(filename, "a", newline="") as csvfile:
            fieldnames = ["Timestep (ms)", "Distance (mm)"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header if the file is newly created
            if not file_exists:
                writer.writeheader()

            writer.writerow(
                {"Timestep (ms)": self.absolute_timestamp, "Distance (mm)": distance}
            )

    def write_error_msg_to_csv(self, filename, error_msg):
        """
        Appends error message to a .csv file.
        """

        # Check if self.error_dir exists, otherwise create it
        if not os.path.exists(self.error_dir):
            os.makedirs(self.error_dir)

        file_exists = True
        try:
            with open(filename, "r"):
                pass
        except FileNotFoundError:
            file_exists = False

        # Write error_msg to csv file
        with open(filename, "a", newline="") as csvfile:
            fieldnames = ["Timestep (ms)", "Error Message"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header if the file is newly created
            if not file_exists:
                writer.writeheader()

            writer.writerow(
                {"Timestep (ms)": self.absolute_timestamp, "Error Message": error_msg}
            )
