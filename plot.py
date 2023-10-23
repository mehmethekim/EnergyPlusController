
from typing import Dict
from datetime import datetime, timedelta
from queue import Queue,Empty
import matplotlib.pyplot as plt
import matplotlib.animation as animation
def plot_energy_data(output_queue:Queue):
    zone_mean_temp = []  # List to store 'zone_mean_temp' values
    site_outdoor_temp = []  # List to store 'site_outdoor_temp' values
    site_sky_cover = []  # List to store 'site_sky_cover' values
    data : Dict[str, float] = {}  # Dict to store data from the queue

    


    date_time = []
    try:
        while True:
            data  = output_queue.get(timeout=1)  # Get data from the queue
            if int(data["year"]==1998) and data["day"]>13:
                print("Year is ",data["year"])
                zone_mean_temp.append(data.get('zone_mean_temp', 0))
                site_outdoor_temp.append(data.get('site_outdoor_temp', 0))
                site_sky_cover.append(data.get('site_sky_cover', 0))
                date_time.append(datetime(year=int(data["year"]), month=int(data["month"]), day=int(data["day"]), hour=int(data["hour"])))
            # Update the current date by adding 1 hour

    except Empty:
        pass

    # Create the line graph
    # Sort the date_time list in ascending order
    date_time.sort()
    plt.plot(date_time, zone_mean_temp, label='Zone Mean Temp')
    plt.plot(date_time, site_outdoor_temp, label='Site Outdoor Temp')
    #plt.plot(date_time, site_sky_cover, label='Site Sky Cover')

    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.legend()
    plt.show()

# Call the plotting function with your output_queue
# plot_energy_data(output_queue)