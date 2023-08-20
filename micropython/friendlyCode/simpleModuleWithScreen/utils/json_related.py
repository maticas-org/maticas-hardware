import ujson

def update_json_field(filepath: str, fiedldname:str, value: str) -> None: 
    """
    Updates a field in a json file
    """
    with open(filepath, "r") as f:
        data = ujson.load(f)
        data[fiedldname] = value

    with open(filepath, "w") as f:
        ujson.dump(data, f)
    
def update_json_actuator(filepath: str, actuatorId: str, settings: dict) -> None:
    """
    Updates an actuator in a json file
    """
    with open(filepath, "r") as f:
        data = ujson.load(f)
        
        for field in settings.keys():
            data["actuators"][actuatorId][field] = settings[field]

    with open(filepath, "w") as f:
        ujson.dump(data, f)