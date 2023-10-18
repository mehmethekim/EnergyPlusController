from pyenergyplus.api import EnergyPlusAPI
from pyenergyplus.datatransfer import DataExchange
from typing import Dict
from queue import Queue
import threading

input_file_path = "input_files.txt"

class EnergyPlusController:
    """
        Initialize an EnergyPlusController.

        Parameters:
        - output_queue (Queue): A queue for collecting simulation output data.

        This constructor initializes an EnergyPlus API, sets up a simulation state, and defines several variables
        to be used in the simulation. It also initializes various internal attributes.

        Example:
        energyplus_controller = EnergyPlusController(output_queue)
    """
    def __init__(self,output_queue:Queue) -> None:
        self.api = EnergyPlusAPI()
        self.state = self.api.state_manager.new_state()
        self.runtime = self.api.runtime
        self.data_exchange = self.api.exchange
        self.cmd_args = []
        self.weather_data_file = ""
        self.example_file = ""
        self.energyplus_thread = None
        self.initialized = False
        self.output_queue = output_queue
        #VARIABLES TO USE IN THE SIMULATION
        self.variables = {
                
                "zone_mean_temp": ("Zone Mean Air Temperature","ZONE ONE" ),
                "site_outdoor_temp": ("Site Outdoor Air Drybulb Temperature","Environment"  ),
                "site_sky_cover": ("Site Total Sky Cover" ,"Environment" ),
        }

        self.var_handles: Dict[str, int] = {}
    """
        Initialize the EnergyPlus environment.

        This function initializes the EnergyPlus environment, including variable handles and state, if it has not
        already been initialized.

        Returns:
        - bool: True if initialization was successful, False if already initialized or during warm-up.

        This function is typically called internally by other methods and is not meant for external use.
    """
    def _initialize_environment(self):
        if self.initialized:
            return True
        if self.data_exchange.warmup_flag(self.state):
            return False
        self.var_handles = {
                key: self.data_exchange.get_variable_handle(self.state, *var)
                for key, var in self.variables.items()
            }
        print(self.var_handles)
        self.initialized =True
        return True
    """
        Parse the input file to extract necessary information.

        This function reads an input file and extracts the paths to weather data and an example file, which are used
        as command-line arguments when running EnergyPlus.

        This function is typically called internally by other methods and is not meant for external use.
    """
    def _parse_input_file(self) -> None:
        with open(input_file_path, "r") as file:
            lines = file.readlines()
        # Assuming the first line contains the weather data file path and the second line contains the example file path
        if len(lines) >= 1:
            self.weather_data_file = lines[0].strip()
        if len(lines) >= 2:
            self.example_file = lines[1].strip()
        
        self.cmd_args.append("-w")
        self.cmd_args.append(self.weather_data_file)
        self.cmd_args.append("-d")
        self.cmd_args.append("sim_output")
        self.cmd_args.append(self.example_file)
    """
        Run the EnergyPlus simulation.

        This function runs the EnergyPlus simulation using the command-line arguments specified in the input file.

        This function is typically called internally by other methods and is not meant for external use.
    """
    def _run_energyplus(self):
        self._parse_input_file()
        self.runtime.run_energyplus(self.state, self.cmd_args)
            
    """
        Report the progress of the simulation.

        Parameters:
        - progress (int): The progress percentage of the simulation.

        This function prints the simulation progress if it's a multiple of 5.

        This function is typically called internally by other methods and is not meant for external use.
        """
    def _report_progress(self,progress: int) -> None:
        if progress % 5  == 0:
            print(f"Simulation progress: {progress}%")
    
    
    def _parse_output(self):
        pass
    """
        Collect and store output data from the EnergyPlus simulation.

        Parameters:
        - _state: The EnergyPlus simulation state (unused).

        This function collects and stores the output data, such as variable values, and puts it in the output queue.

        This function is typically called internally by other methods and is not meant for external use.
    """
    def _collect_output(self,_state):
        #self.data_exchange.process_outputs(self.state)
        if not self._initialize_environment():
            return
        self.next_output = {
            **{
                key: self.data_exchange.get_variable_value(self.state, handle)
                for key, handle
                in self.var_handles.items()
            }
        }
        print(self.next_output)
        self.output_queue.put(self.next_output)
    """
        Start the EnergyPlus simulation.

        This function sets up callbacks for progress reporting and output collection, runs the EnergyPlus simulation
        in a separate thread, and suppresses console output.

        Example:
        energyplus_controller.start()
    """
    def start(self):
        self.runtime.callback_progress(self.state, self._report_progress)
        # register callback used to collect observations
        self.runtime.callback_end_zone_timestep_after_zone_reporting(self.state, self._collect_output)
 
        self.runtime.set_console_output_status(self.state, False)
        if self.energyplus_thread is None or not self.energyplus_thread.is_alive():
            self.energyplus_thread = threading.Thread(target=self._run_energyplus)
            self.energyplus_thread.start()
            print("EnergyPlus started")
    """
        Stop the EnergyPlus simulation.

        This function waits for the EnergyPlus simulation thread to finish and then stops it.

        Example:
        energyplus_controller.stop()
    """
    def stop(self):
        if self.energyplus_thread and self.energyplus_thread.is_alive():
            self.energyplus_thread.join()  # Wait for the thread to finish
            print("EnergyPlus stopped")

        else:
            print("EnergyPlus is not running")
