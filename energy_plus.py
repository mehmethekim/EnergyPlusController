from pyenergyplus.api import EnergyPlusAPI
import threading

input_file_path = "input_files.txt"

class EnergyPlusController:
    def __init__(self) -> None:
        self.api = EnergyPlusAPI()
        self.state = self.api.state_manager.new_state()
        self.runtime = self.api.runtime
        self.data_exchange = self.api.exchange
        self.cmd_args = []
        self.weather_data_file = ""
        self.example_file = ""
        self.energyplus_thread = None
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

    def _run_energyplus(self):
        self._parse_input_file()
        self.runtime.run_energyplus(self.state, self.cmd_args)
            

    def _report_progress(self,progress: int) -> None:
        if progress % 5  == 0:
            print(f"Simulation progress: {progress}%")

        
    def start(self):
        self.runtime.callback_progress(self.state, self._report_progress) 
        self.runtime.set_console_output_status(self.state, True)
        if self.energyplus_thread is None or not self.energyplus_thread.is_alive():
            self.energyplus_thread = threading.Thread(target=self._run_energyplus)
            self.energyplus_thread.start()
            print("EnergyPlus started")

    def stop(self):
        if self.energyplus_thread and self.energyplus_thread.is_alive():
            self.energyplus_thread.join()  # Wait for the thread to finish
            print("EnergyPlus stopped")
        else:
            print("EnergyPlus is not running")
