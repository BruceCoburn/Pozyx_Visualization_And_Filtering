#!/usr/bin/env python
"""
This script is used to collect data from the Pozyx device. It is based on the ready_to_range.py script from the Pozyx
playground.

We collect data from a singular anchor and tag.

The data is saved in a .csv file with the following headers:
    - Timestep (ms)
    - Distance (mm)

'Timestep (ms)' is the time from the start of the script in milliseconds.
'Distance (mm)' is the distance between the tag and anchor in millimeters.
"""

# Import Python-native modules
import time

# Import Pozyx-specific modules
from pypozyx import PozyxSerial, PozyxConstants, get_first_pozyx_serial_port
from pypozyx.tools.version_check import perform_latest_version_check

# Import custom modules
# from pozyx_helpers.PozyxClasses import Pozyx1dCapture
from pozyx_helpers.Pozyx1DCapture import Pozyx1DCapture, convertDataListsToCSV, convertErrorListsToCSV
from pozyx_helpers.supplemental_functions import nice_print

if __name__ == "__main__":
    # Check for the latest PyPozyx version.
    # Skip if this takes too long or is not needed by setting to False.
    check_pypozyx_version = True
    if check_pypozyx_version:
        perform_latest_version_check()

    # Identify the COM Port of the Pozyx device
    serial_port = get_first_pozyx_serial_port()
    nice_print(f"POZYX serial_port: {serial_port}")
    if serial_port is None:
        print("No pozyx connected. Check your USB cable or your driver!")
        quit()

    ###########################################
    # HARDCODE the remote_id of the Pozyx tag
    ###########################################
    # remote_id = 0x683A
    remote_id = 0x6832
    remote = False  # whether to use the given remote device for ranging
    if not remote:
        remote_id = None

    ###########################################
    # HARDCODE the remote_id of the Pozyx anchor
    ###########################################
    destination_id = 0x1123

    ###########################################
    # Establish which Pozyx protocol to use
    # Options are:
    #   - PozyxConstants.RANGE_PROTOCOL_PRECISION
    #   - PozyxConstants.RANGE_PROTOCOL_FAST
    ###########################################
    pozyx = PozyxSerial(serial_port)
    ranging_protocol = PozyxConstants.RANGE_PROTOCOL_PRECISION
    # ranging_protocol = PozyxConstants.RANGE_PROTOCOL_FAST

    # Create a Pozyx1dCapture object
    pozyx1d = Pozyx1DCapture(
        pozyx=pozyx,
        destination_id=destination_id,
        protocol=ranging_protocol,
        remote_id=remote_id,
    )
    pozyx1d.setup()

    # Run the script for 10 seconds
    duration_s = 10
    start_time = time.time()
    while time.time() - start_time < duration_s:
        pozyx1d.loop()

    print("")
    nice_print(f"Ran for {duration_s} seconds using {pozyx1d.protocol_name} protocol.")
    print(f"---> Run file: {pozyx1d.datafile}")
    print(f"---> Error file: {pozyx1d.errorfile}")

    # Compute the number of samples per second
    data_samples = pozyx1d.num_data_samples
    data_samples_per_second = data_samples / duration_s

    err_samples = pozyx1d.num_err_samples
    err_samples_per_second = err_samples / duration_s

    total_samples = data_samples + err_samples
    total_samples_per_second = total_samples / duration_s

    # Print the number of samples per second
    print(
        f"Data samples per second: {data_samples_per_second} || {1/data_samples_per_second} seconds per data sample"
    )
    print(
        f"Error samples per second: {err_samples_per_second} || {1/err_samples_per_second} seconds per error sample"
    )
    print(
        f"Total samples per second: {total_samples_per_second} || {1/total_samples_per_second} seconds per sample"
    )
    print(
        f"Pozyx Pulses: {pozyx1d.num_pozyx_pulses} || Pozyx Pulses per second: {pozyx1d.num_pozyx_pulses / duration_s}"
    )

    # Convert the data and error lists to CSV files
    convertDataListsToCSV(pozyx1d.timestamp_list, pozyx1d.data_list, pozyx1d.datafile)
    convertErrorListsToCSV(pozyx1d.error_timestamp_list, pozyx1d.error_list, pozyx1d.errorfile)
