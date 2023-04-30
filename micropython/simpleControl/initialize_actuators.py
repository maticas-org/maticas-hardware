from machine import Pin, I2C, ADC
from module  import Module
from json    import load

mod = Module(config_file = "./config.json")

mod.add_actuator(actuator = "fan",           pin = Pin(33, Pin.OUT))
mod.add_actuator(actuator = "lights",        pin = Pin(13, Pin.OUT))
mod.add_actuator(actuator = "water pump",    pin = Pin(27, Pin.OUT))
mod.add_actuator(actuator = "water oxygen",  pin = Pin(26, Pin.OUT))
mod.add_actuator(actuator = "recirculation", pin = Pin(14, Pin.OUT))



