#!/usr/bin/env python
"""
The Pozyx ready to range tutorial (c) Pozyx Labs
Please read the tutorial that accompanies this sketch: https://www.pozyx.io/Documentation/Tutorials/ready_to_range/Python

This demo requires two Pozyx devices. It demonstrates the ranging capabilities and the functionality to
to remotely control a Pozyx device. Move around with the other Pozyx device.

This demo measures the range between the two devices. The closer the devices are to each other, the more LEDs will
light up on both devices.
"""
import datetime
import os
import csv

from pypozyx import (
    PozyxSerial,
    PozyxConstants,
    version,
    SingleRegister,
    DeviceRange,
    POZYX_SUCCESS,
    POZYX_FAILURE,
    get_first_pozyx_serial_port,
    get_serial_ports,
)

from pypozyx.tools.version_check import perform_latest_version_check


class ReadyToRange(object):
    """Continuously performs ranging between the Pozyx and a destination and sets their LEDs"""

    def __init__(
        self,
        pozyx,
        destination_id,
        range_step_mm=1000,
        protocol=PozyxConstants.RANGE_PROTOCOL_PRECISION,
        remote_id=None,
    ):
        self.pozyx = pozyx
        self.destination_id = destination_id
        self.range_step_mm = range_step_mm
        self.remote_id = remote_id
        self.protocol = protocol

        self.old_timestamp = 0
        self.timestamp_difference = 0

        self.mkdir_name = "ranging_runs/"
        self.original_timestamp = datetime.datetime.now()
        self.filename_timestamp = self.original_timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = self.mkdir_name + "pozyx_" + self.filename_timestamp + ".csv"

    def setup(self):
        """Sets up both the ranging and destination Pozyx's LED configuration"""
        print("------------POZYX RANGING V{} -------------".format(version))
        print("NOTES: ")
        print(" - Change the parameters: ")
        print("\tdestination_id(target device)")
        print("\trange_step(mm)")
        print("")
        print("- Approach target device to see range and")
        print("led control")
        print("")
        if self.remote_id is None:
            for device_id in [self.remote_id, self.destination_id]:
                self.pozyx.printDeviceInfo(device_id)
        else:
            for device_id in [None, self.remote_id, self.destination_id]:
                self.pozyx.printDeviceInfo(device_id)
        print("")
        print("- -----------POZYX RANGING V{} -------------".format(version))
        print("")
        print("START Ranging: ")

        # make sure the local/remote pozyx system has no control over the LEDs.
        led_config = 0x0
        self.pozyx.setLedConfig(led_config, self.remote_id)
        # do the same for the destination.
        self.pozyx.setLedConfig(led_config, self.destination_id)
        # set the ranging protocol
        self.pozyx.setRangingProtocol(self.protocol, self.remote_id)

    def loop(self):
        """Performs ranging and sets the LEDs accordingly"""
        device_range = DeviceRange()
        status = self.pozyx.doRanging(self.destination_id, device_range, self.remote_id)
        self.timestamp_difference = device_range.timestamp - self.old_timestamp
        self.old_timestamp = device_range.timestamp
        if status == POZYX_SUCCESS:
            print(f"--------------------------")
            print(
                f"Timstamp: {device_range.timestamp} ms\t Timestamp difference: {self.timestamp_difference} ms \t Distance: {device_range.distance} mm"
            )
            print(f"Timstamp difference: {self.timestamp_difference} ms")
            print(f"Distance: {device_range.distance} mm")
            self.append_distance_to_csv(
                filename=self.filename, distance=device_range.distance
            )
            if self.ledControl(device_range.distance) == POZYX_FAILURE:
                print("ERROR: setting (remote) leds")
        else:
            error_code = SingleRegister()
            status = self.pozyx.getErrorCode(error_code)
            if status == POZYX_SUCCESS:
                print(
                    "ERROR Ranging, local %s" % self.pozyx.getErrorMessage(error_code)
                )
            else:
                print("ERROR Ranging, couldn't retrieve local error")

    def ledControl(self, distance):
        """Sets LEDs according to the distance between two devices"""
        status = POZYX_SUCCESS
        ids = [self.remote_id, self.destination_id]
        # set the leds of both local/remote and destination pozyx device
        for id in ids:
            status &= self.pozyx.setLed(4, (distance < range_step_mm), id)
            status &= self.pozyx.setLed(3, (distance < 2 * range_step_mm), id)
            status &= self.pozyx.setLed(2, (distance < 3 * range_step_mm), id)
            status &= self.pozyx.setLed(1, (distance < 4 * range_step_mm), id)
        return status

    def get_timestamp_difference_ms(self, timestamp1, timestamp2):
        ms_difference = timestamp1 - timestamp2
        return ms_difference.total_seconds() * 1000

    def append_distance_to_csv(self, filename, distance):
        # Check if the file exists
        # If it does not exist, create it and add the header
        # If it does exist, append the data to the file

        # Check if self.mkdir_name exists and create it if it does not
        if not os.path.exists(self.mkdir_name):
            os.makedirs(self.mkdir_name)

        file_exists = True
        try:
            with open(filename, "r"):
                pass
        except FileNotFoundError:
            file_exists = False

        # Write data to CSV file
        with open(filename, "a", newline="") as csvfile:
            fieldnames = ["Timestep (ms)", "Distance (mm)"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header if the file is newly created
            if not file_exists:
                writer.writeheader()

            timestep = self.get_timestamp_difference_ms(
                datetime.datetime.now(), self.original_timestamp
            )

            # Write the data to the CSV file
            writer.writerow({"Timestep (ms)": timestep, "Distance (mm)": distance})


if __name__ == "__main__":
    # Check for the latest PyPozyx version. Skip if this takes too long or is not needed by setting to False.
    check_pypozyx_version = True
    if check_pypozyx_version:
        perform_latest_version_check()

    # hardcoded way to assign a serial port of the Pozyx
    # serial_port = 'COM3'

    # the easier way
    serial_port = get_first_pozyx_serial_port()
    print(f"serial_port: {serial_port}")
    # serial_port = get_serial_ports()[1]
    if serial_port is None:
        print("No Pozyx connected. Check your USB cable or your driver!")
        quit()

    # remote_id = 0x605D           # the network ID of the remote device
    remote_id = 0x683A
    remote = False  # whether to use the given remote device for ranging
    if not remote:
        remote_id = None

    # destination_id = 0x6e66      # network ID of the ranging destination
    destination_id = 0x1123  # network ID of the ranging destination
    # distance that separates the amount of LEDs lighting up.
    range_step_mm = 1000

    # the ranging protocol, other one is PozyxConstants.RANGE_PROTOCOL_PRECISION
    # ranging_protocol = PozyxConstants.RANGE_PROTOCOL_PRECISION
    ranging_protocol = PozyxConstants.RANGE_PROTOCOL_FAST

    pozyx = PozyxSerial(serial_port)
    r = ReadyToRange(pozyx, destination_id, range_step_mm, ranging_protocol, remote_id)
    r.setup()
    print(f"after setup...")
    while True:
        r.loop()
