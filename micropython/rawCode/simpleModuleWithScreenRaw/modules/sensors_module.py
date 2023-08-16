from json import load
from utils.time_management_module import*
class SensorsModule():
	def __init__(self,config_file:str):
		with open(config_file)as f:
			self.config=load(f)
		self.sensors=self.config["sensors"]
		self.default_init()
	def default_init(self)->None:
		for sensorId in self.sensors.keys():
			self.sensors[sensorId]["exec"]=None
			self.sensors[sensorId]["status"]=False
			self.sensors[sensorId]["lastmeasured"]=Time(-100,0,0)
			self.sensors[sensorId]["measure_every_x_time"]=Time(*self.sensors[sensorId]["measure_every_x_time"])
	def check(self)->None:
		print("Checking sensors...")
		for sensorId in self.sensors.keys():
			if None==self.sensors[sensorId]["exec"]:
				print("Sensor \"{}\" has no candidate for answering a call.".format(self.sensors[sensorId]["name"]))
			else:
				result=self.sensors[sensorId]["exec"]()
				if result!=-1:
					self.sensors[sensorId]["status"]=True
				else:
					print("Sensor \"{}\" isn't OK.".format(self.sensors[sensorId]["name"]))
		print("Done!\n")
	def add(self,sensorId:str,fn:callable)->int:
		if sensorId not in self.sensors.keys():
			print("this sensor does not exist in the ACTUATORS field. Consider adding it in the file './config.json'.")
			return -1
		self.sensors[sensorId]["exec"]=fn
		print("{} added.".format(self.sensors[sensorId]["name"]))
		return 0