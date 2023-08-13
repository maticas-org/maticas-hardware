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
		for actuatorId in self.actuators.keys():
			self.actuators[actuatorId]["exec"]=None
			self.actuators[actuatorId]["status"]=False
			self.actuators[actuatorId]["lastmodified"]=Time(*self.actuators[actuatorId]["starttime"])-Time(100,0,0)
			self.actuators[actuatorId]["starttime"]=Time(*self.actuators[actuatorId]["starttime"])
			self.actuators[actuatorId]["endtime"]=Time(*self.actuators[actuatorId]["endtime"])
		for actuatorId in self.actuators.keys():
			if self.actuators[actuatorId]["type"]=='timed':
				self.timed_actuators.append(actuatorId)
			elif self.actuators[actuatorId]["type"]=='on/off':
				self.onoff_actuators.append(actuatorId)
	def startup_off(self)->None:
		print("Starting up actuators...")
		for actuatorId in self.actuators.keys():
			if self.actuators[actuatorId]["exec"]!=None:
				self.actuators[actuatorId]["exec"].value(0)
		print("Done! they are all OFF.\n")
	def check(self)->None:
		print("Checking actuators...")
		for actuatorId in self.actuators.keys():
			if None==self.actuators[actuatorId]["exec"]:
				print("actuator \"{}\" has no candidate for answering a call".format(actuatorId["name"]))
		print("Done!\n")
	def add(self,actuator:str,pin:Pin)->int:
		if actuator not in self.actuators.keys():
			print("this actuator does not exist in the ACTUATORS field. Consider adding it in the file './config.json'.")
			return -1
		self.actuators[actuator]["exec"]=pin
		print("{} added.".format(self.actuators[actuator]["name"]))
		return 0