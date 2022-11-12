# sources: https://randomnerdtutorials.com/micropython-bme280-esp32-esp8266/
# sources: https://github.com/RuiSantosdotme/ESP-MicroPython/blob/master/code/WiFi/HTTP_Client_IFTTT_BME280/BME280.py

from machine import Pin, I2C, ADC
from module import Module

from BME280 import BME280
from bh1750 import BH1750


mod = Module(config_file = "./mqtt_config.json")

panel_voltage = ADC(Pin(34))
battery_voltage = ADC(Pin(35))

#full voltage range to measure, up to 3.3V
panel_voltage.atten(ADC.ATTN_11DB)
battery_voltage.atten(ADC.ATTN_11DB)

#set the width of the ADC reading to 12 bits, up to 4095
panel_voltage.width(ADC.WIDTH_12BIT)
battery_voltage.width(ADC.WIDTH_12BIT)


scl = Pin(22)
sda = Pin(21)

i2c = I2C(scl = scl,
          sda = sda)

#here is some data about the voltage sensor: https://www.youtube.com/watch?v=NNUBWpSgSYM
# some constants of the sensor which takes the voltage measurements
R1 = 30000;
R2 = 7500;
correction_factor = 0.65

# some battery constants to calculate the battery level
max_battery_voltage = 3.7
max_panel_voltage = 16.0

#---------------------------------------------------------------------------------#
def from_analog_read_to_voltage(analog_read: int, max_voltage = 3.3, resolution = 4095):
    
    vout = (analog_read * max_voltage)/resolution
    vin  = vout/(R2/(R1+R2))
    return vin + correction_factor


def read_panel_voltage(nsamples = 5):

    analog_read = 0
    for i in range(nsamples):
        analog_read += panel_voltage.read()
        sleep(0.1)

    return "{:.3f}".format(from_analog_read_to_voltage(analog_read/nsamples))

def read_battery_voltage(nsamples = 5):

    analog_read = 0
    for i in range(nsamples):
        analog_read += battery_voltage.read()
        sleep(0.1)

    return "{:.3f}".format(from_analog_read_to_voltage(analog_read/nsamples))

try:
    mod.add_module_function(alias = "panel_voltage",  function = read_panel_voltage)
    mod.add_module_function(alias = "battery_energy", function = read_battery_voltage)
except:
    print("Error with panel voltage sensor or battery energy sensor.")

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









