import csv
import math


def sine_wave_values(frequency, duration):
    """
    Generate values from a sine wave based on frequency and duration.

    :param frequency: Frequency of the sine wave (in Hz)
    :param duration: Duration for which sine wave values need to be generated (in seconds)
    :return: List of (time, value) pairs
    """
    sample_rate = 1000  # samples per second
    values = []

    for t in range(int(sample_rate * duration)):
        time = t / sample_rate
        value = math.sin(2 * math.pi * frequency * time)
        values.append((time, value))

    return values


def write_to_csv(data, filename="sine_wave.csv"):
    """
    Write data to a CSV file.

    :param data: List of data to be written to the CSV
    :param filename: Name of the CSV file
    """
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Time", "Value"])  # Header
        writer.writerows(data)


def main():
    # frequency = float(input("Enter the frequency (in Hz) of the sine wave: "))
    """
    duration = float(
        input(
            "Enter the time duration (in seconds) for which values need to be generated: "
        )
    )
    """
    frequency = 440 # Hz
    duration = 1 # seconds
    filename = "sine_wave_440_Hz.csv"

    values = sine_wave_values(frequency, duration)
    write_to_csv(values, filename=filename)
    print(f"Sine wave values written to {filename}")


if __name__ == "__main__":
    main()
