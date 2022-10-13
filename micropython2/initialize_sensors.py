# sources: https://randomnerdtutorials.com/micropython-bme280-esp32-esp8266/
# sources: https://github.com/RuiSantosdotme/ESP-MicroPython/blob/master/code/WiFi/HTTP_Client_IFTTT_BME280/BME280.py

from machine import Pin, I2C
from module import Module

from BME280 import BME280
from bh1750 import BH1750


mod = Module(config_file = "./mqtt_config.json")

scl = Pin(22)
sda = Pin(21)

i2c = I2C(scl = scl,
          sda = sda)

#---------------------------------------------------------------------------------#
try:
    bme = BME280(i2c = i2c)
    mod.add_module_function(alias = "temp",     function = bme.temperature_value)
    mod.add_module_function(alias = "hum",      function = bme.humidity_value)
    mod.add_module_function(alias = "pressure", function = bme.pressure_value)

except:
    print("BME280 sensor not found")

#---------------------------------------------------------------------------------#
try:
    bh  = BH1750(bus = i2c)
    # in case we have to send parameters to the function 
    # we have to create a wraper function to pass it to the add_module_function 
    def luminance_wrapper():
        return bh.luminance(BH1750.ONCE_HIRES_1)

    mod.add_module_function(alias = "lux",  function = luminance_wrapper)

except:
    print("BH1750 sensor not found")









