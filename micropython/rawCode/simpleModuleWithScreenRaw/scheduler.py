import gc
from time import sleep,ticks_ms,ticks_diff
from machine import reset
from utils.internet_connection import*
from utils.time_management_module import*
from modules.actuators_module import ActuatorsModule
from modules.sensors_module import SensorsModule
from modules.screen_module import ScreenModule
from modules.web_module import WebModule
class Scheduler():
	def __init__(self,act_module:ActuatorsModule,sen_module:SensorsModule,screen_module:ScreenModule,web_module:WebModule):
		self.act_module=act_module
		self.sen_module=sen_module
		self.screen_module=screen_module
		self.web_module=web_module
		self.actuators=act_module.actuators
		self.sensors=sen_module.sensors
		self.boot=True
		self.timed_actuators=act_module.timed_actuators
		self.onoff_actuators=act_module.onoff_actuators
		self.current_time=Time(*get_current_time())
		self.check()
	def check(self):
		self.act_module.check()
		self.sen_module.check()
	def measure(self):
		for sensorName,values in self.sensors.items():
			delta=self.current_time-values["lastmeasured"]
			if values["status"]:
				if delta>values["measure_every_x_time"]:
					measurement=values["exec"]()
					print("{} value is: {}".format(sensorName,measurement))
					self.sensors[sensorName]["lastmeasured"]=self.current_time
				else:
					print("We don't need the {} measurement yet, delta: {}".format(sensorName,delta))
			else:
				print("Sensor {} is not working...".format(sensorName))
	def control_timed_actuators(self):
		for act in self.timed_actuators:
			if self.actuators[act]["exec"]==None:
				print("actuator {} has no exec object to call".format(act))
				continue
			if self.current_time>self.actuators[act]["endtime"]:
				self.actuators[act]["exec"].value(0)
			elif self.current_time<self.actuators[act]["starttime"]:
				self.actuators[act]["exec"].value(0)
			else:
				lastmodified=self.actuators[act]["lastmodified"]
				delta=self.current_time-lastmodified
				delta_min=delta.to_total_minutes()
				value=self.actuators[act]["status"]
				if value==0:
					if delta_min>self.actuators[act]["minutesoff"]:
						self.actuators[act]["exec"].value(1)
						self.actuators[act]["status"]=1
						self.actuators[act]["lastmodified"]=self.current_time
						print("Actuator {} should be ON. Time elapsed since OFF is {}.".format(act,delta))
					else:
						print("Actuator {} OK it is OFF. Time elapsed since lastcheck is {}.".format(act,delta))
				elif value==1:
					if delta_min>self.actuators[act]["minuteson"]:
						self.actuators[act]["exec"].value(0)
						self.actuators[act]["status"]=0
						self.actuators[act]["lastmodified"]=self.current_time
						print("Actuator {} should be OFF. Time elapsed since ON is {}.".format(act,delta))
					else:
						print("Actuator {} OK it is ON. Time elapsed since lastcheck is {}.".format(act,delta))
				sleep(0.5)
	def control_on_off_actuators(self):
		for act in self.onoff_actuators:
			if self.actuators[act]["exec"]==None:
				print("actuator {} has no exec object to call".format(act))
				continue
			if self.current_time>self.actuators[act]["endtime"]:
				self.actuators[act]["exec"].value(0)
				print("It is too late {} Actuator {} should be OFF".format(self.current_time,act))
			elif self.current_time<self.actuators[act]["starttime"]:
				self.actuators[act]["exec"].value(0)
				print("It is too early {} Actuator {} should be OFF".format(self.current_time,act))
			else:
				self.actuators[act]["exec"].value(1)
				print("Right on time! {} Actuator {} should be ON".format(self.current_time,act))
			sleep(0.5)
	def display_ip(self):
		self.screen_module.update_ip()
		self.screen_module.clear_screen()
		self.screen_module.display_ip()
	def loop(self,log=True):
		self._loop(log=log)
	def _loop(self,log=True):
		last=ticks_ms()
		sync_time_every_x_time=Time(0,0,60)
		sync_time_count=Time(0,0,0)
		update_screen_every_x_time=Time(1,0,0)
		update_screen_count=update_screen_every_x_time
		handle_modules_every_x_time=Time(0,0,30)
		handle_modules_every_x_msecs=handle_modules_every_x_time.to_total_seconds()*1000
		while True:
			current_use_of_memory=gc.mem_alloc()
			available_memory=gc.mem_free()
			percentage=(current_use_of_memory/(current_use_of_memory+available_memory))*100
			print("Memory usage: {}%".format(percentage))
			if gc.mem_free()<102000:
				gc.collect()
			now=ticks_ms()
			if(ticks_diff(now,last)>=(handle_modules_every_x_msecs)) or (self.boot):
				if(self.boot) or (sync_time_count>=sync_time_every_x_time):
					self.current_time=Time(*get_current_time())
					sync_time_count=Time(0,0,0)
					self.boot=False
					print("server side time update")
				else:
					self.current_time+=handle_modules_every_x_time
					sync_time_count+=handle_modules_every_x_time
					print("local side time update")
				if update_screen_count>=update_screen_every_x_time:
					self.display_ip()
					update_screen_count=Time(0,0,0)
					print("screen update")
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
				last=now
				print("Done!\n")
			self.web_module.serve()
			sleep(0.1)
			if self.web_module.need_to_update:
				self.screen_module.display_restart_screen()
				reset()
			gc.collect()