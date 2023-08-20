from modules.database    import Database

#--------------------------------------------------------------#
#                       DB MODULE
#--------------------------------------------------------------#
config_file = "./utils/config.json"
db_mod = Database(config_file = config_file)

#go and find the id in the config.json, these are the same ids of the sensors
db_mod.add_register("0", max_len=120)
db_mod.add_register("1", max_len=120)