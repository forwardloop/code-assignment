import csv
from datetime import datetime

def import_from_csv(filename="/f1-pipeline-python-kc/f1_generate_lap_times.csv"):
    # Import lap times from a f1_generate_lap_times.csv CSV file location.
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        lap_times = [(row[0], int(row[1]), row[2]) for row in reader]
    
    return lap_times

def validate_data(lap_times):
    # Validate f1_generate_lap_times data before moving to calculate average lap times.
    driver_lap_counts = {}
    for row in lap_times:
        driver, lap, time = row
        
        if not isinstance(driver, str) or not driver.strip():  # Check if driver is not string
            raise ValueError(f"Invalid driver name: {driver}")
        if not isinstance(lap, int) or lap <= 0:  # Check if lap time not integer and time lap less than 0
            raise ValueError(f"Invalid lap number: {lap}")
        try:
            datetime.strptime(time, "%M:%S")  # Ensure the lap time mm:ss format 
        except ValueError:
            raise ValueError(f"Invalid time format: {time}")
        
        driver_lap_counts[driver] = driver_lap_counts.get(driver, 0) + 1
    
    for driver, count in driver_lap_counts.items():  # Check if driver has at least 3 laps recorded
        if count < 3:
            raise ValueError(f"Driver {driver} has fewer than 3 laps recorded.")

def calculate_average_lap_times(lap_times):
    # Calculate average lap time per driver and return top 3 in ascending order.
    lap_totals = {}
    lap_counts = {}
    
    # Convert minutes + seconds to total seconds
    for driver, _, time in lap_times:
        minutes, seconds = map(int, time.split(":"))
        total_seconds = minutes * 60 + seconds
        
        if driver not in lap_totals: 
            lap_totals[driver] = 0
            lap_counts[driver] = 0
        
        lap_totals[driver] += total_seconds
        lap_counts[driver] += 1
    
    # Calculate average lap time for top 3 drivers
    average_lap_times = {driver: lap_totals[driver] / lap_counts[driver] for driver in lap_totals}
    
    # Return top 3 drivers in ascending order of their average lap time
    sorted_drivers = sorted(average_lap_times.items(), key=lambda x: x[1])[:3]
    
    # Return the result for CSV output 
    return [(driver, f"{int(avg // 60)}:{int(avg % 60):02d}") for driver, avg in sorted_drivers]

def calculate_fastest_lap_times(lap_times):
    # Calculate the fastest lap time per driver
    driver_fastest_times = {}
    
    for driver, _, time in lap_times:
        minutes, seconds = map(int, time.split(":"))
        total_seconds = minutes * 60 + seconds
        
        if driver not in driver_fastest_times:
            driver_fastest_times[driver] = total_seconds
        else:
            # Update if this lap is faster (smaller total seconds)
            driver_fastest_times[driver] = min(driver_fastest_times[driver], total_seconds)
    
    # Convert the fastest times back to minutes:seconds format
    return {driver: f"{int(seconds // 60)}:{int(seconds % 60):02d}" for driver, seconds in driver_fastest_times.items()}

def export_best_lap_times_with_fast_time(top_three, fastest_times, filename="top-3-drivers-result.csv"):
    """Export the best average lap times with fast times to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Driver", "Average Time", "Fastest Time"])
        for driver, avg_time in top_three:
            fast_time = fastest_times.get(driver, "N/A")
            writer.writerow([driver, avg_time, fast_time])

# Import and read the lap times from f1_generate_lap_times.csv
lap_times = import_from_csv()

# Validate data
validate_data(lap_times)

# Calculate the top 3 drivers with the best average lap times
top_three = calculate_average_lap_times(lap_times)

# Calculate the fastest lap time for each driver
fastest_times = calculate_fastest_lap_times(lap_times)

# Export results to the CSV file with fast times
export_best_lap_times_with_fast_time(top_three, fastest_times, "/f1-pipeline-python-kc/top-3-drivers-result.csv")
