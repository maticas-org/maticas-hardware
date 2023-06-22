import scheduler
import modules.initialize_modules as mods

act_module = mods.act_mod
act_module.startup_off()

sen_module = mods.sen_mod

sch = scheduler.Scheduler(act_module = act_module, sen_module = sen_module)
sch.loop()








