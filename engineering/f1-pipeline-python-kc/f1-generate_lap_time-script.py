import random
import csv

def generate_lap_time():
    #Generate a random lap time between 1:20 and 1:40 (mm:ss format).
    minutes = 1  #defualt 1 minute 
    seconds = random.randint(20, 40)  # Random seconds between 20 and 40
    return f"{minutes}:{seconds:02d}"  # Ensure two-digit seconds

def generate_f1_lap_times(drivers, min_laps=3):
     #Generate F1 lap times for each driver
    lap_data = []
    for driver in drivers:
        laps = random.randint(min_laps, min_laps + 5)  # At least 3, up to 8 laps
        for lap in range(1, laps + 1):
            lap_time = generate_lap_time()
            lap_data.append((driver, lap, lap_time))
    return lap_data

def export_to_csv(lap_times, filename="f1_generate_lap_times.csv"):
    #Export genrate lap times to a CSV header.
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Driver", "Lap", "Time"])
        writer.writerows(lap_times)

# Generate driver list base on https://www.formula1.com/en/results/2021/races/1064/bahrain/practice/1
drivers = ["Max Verstappen", "Valtteri Bottas", "Lando Norris", "Lewis Hamilton", "Charles Leclerc", "Sergio Perez","Pierre Gasly", "Carlos Sainz","Daniel Ricciardo" ]

# Generate random lap times function 
lap_times = generate_f1_lap_times(drivers)

# Export the f1_generate_lap_times.csv to file location
export_to_csv(lap_times, "/f1-pipeline-python-kc/f1_generate_lap_times.csv")
