from machine import Pin
from json import load
from utils.time_management_module import *

class ActuatorsModule():

    def __init__(self,
                 config_file: str):

        # reads the configuration file and stores it in a dictionary
        # for later instantiation of the connection
        with open(config_file) as f:
            self.config = load(f)

        self.actuators = self.config["actuators"]
        self.timed_actuators = []
        self.onoff_actuators = []

        self.default_init()

    def default_init(self) -> None:

        # Fills the actuators dict with a default value for the exec field

        # The exec field will be mapped later to a pin object.
        # The status field says if the actuator is on or off.
        # The lastchecked field stores the Time object when the actuator was checked.

        # Time obj is a wrapper class of this: tuple(hour, minute, second)
        for actuatorName in self.actuators.keys():
            self.actuators[actuatorName]["exec"] = None
            self.actuators[actuatorName]["status"] = False

            # makes it look like it's been a while since actuators where checked for the last time
            # so that the scheduler runs each actuator on boot
            self.actuators[actuatorName]["lastmodified"] = Time(*self.actuators[actuatorName]["starttime"]) - Time(100,
                                                                                                                   0, 0)
            self.actuators[actuatorName]["starttime"] = Time(*self.actuators[actuatorName]["starttime"])
            self.actuators[actuatorName]["endtime"] = Time(*self.actuators[actuatorName]["endtime"])

        # Separates the actuatornames into the ones which are
        # timed and the ones that are not timed
        for actuatorName in self.actuators.keys():
            if self.actuators[actuatorName]["type"] == 'timed':
                self.timed_actuators.append(actuatorName)

            elif self.actuators[actuatorName]["type"] == 'on/off':
                self.onoff_actuators.append(actuatorName)

    def startup_off(self) -> None:

        print("Starting up actuators...")
        # turn off all the actuators at boot
        for actuatorName in self.actuators.keys():

            if self.actuators[actuatorName]["exec"] != None:
                self.actuators[actuatorName]["exec"].value(0)

        print("Done! they are all OFF.\n")

    def check(self) -> None:

        """
            This function checks if all the actuators
            have a canditate for requesting action.
        """

        print("Checking actuators...")
        for actuatorName in self.actuators.keys():

            if None == self.actuators[actuatorName]["exec"]:
                print("actuator \"{}\" has no candidate for answering a call".format(actuatorName))

        print("Done!\n")

    def add(self,
            actuator: str,
            pin: Pin) -> int:

        """
            This is the function the user should modify by adding the actuator
            he/she wants.
        """

        if actuator not in self.actuators.keys():
            print(
                "this actuator does not exist in the ACTUATORS field. Consider adding it in the file './config.json'.")
            return -1

        self.actuators[actuator]["exec"] = pin
        print("{} added.".format(actuator))

        return 0




