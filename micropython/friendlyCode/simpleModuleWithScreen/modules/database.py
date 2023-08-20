import ujson
from utils.time_management_module import *

#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------

class MeasurementList:

    def __init__(self,
                 minutes_between_measurement: int,
                 max_len: int = 120):

        """
            Is a cyclic list, which keeps track of the latest measurement index, 
            and the oldest_measurement_idx.
        """

        self.measurements = [0] * max_len
        self.max_len = max_len
        self.minutes_between_measurement = minutes_between_measurement

        self.oldest_measurement_idx = 0
        self.latest_measurement_idx = 0
        self.n_additions = 0

    def append(self, measurement: float):

        if (len(self.measurements) < self.max_len):
            self.measurements.append(int(round(measurement)))
            self.n_additions += 1
        
        else:
            self.latest_measurement_idx = (self.n_additions % len(self.measurements)) - 1
            self.oldest_measurement_idx = (self.latest_measurement_idx + 1) % len(self.measurements)
            self.measurements[self.latest_measurement_idx] = int(round(measurement))
            self.n_additions += 1
    
    def get_latest_measurement(self) -> float:
        return self.measurements[self.latest_measurement_idx]
    
    def nth_hour_generator(self, n_hours: int):
        """
            Returns a generator which yields the nth hour of measurements.
            The generator will yield the measurements from oldest to latest.

            If n_hours is larger than the total time of the measurement list,
            a ValueError will be raised.
        """

        if (n_hours > self.minutes_between_measurement * len(self.measurements)):
            raise ValueError("n_hours is larger than the total time of the measurement list")

        n_measurements = int(n_hours * 60 / self.minutes_between_measurement)

        #from oldest to latest
        for i in range(n_measurements):
            yield self.measurements[(self.oldest_measurement_idx + i) % len(self.measurements)]
    
    def last_n_minutes_generator(self, n_minutes: int):

        """
            Returns a generator which yields the last n_minutes of measurements.
            The generator will yield the measurements from oldest to latest.

            If n_minutes is larger than the total time of the measurement list,
            a ValueError will be raised.
        """

        if (n_minutes > self.minutes_between_measurement * len(self.measurements)):
            raise ValueError("n_minutes is larger than the total time of the measurement list")

        n_measurements = int(n_minutes / self.minutes_between_measurement)

        #from oldest to latest
        for i in range(n_measurements):
            yield self.measurements[(self.oldest_measurement_idx + i) % len(self.measurements)]
    
    def last_n_hours_generator(self, n_hours: int):
        return self.last_n_minutes_generator(n_hours * 60)
    
    def __getitem__(self, idx: int) -> float:
        """
            Gives the idx'th oldest measurement.
        """
        if (idx >= len(self.measurements)):
            raise IndexError("idx is larger than the length of the measurement list")

        return self.measurements[(self.latest_measurement_idx + idx) % len(self.measurements)]

#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------

class Database:

    def __init__(self, config_file: str) -> None:
        self.registers = dict() #Dict[str, MeasurementList]

        with open(config_file, "r") as f:
            self.config = ujson.load(f)["sensors"]
    
    def get_register(self, register_id: str) -> MeasurementList:
        if (register_id in self.registers.keys()):
            return self.registers[register_id]
        else:
            raise ValueError("Register {} does not exist".format(register_id))
    
    def add_register(self,
                     register_id: str,
                     max_len: int = 120) -> None:
        
        """
            Adds a register to the database. The register_id must correspond to the id of a sensor in the config file.
            The max_len is the maximum number of measurements that will be stored in the database.
        """

        if (register_id not in self.registers.keys()) and (register_id in self.config.keys()):

            minutes_between_measurement = Time(*self.config[register_id]["measure_every_some_time"]).to_total_minutes()
            self.registers[register_id] = MeasurementList(minutes_between_measurement, max_len)
        else:
            raise ValueError("Register {} already exists or is not in config file".format(register_id))

    def add_measurement(self, register_id: str, measurement: float) -> None:
        """
            Adds a measurement to the register with id register_id.
        """
        if (register_id in self.registers.keys()) and (measurement is not None) and (measurement > 0):
            self.registers[register_id].append(measurement)
        else:
            raise ValueError("Register {} does not exist".format(register_id))
