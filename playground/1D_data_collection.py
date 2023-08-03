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
from pozyx_helpers.PozyxClasses import Pozyx1dCapture
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
    remote_id = 0x683A
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
    pozyx1d = Pozyx1dCapture(
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
    nice_print(f"Ran for {duration_s} seconds.")
    print(f"---> Run file: {pozyx1d.datafile}")
    print(f"---> Error file: {pozyx1d.errorfile}")