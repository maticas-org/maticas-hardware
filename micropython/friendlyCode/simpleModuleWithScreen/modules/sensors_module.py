import gc
from json import load
from utils.time_management_module import *
from friendlyCode.simpleModuleWithScreen.utils.metrics import Statistics

import initialize_database as db
#----------------------------------------------------------------------------------
#
#----------------------------------------------------------------------------------

class SensorWrapper:

    #use the instance of Database as a class attribute
    _database = db.db_mod

    def __init__(self, 
                 sensor_id: str,
                 sensor_name: str,
                 measure_every_some_time: Time):
        
        self.id = sensor_id
        self.name = sensor_name
        self.last_measured = Time(-100, 0, 0)
        self.measure_every_some_time = measure_every_some_time
        self.measurement_function = None

    @property
    def is_working(self) -> bool:
        """
            Tells wheter or not a measurement_function has been provided
            and therefore if the sensorwrapper works
        """
        return self.measurement_function != None

    def add_to_database(self, measurement: float):
        SensorWrapper._database.add_measurement(self.id, measurement)

    def set_measurement_function(self, fn: callable) -> None:
        self.measurement_function = fn

    def measure(self, now: Time) -> float:
        
        if (self.is_working):
            return self.measurement_function()
        elif (not self.is_working):
            raise ValueError("No measure function has been set")
            
    
    def timed_measurement(self, now: Time) -> float:
        """ 
            This function is used for checking if it's time to measure again.
        """

        if not self.is_working:
            print("Sensor {} is not working...".format(self.name))
            return None

        elif now - self.last_measured >= self.measure_every_some_time:
            self.last_measured = now
            measurement = self.measure(self.last_measured)
            print("{} value is: {}".format(self.name, measurement))

            self.add_to_database(measurement)
            return measurement

        else:
            print("We don't need the {} measurement yet, delta: {}".format(self.name, now - self.last_measured))
            return None

    def __str__(self) -> str:
        return "SensorWrapper: {} ({})".format(self.name, self.id)
    
    def __repr__(self) -> str:
        return self.__str__()

#----------------------------------------------------------------------------------
#
#----------------------------------------------------------------------------------

class SensorsModule():

    def __init__(self,
                 config_file: str):

        # reads the configuration file and stores it in a dictionary
        # for later instantiation of the connection
        with open(config_file) as f:
            self.config = load(f)

        self.sensors_config = self.config["sensors"]
        self.sensors = dict() #type Dict[str, SensorWrapper]
        self.default_init()

    def timed_measurement(self, now: Time):
        for sensor_id in self.sensors.keys():
            self.sensors[sensor_id].timed_measurement(now)

    def default_init(self) -> None:

        for sensor_id in self.sensors_config.keys():
            self.sensors[sensor_id] = SensorWrapper(sensor_id,
                                                    self.sensors_config[sensor_id]["name"], 
                                                    Time(*self.sensors_config[sensor_id]["measure_every_some_time"]),)

    def set_measurement_function(self,
                                 sensor_id: str,
                                 fn: callable) -> int:

        """
            Sets a measurement function 
        """

        if sensor_id not in self.sensors.keys():
            print("this sensor does not exist in the ACTUATORS field. Consider adding it in the file './config.json'.")
            return -1

        self.sensors[sensor_id].set_measurement_function(fn)
        print("Sensor {} added.".format(self.sensors[sensor_id].name))

        return 0