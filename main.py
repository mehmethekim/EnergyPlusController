from queue import Queue,Empty
from energy_plus import EnergyPlusController
from typing import Dict
import time
from datetime import datetime, timedelta
from plot import plot_energy_data

output_queue = Queue()
energy_plus_controller = EnergyPlusController(output_queue)
energy_plus_controller.start()
energy_plus_controller.stop()

plot_energy_data(output_queue)