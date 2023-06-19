import time
import machine

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

            if values["status"]:
            
                if delta > values["measure_every_x_time"]:
                    measurement = values["exec"]()
                    print("{} value is: {}".format(sensorName, measurement))

                    self.sensors[sensorName]["lastmeasured"] = self.current_time

                else:
                    print("We don't need the {} measurement yet, delta: {}".format(sensorName, delta))

            else:
                print("Sensor {} is not working...".format(sensorName))


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

        except Exception as e:
            print("An error occurred: {}".format(e))

            #turn off all the actuators
            self.act_module.startup_off()
            sleep(2)

            #reboots in order to reestablish wifi connection
            machine.reset()


    def _loop(self):

        last = time.ticks_ms()

        sync_time_every_x_time      = Time(3, 0, 0)
        time_counter                = Time(0, 0, 0)

        handle_modules_every_x_time  = Time(0, 1, 0)
        handle_modules_every_x_msecs = handle_modules_every_x_time.to_total_seconds()*1000

        # Main loop that runs indefinitely
        while True:

            # Current time in milliseconds
            now = time.ticks_ms()

            # Check if n minutes have elapsed since the last task execution
            if (time.ticks_diff(now, last) >= (handle_modules_every_x_msecs)) or (self.boot):

                #update time, in order to avoid making too many requests to the 
                #server we only do them periodically
                if (self.boot) or (time_counter >= sync_time_every_x_time):
                    self.current_time   = Time(*get_current_time())
                    time_counter        = Time(0, 0, 0)
                    self.boot           = False
                    print("server side time update")

                #the rest of the time we use the local elapsed millies 
                else:
                    self.current_time   += handle_modules_every_x_time
                    time_counter        += handle_modules_every_x_time
                    print("local side time update")


                print("curent time {}\n".format(self.current_time))
                sleep(0.1)

                print("handling on/off actuators...")
                self.control_on_off_actuators()
                print("\n")

                print("handling timed actuators...")
                self.control_timed_actuators()
                print("\n")

                print("handling sensors...")
                self.measure()
                print("\n")

                # Update the last execution time
                last = now

                print("Done!")
                print("\n")

            # Wait for a short amount of time before checking the time again
            sleep(2)


