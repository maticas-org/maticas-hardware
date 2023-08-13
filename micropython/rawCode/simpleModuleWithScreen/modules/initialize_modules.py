from time import sleep
from ds18x20 import DS18X20
from onewire import OneWire
from machine import Pin,I2C,ADC
from modules.actuators_module import ActuatorsModule
from modules.sensors_module import SensorsModule
from modules.screen_module import ScreenModule
from modules.web_module import WebModule
config_file="./utils/config.json"
act_mod=ActuatorsModule(config_file=config_file)
act_mod.add(actuator="0",pin=Pin(16,Pin.OUT))
print()
sen_mod=SensorsModule(config_file=config_file)
print()
screen_mod=ScreenModule(config_file=config_file)
web_mod=WebModule(config_file=config_file)