from utils.mqtt_wrapper import MqttConnectionWrapper

#connects to mqtt broker
mqtt_module = MqttConnectionWrapper(config_file = config_file)
#mqtt_module.mqtt_connect()

#mqtt_module.log("initializing actuators and sensors modules...")

import scheduler
import modules.initialize_modules as mods

act_module = mods.act_mod
act_module.startup_off()
sen_module = mods.sen_mod

#mqtt_module.log("Building scheduler...")

sch = scheduler.Scheduler(act_module = act_module,
                          sen_module = sen_module,
                          mqtt_module = mqtt_module)

sch.loop()
