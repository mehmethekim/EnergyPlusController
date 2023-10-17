import sys

import time
import threading
from energy_plus import EnergyPlusController

energy_plus_controller = EnergyPlusController()
energy_plus_controller.start()
energy_plus_controller.stop()