import time
from time_management_module import *

class Scheduler():

    def __init__(self, module: Module):

        self.module    = module
        self.actuators = module.actuators
        self.boot      = True

        self.current_time = Time(*get_current_time())

        #adds all the timed actuators
        self.timed_actuators = []
        self.onoff_actuators = []
        
        for actuatorName in self.actuators.keys():
            if self.actuators[actuatorName]["type"] == 'timed':
                self.timed_actuators.append(actuatorName)

            if self.actuators[actuatorName]["type"] == 'on/off':
                self.onoff_actuators.append(actuatorName)

    def control_timed_actuators(self):


        for act in self.timed_actuators:

            #went beyond the end time
            if self.current_time > self.actuators[act]["endtime"]:
                self.actuators[act]["exec"].value(0)

            #is too early and is not time to start
            elif self.current_time < self.actuators[act]["starttime"]:
                self.actuators[act]["exec"].value(0)

            #is on time
            else:

                lastchecked = self.actuators[act]["lastchecked"]

                delta = (self.current_time - lastchecked).min
                value = self.actuators[act]["status"]

                #if actuator is off
                if value == 0:
                    if delta > self.actuators[act]["minutesoff"]:
                        self.actuators[act]["exec"].value(1)
                        self.actuators[act]["status"] = 1

                #if actuator is on
                elif value == 1:
                    if delta > self.actuators[act]["minuteson"]:
                        self.actuators[act]["exec"].value(0)
                        self.actuators[act]["status"] = 0
                
    def control_on_off_actuators(self):


        for act in self.onoff_actuators:
            
            #went beyond the end time
            if self.current_time > self.actuators[act]["endtime"]:
                self.actuators[act]["exec"].value(0)

            #is too early and is not time to start
            elif self.current_time < self.actuators[act]["starttime"]:
                self.actuators[act]["exec"].value(0)
 
    def loop(self):

        last = time.ticks_ms()
        check_every_n_minutes = 3
        check_every_n_seconds = check_every_n_minutes * 60 * 1000

        # Main loop that runs indefinitely
        while True:

            # Current time in milliseconds
            now = time.ticks_ms()

            # Check if 3 minutes have elapsed since the last task execution
            if (time.ticks_diff(now, last) >= check_every_n_seconds) or (self.boot):

                #update time 
                self.current_time = Time(*get_current_time())
                print("curent time {}".format(self.current_time))

                print("handling on/off actuators...")
                self.control_on_off_actuators()
                print("handling timed actuators...")
                self.control_timed_actuators()

                # Update the last execution time
                last = now
                self.boot = False
                print("Done!")

            # Wait for a short amount of time before checking the time again
            sleep(2)

