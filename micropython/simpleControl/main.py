import scheduler
import initialize_actuators as acts

module = acts.mod
module.startup_off()

sch    = scheduler.Scheduler(module = module)
sch.loop()

