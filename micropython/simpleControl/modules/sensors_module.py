import machine

from json                   import load
from time_management_module import *


class SensorsModule():

    def __init__(self, 
                 config_file: str):


        # reads the configuration file and stores it in a dictionary
        # for later instantiation of the connection
        with open(config_file) as f:
            self.config = load(f)

        self.sensors = self.config["sensors"]
        self.default_init()
 

    def default_init(self) -> None:

        # Fills the sensors dict with a default value for the exec field

        # The 'exec' field will be mapped later to a function which specifies how to take measurements.
        # this function must return the value measured

        # The 'status' field says if the sensor is Working (True) or not working (False).
        # The 'lastmeasured' field stores the Time object of the last time the sensor was checked.

        # Time obj is a wrapper class of this: tuple(hour, minute, second)  
        for sensorName in self.sensors.keys():
            self.sensors[sensorName]["exec"]   = None
            self.sensors[sensorName]["status"] = False

            # Makes it look like it's been a while since sensors where checked for the last time
            # so that the scheduler runs each sensor on boot
            self.sensors[sensorName]["lastmeasured"] = Time(-100, 0, 0)

            # Converts the 'measure_every_x_time' field to a time object which we can work with
            self.sensors[sensorName]["measure_every_x_time"] = Time(*self.sensors[sensorName]["measure_every_x_time"])

        

    def check(self) -> None:

        """
            This function checks if all the sensors 
            have a canditate for requesting action.
        """

        print("Checking sensors...")
        for sensorName in self.sensors.keys():

            if None == self.sensors[sensorName]["exec"]:
                print("Sensor \"{}\" has no candidate for answering a call.".format(sensorName))
            
            else:
                result = self.sensors[sensorName]["exec"]()

                #if the result is does not give an error  
                if result != -1:
                    self.sensors[sensorName]["status"] = True

                else:
                    print("Sensor \"{}\" isn't OK.".format(sensorName))
        print("Done!\n")
            



    def add(self,
            sensorName: str,
            fn: callable) -> int:

        """
            This is the function the user should modify by adding the sensor 
            he/she wants.
        """

        if sensorName not in self.sensors.keys():
            print("this sensor does not exist in the ACTUATORS field. Consider adding it in the file './config.json'.")
            return -1 

        self.sensors[sensorName]["exec"] = fn
        print("{} added.".format(sensorName))

        return 0






