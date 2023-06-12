measureimport machine

from time_management_module import *
from internet_connection    import *


class Scheduler():

    def __init__(self,
                 act_module: ActuatorsModule,
                 sen_module: SensorsModule):

        self.act_module = act_module
        self.sen_module = sen_module

        self.actuators  = act_module.actuators
        self.sensors    = sen_module.sensors
        self.boot       = True

        #gets the timed and on/off actuators names
        self.timed_actuators = act_module.timed_actuators
        self.onoff_actuators = act_module.onoff_actuators

        self.current_time = Time(*get_current_time())
        self.check()

    def check(self):
        self.act_module.check()
        self.sen_module.check()


    def measure(self):

        for sensorName, values in self.sensors.items():
            delta = self.current_time - values["lastmeasured"]
            
            if delta > values["measure_every_x_time"]:
                measurement = values["exec"]()
                print("{} value is: {}".format(sensorName, measurement)

            else:
                print("We don't need the {} measurement yet, delta: {}".format(sensorName, delta)


    def control_timed_actuators(self):


        #for each timed actuator it ensures if it should be on or off
        for act in self.timed_actuators:

            #went beyond the end time
            if self.current_time > self.actuators[act]["endtime"]:
                self.actuators[act]["exec"].value(0)

            #is too early and is not time to start
            elif self.current_time < self.actuators[act]["starttime"]:
                self.actuators[act]["exec"].value(0)

            #is on time
            else:

                lastmodified = self.actuators[act]["lastmodified"]

                delta = self.current_time - lastmodified
                delta_min = delta.to_total_minutes() 

                value = self.actuators[act]["status"]

                #if actuator is off
                if value == 0:

                    if delta_min > self.actuators[act]["minutesoff"]:
                        self.actuators[act]["exec"].value(1)
                        self.actuators[act]["status"] = 1
                        self.actuators[act]["lastmodified"] = self.current_time 

                        print("Actuator {} should be ON. Time elapsed since OFF is {}.".format(act, delta))

                    else:
                        print("Actuator {} OK it is OFF. Time elapsed since lastcheck is {}.".format(act, delta))

                #if actuator is on
                elif value == 1:
                    if delta_min > self.actuators[act]["minuteson"]:
                        self.actuators[act]["exec"].value(0)
                        self.actuators[act]["status"] = 0
                        self.actuators[act]["lastmodified"] = self.current_time 

                        print("Actuator {} should be OFF. Time elapsed since ON is {}.".format(act, delta))

                    else:
                        print("Actuator {} OK it is ON. Time elapsed since lastcheck is {}.".format(act, delta))

                sleep(0.5)
                
    def control_on_off_actuators(self):


        for act in self.onoff_actuators:
            
            #went beyond the end time
            if self.current_time > self.actuators[act]["endtime"]:
                self.actuators[act]["exec"].value(0)
                print("It is too late {} Actuator {} should be OFF".format(self.current_time, act))
                

            #is too early and is not time to start
            elif self.current_time < self.actuators[act]["starttime"]:
                self.actuators[act]["exec"].value(0)
                print("It is too early {} Actuator {} should be OFF".format(self.current_time, act))
                

            #if it's on time to start then turn ir on
            else: 
                self.actuators[act]["exec"].value(1)
                print("Right on time! {} Actuator {} should be ON".format(self.current_time, act))
                
            sleep(0.5)
 
    def loop(self):

        try:
            self._loop()

        except:
            #turn off all the actuators
            self.act_module.startup_off()
            sleep(1)

            #reboots in order to reestablish wifi connection
            machine.reset()


    def _loop(self):

        last = time.ticks_ms()
        check_every_n_minutes = 0.5
        check_every_n_seconds = check_every_n_minutes * 60 * 1000


        # Main loop that runs indefinitely
        while True:

            # Current time in milliseconds
            now = time.ticks_ms()

            # Check if n minutes have elapsed since the last task execution
            if (time.ticks_diff(now, last) >= check_every_n_seconds) or (self.boot):

                #update time 
                self.current_time = Time(*get_current_time())
                print("curent time {}".format(self.current_time))
                sleep(0.1)

                print("handling on/off actuators...")
                self.control_on_off_actuators()
                print("\n")

                print("handling timed actuators...")
                self.control_timed_actuators()

                print("handling sensors...")
                self.measure()

                # Update the last execution time
                last = now
                self.boot = False

                print("Done!")
                print("\n")

            # Wait for a short amount of time before checking the time again
            sleep(2)


