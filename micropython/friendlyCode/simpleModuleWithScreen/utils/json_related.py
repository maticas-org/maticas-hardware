import ujson

def update_json_file(filepath: str, fiedldname:str, value: str) -> None: 
    """
        Updates a field in a json file.
        If the field does not exist, it is created.

        Args:
            filepath (str): The path to the json file.
            fieldname (str): The name of the field to update.
            value (str): The value to update the field with.
    """
    with open(filepath, "r") as f:
        data = ujson.load(f)
        data[fiedldname] = value

    with open(filepath, "w") as f:
        ujson.dump(data, f)