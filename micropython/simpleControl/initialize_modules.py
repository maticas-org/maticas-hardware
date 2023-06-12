from time               import sleep
from ds18x20            import DS18X20
from onewire            import OneWire
from machine            import Pin, I2C, ADC
from actuators_module   import ActuatorsModule
from sensors_module     import SensorsModule

#--------------------------------------------------------------#
#                       ACTUATORS MODULE
#--------------------------------------------------------------#

act_mod = ActuatorsModule(config_file = "./config.json")

act_mod.add(actuator = "fan",           pin = Pin(33, Pin.OUT))
act_mod.add(actuator = "lights",        pin = Pin(13, Pin.OUT))
act_mod.add(actuator = "water pump",    pin = Pin(27, Pin.OUT))
act_mod.add(actuator = "water oxygen",  pin = Pin(26, Pin.OUT))
act_mod.add(actuator = "recirculation", pin = Pin(14, Pin.OUT))

#--------------------------------------------------------------#
#                       SENSORS MODULE
#--------------------------------------------------------------#

sen_mod = SensorsModule(config_file = "./config.json")

# Initiate ec sensor which comes from an analog reading and build
# its measure function
ec_sensor = Pin(34)
ec_sensor.atten(ADC.ATTN_11DB)

def measure_ec(nsamples = 5):
    measurements = []

    for sample in range(nsamples):
        measurements.append(ec_sensor.read())
        sleep(5)

    return sum(measurements)/len(measurements)


# Initiate DS18B20 sensor and build its measure function
wtemp_sensor = DS18X20(OneWire(Pin(25)))
roms = ds_sensor.scan()
print('Found DS devices: ', roms)

def measure_wtemp(nsamples = 5):
    measurements = []

    for sample in range(nsamples):
        for rom in roms:
            wtemp_sensor.convert_temp()
            sleep(1)
            measurements.append(wtemp_sensor.read_temp(rom))

    return sum(measurements)/len(measurements)


sen_mod.add(sensorName = "water temperature", measure_wtemp)
sen_mod.add(sensorName = "electroconductivity", measure_ec)



