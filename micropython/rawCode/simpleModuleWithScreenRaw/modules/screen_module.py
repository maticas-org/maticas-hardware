import machine
from time import sleep
from dependencies.uQR import QRCode
from dependencies.ssd1306 import SSD1306_I2C
from utils.json_related import*
from utils.internet_connection import*
class ScreenModule():
	def __init__(self,config_file:str,screenwidth:int=128,screenheight:int=64,scl_pin:int=22,sda_pin:int=21):
		with open(config_file)as f:
			config=load(f)
			self.ip=config["ip"]
		self.config_file=config_file
		self.screenwidth=screenwidth
		self.screenheight=screenheight
		self.scl_pin=scl_pin
		self.sda_pin=sda_pin
		self.boot_screen()
		self.qr=QRCode(border=1,box_size=2)
		self.display_boot_screen()
	def boot_screen(self)->None:
		i2c=machine.I2C(scl=machine.Pin(self.scl_pin),sda=machine.Pin(self.sda_pin))
		self.screen=SSD1306_I2C(128,64,i2c,60)
		self.screen.poweron()
	def clear_screen(self)->None:
		self.screen.fill(0)
		self.screen.show()
	def display_boot_screen(self)->None:
		self.screen.fill(1)
		self.screen.text("Bienvenido a",self.screenwidth//8,self.screenheight//8,0)
		sleep(1)
		self.screen.text("Maticas :D",self.screenwidth//4,self.screenheight//2,0)
		self.screen.show()
		sleep(3.5)
	def display_restart_screen(self)->None:
		self.screen.fill(1)
		self.screen.text("Guardando",self.screenwidth//8,self.screenheight//8,0)
		self.screen.text("Cambios...",self.screenwidth//8,self.screenheight//4,0)
		self.screen.show()
		sleep(0.85)
		self.screen.text("Reiniciando...",self.screenwidth//8,3*self.screenheight//4,0)
		self.screen.show()
		sleep(0.85)
	def update_ip(self)->None:
		self.ip=connect2(config_file=self.config_file,doreconnect=False)
		if self.ip==None:
			self.ip="No internet connection"
		update_json_field(self.config_file,"ip",self.ip)
	def display_ip(self)->None:
		self.qr.add_data("http://{}".format(self.ip))
		matrix=self.qr.get_matrix()
		paddingx=int(self.screenwidth/4)
		paddingy=5
		for y in range(len(matrix)*2):
			for x in range(len(matrix[0])*2):
				value= not matrix[int(y/2)][int(x/2)]
				self.screen.pixel(x+paddingx,y+paddingy,value)
		self.screen.show()