from machine import Pin
from json import load
from utils.time_management_module import*
class ActuatorsModule():
	def __init__(self,config_file:str):
		with open(config_file)as f:
			self.config=load(f)
		self.actuators=self.config["actuators"]
		self.timed_actuators=[]
		self.onoff_actuators=[]
		self.default_init()
	def default_init(self)->None:
		for actuatorName in self.actuators.keys():
			self.actuators[actuatorName]["exec"]=None
			self.actuators[actuatorName]["status"]=False
			self.actuators[actuatorName]["lastmodified"]=Time(*self.actuators[actuatorName]["starttime"])-Time(100,0,0)
			self.actuators[actuatorName]["starttime"]=Time(*self.actuators[actuatorName]["starttime"])
			self.actuators[actuatorName]["endtime"]=Time(*self.actuators[actuatorName]["endtime"])
		for actuatorName in self.actuators.keys():
			if self.actuators[actuatorName]["type"]=='timed':
				self.timed_actuators.append(actuatorName)
			elif self.actuators[actuatorName]["type"]=='on/off':
				self.onoff_actuators.append(actuatorName)
	def startup_off(self)->None:
		print("Starting up actuators...")
		for actuatorName in self.actuators.keys():
			if self.actuators[actuatorName]["exec"]!=None:
				self.actuators[actuatorName]["exec"].value(0)
		print("Done! they are all OFF.\n")
	def check(self)->None:
		print("Checking actuators...")
		for actuatorName in self.actuators.keys():
			if None==self.actuators[actuatorName]["exec"]:
				print("actuator \"{}\" has no candidate for answering a call".format(actuatorName))
		print("Done!\n")
	def add(self,actuator:str,pin:Pin)->int:
		if actuator not in self.actuators.keys():
			print("this actuator does not exist in the ACTUATORS field. Consider adding it in the file './config.json'.")
			return -1
		self.actuators[actuator]["exec"]=pin
		print("{} added.".format(actuator))
		return 0