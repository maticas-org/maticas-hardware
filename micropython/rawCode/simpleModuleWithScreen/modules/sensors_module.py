from json import load
from utils.time_management_module import*
class SensorsModule():
	def __init__(self,config_file:str):
		with open(config_file)as f:
			self.config=load(f)
		self.sensors=self.config["sensors"]
		self.default_init()
	def default_init(self)->None:
		for sensorName in self.sensors.keys():
			self.sensors[sensorName]["exec"]=None
			self.sensors[sensorName]["status"]=False
			self.sensors[sensorName]["lastmeasured"]=Time(-100,0,0)
			self.sensors[sensorName]["measure_every_x_time"]=Time(*self.sensors[sensorName]["measure_every_x_time"])
	def check(self)->None:
		print("Checking sensors...")
		for sensorName in self.sensors.keys():
			if None==self.sensors[sensorName]["exec"]:
				print("Sensor \"{}\" has no candidate for answering a call.".format(sensorName))
			else:
				result=self.sensors[sensorName]["exec"]()
				if result!=-1:
					self.sensors[sensorName]["status"]=True
				else:
					print("Sensor \"{}\" isn't OK.".format(sensorName))
		print("Done!\n")
	def add(self,sensorName:str,fn:callable)->int:
		if sensorName not in self.sensors.keys():
			print("this sensor does not exist in the ACTUATORS field. Consider adding it in the file './config.json'.")
			return -1
		self.sensors[sensorName]["exec"]=fn
		print("{} added.".format(sensorName))
		return 0