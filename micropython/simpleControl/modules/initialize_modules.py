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

act_mod.add(actuator = "fan",           pin = Pin(16, Pin.OUT))
act_mod.add(actuator = "lights",        pin = Pin(17, Pin.OUT))
act_mod.add(actuator = "water pump",    pin = Pin(18, Pin.OUT))
act_mod.add(actuator = "water oxygen",  pin = Pin(19, Pin.OUT))
act_mod.add(actuator = "recirculation", pin = Pin(21, Pin.OUT))
print()

#--------------------------------------------------------------#
#                       SENSORS MODULE
#--------------------------------------------------------------#

sen_mod = SensorsModule(config_file = "./config.json")

# Initiate ec sensor which comes from an analog reading and build
# its measure function
ec_sensor = ADC(Pin(34))
ec_sensor.atten(ADC.ATTN_11DB)

def measure_ec(nsamples = 5)->int:
    measurements = []

    try:
        for sample in range(nsamples):
            measurements.append(ec_sensor.read())
            sleep(5)
    except:
        print("This sensor seems to have a problem. FIX IT")
        return -1

    return sum(measurements)/len(measurements)


# Initiate DS18B20 sensor and build its measure function
wtemp_sensor = DS18X20(OneWire(Pin(25)))
roms = wtemp_sensor.scan()
print('Found DS devices: ', roms)

def measure_wtemp(nsamples = 5)->int:
    measurements = []

    for sample in range(nsamples):
        try:
            for rom in roms:
                wtemp_sensor.convert_temp()
                sleep(1)
                measurements.append(wtemp_sensor.read_temp(rom))
        except:
            print("This sensor seems to have a problem. FIX IT")
            return -1

    return sum(measurements)/len(measurements)


sen_mod.add(sensorName = "water temperature",   fn = measure_wtemp)
sen_mod.add(sensorName = "electroconductivity", fn = measure_ec)
print()



