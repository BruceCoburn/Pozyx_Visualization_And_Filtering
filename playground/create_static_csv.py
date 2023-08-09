import csv


def create_csv(frequency, constant_distance, number_of_secs=10, filename="output.csv"):
    timestep_interval = 1000 / frequency  # Convert frequency (Hz) to interval (ms)
    total_data_points = int(frequency * number_of_secs)  # how many seconds worth of data points

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timesteps (ms)", "Distance (mm)"])

        total_time = 0
        for _ in range(total_data_points):
            writer.writerow([total_time, constant_distance])
            total_time += timestep_interval


if __name__ == "__main__":
    # Get user input for frequency and constant distance
    # frequency = float(input("Enter the frequency (Hz): "))
    # distance = float(input("Enter the constant distance (mm): "))

    frequency = 62 # Hz
    distance = 1867 # mm

    distance_str = str(distance)

    output_filename = f'static_{distance_str[0]}p{distance_str[1:]}m.csv'

    create_csv(frequency, distance, number_of_secs=10, filename=output_filename)
    print(f"CSV generated with filename '{output_filename}'")
