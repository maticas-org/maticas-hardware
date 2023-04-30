import machine

from json                   import load
from time_management_module import *


class Module():

    def __init__(self, 
                 config_file: str):


        # reads the configuration file and stores it in a dictionary
        # for later instantiation of the connection
        with open(config_file) as f:
            self.config = load(f)

        self.actuators = self.config["actuators"]
        self.default_init()
 

    def default_init(self) -> None:

        #fills the actuators dict with a default value for the exec field

        #the exec field will be mapped later to a pin object.
        #the status field says if the actuator is on or off.
        #the lastchecked field stores the Time object when the actuator was checked.

        #Time obj is a wrapper class of this: tuple(hour, minute, second)  
        for actuatorName in self.actuators.keys():
            self.actuators[actuatorName]["exec"]   = None
            self.actuators[actuatorName]["status"] = False

            self.actuators[actuatorName]["lastchecked"] = Time(*self.actuators[actuatorName]["starttime"])
            self.actuators[actuatorName]["starttime"]   = Time(*self.actuators[actuatorName]["starttime"])
            self.actuators[actuatorName]["endtime"]     = Time(*self.actuators[actuatorName]["endtime"])


    def check_actuators(self) -> None:

        """
            This function checks if all the actuators 
            have a canditate for requesting action.
        """

        for actuatorName in self.actuators.keys():

            if "" == self.actuators[actuatorName]["exec"]:
                print("actuator \"{}\" has no candidate for answering a call".format(actuatorName))
            

    def add_actuator(self,
                     actuator: str,
                     pin: Pin):

        """
            This is the function the user should modify by adding the actuator 
            he/she wants.
        """

        if actuator not in self.actuators.keys():
            print("this actuator does not exist in the ACTUATORS field. Consider adding it in the file './config.json'.")
            return

        self.actuators[actuator]["exec"] = pin
        print("{} added.".format(actuator))

        return 0



