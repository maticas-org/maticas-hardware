import gc
from time import sleep, ticks_ms, ticks_diff
from machine import reset

from utils.internet_connection import *
from utils.time_management_module import *
from modules.actuators_module import ActuatorsModule
from modules.sensors_module import SensorsModule
from modules.screen_module import ScreenModule
from modules.web_module import WebModule

class Scheduler():

    def __init__(self,
                 act_module: ActuatorsModule,
                 sen_module: SensorsModule,
                 screen_module: ScreenModule, 
                 web_module: WebModule):

        self.act_module = act_module
        self.sen_module = sen_module
        self.screen_module = screen_module
        self.web_module = web_module

        self.actuators = act_module.actuators
        self.sensors = sen_module.sensors
        self.boot = True
        self.current_time = Time(*get_current_time())
        
        self.sync_time_every_some_time = Time(1, 30, 0) #sync time with server timing
        self.time_away_count = Time(0, 0, 0) #counter of how much time, the module has been without updating
        self.handle_modules_every_some_time = Time(0, 0, 30) #used for avoiding doing too many unnesary checks on most modules

    def clean_memory(self) -> None:
        if self.get_memory_use_percentage() >= 60:
            gc.collect()

    def get_memory_use_percentage(self) -> float:
        current_use_of_memory = gc.mem_alloc()
        available_memory = gc.mem_free()
        percentage = (current_use_of_memory / (current_use_of_memory + available_memory)) * 100

        print("Memory usage: {}%".format(percentage))
        return percentage

    def update_time(self) -> None:
        # update time, in order to avoid making too many requests to the
        # server we only do them periodically
        if (self.boot) or (self.time_away_count >= self.sync_time_every_some_time):
            self.current_time = Time(*get_current_time())
            self.time_away_count = Time(0, 0, 0)
            self.boot = False

            print("server side time update.")

        # the rest of the time we use the local elapsed millies
        else:
            self.current_time += self.handle_modules_every_some_time
            self.time_away_count += self.handle_modules_every_some_time

            print("local side time update.")


    def loop(self, log = True):
        self._loop(log = log)

    def _loop(self, log = True):

        last = ticks_ms()

        # Time to handle modules
        handle_modules_every_some_msecs = self.handle_modules_every_some_time.to_total_seconds() * 1000

        # Main loop that runs indefinitely
        while True:

            # Current time in milliseconds and current memory use
            now = ticks_ms()

            # Check if n minutes have elapsed since the last task execution
            if (ticks_diff(now, last) >= (handle_modules_every_some_msecs)) or (self.boot):

                print("handling time...")
                self.update_time()
                print("curent time {}\n".format(self.current_time))
                self.clean_memory()
                sleep(0.1)

                print("handling screen...")
                self.screen_module.display_ip(self.current_time)
                self.clean_memory()
                print("\n")

                print("handling on/off actuators...")
                print("handling timed actuators...")
                self.act_module.timed_control(self.current_time)
                self.clean_memory()
                print("\n")

                print("handling sensors...")
                self.sen_module.timed_measurement(self.current_time)
                self.clean_memory()
                print("\n")

                # Update the last execution time
                last = now
                print("Done!\n")

            self.web_module.serve()
            self.clean_memory()
            sleep(0.1)

            if self.web_module.need_to_update:
                self.screen_module.display_need_to_update_screen()
                reset()
            
            if self.get_memory_use_percentage() >= 95:
                self.clean_memory()
                self.screen_module.display_overflow_screen()
                reset()