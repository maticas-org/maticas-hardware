import scheduler
import initialize_actuators as acts

module = acts.mod
sch    = scheduler.Scheduler(module = module)

sch.loop()

