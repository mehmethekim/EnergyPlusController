from queue import Queue,Empty
from energy_plus import EnergyPlusController
from typing import Dict
import time
from datetime import datetime, timedelta
output_queue = Queue()

#{'zone_mean_temp': 20.45973124627728, 'site_outdoor_temp': 17.8, 'site_sky_cover': 2.25}
#Plot queue contents using matplot lib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

energy_plus_controller = EnergyPlusController(output_queue)
energy_plus_controller.start()
energy_plus_controller.stop()
data  = output_queue.get(timeout=1) 
print(data)
def plot_energy_data(output_queue:Queue):
    timestamps = []  # List to store timestamps
    zone_mean_temp = []  # List to store 'zone_mean_temp' values
    site_outdoor_temp = []  # List to store 'site_outdoor_temp' values
    site_sky_cover = []  # List to store 'site_sky_cover' values
    data : Dict[str, float] = {}  # Dict to store data from the queue
    delta_time = 0
    start_date = datetime(2013, 10, 17, 0, 0)  # Starting date (year, month, day, hour, minute)
    current_date = start_date  # Initialize the current date
    try:
        while True:
            data  = output_queue.get(timeout=1)  # Get data from the queue
            timestamps.append(current_date)  # Record the timestamp
            zone_mean_temp.append(data.get('zone_mean_temp', 0))
            site_outdoor_temp.append(data.get('site_outdoor_temp', 0))
            site_sky_cover.append(data.get('site_sky_cover', 0))
            # Update the current date by adding 1 hour
            current_date += timedelta(hours=1)

    except Empty:
        pass

    # Create the line graph
    plt.plot(timestamps, zone_mean_temp, label='Zone Mean Temp')
    plt.plot(timestamps, site_outdoor_temp, label='Site Outdoor Temp')
    plt.plot(timestamps, site_sky_cover, label='Site Sky Cover')

    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.legend()
    plt.show()

# Call the plotting function with your output_queue
plot_energy_data(output_queue)