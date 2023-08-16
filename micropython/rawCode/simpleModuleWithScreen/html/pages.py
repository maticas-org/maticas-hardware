update_config = """<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <link href="https://templatemo.com/tm-style-20210719c.css" rel="stylesheet"> <title>Maticas linea decoración - Modulo 0</title> </head> <body> <div class="form-container"><h1>Maticas linea decoración</h1><h3>Modulo 0</h3><hr><form action="/update" method="post"><table><tr><td><label for="nombre-actuador">Nombre de actuador</label><input type="text" id="nombre-actuador" name="name"></td></tr><tr><td><label for="hora-inicio">Hora de inicio</label><input type="time" step="1" id="hora-inicio" name="starttime"></td></tr><tr><td><label for="hora-fin">Hora de fin</label><input type="time" step="1" id="hora-fin" name="endtime"></td></tr><tr><td><label for="tipo-actuador">Tipo de actuador</label><select id="tipo-actuador" name="type" onchange="toggleTiempoFields()"><option value="timed" selected>Temporizado</option><option value="on/off">On/Off</option></select></td></tr><tr id="minuteson-help-row"><td><br><i>El número de minutos de encendido y apagado debe ser mayor a cero. Se permiten números decimales. Si no se selecciona "Temporizado", la configuración de encendido y apagado se ignorará.</i></td></tr><tr id="minuteson-row"><td><label for="minuteson">¿Cuántos minutos encendido?</label><input type="number" id="minuteson" name="minuteson" min="1.0" step="any"></td></tr><tr id="-row"><td><label for="minutesoff">¿Cuántos minutos apagado?</label><input type="number" id="minutesoff" name="minutesoff" min="1.0" step="any"></td></tr></table><br><input type="submit" value="Guardar"></form></div></body></html>"""

def get_config(config_file: str) -> dict:
    import ujson
    from utils.time_management_module import Time

    with open(config_file, "r") as f:
        config = ujson.load(f)
        config = config["actuators"]["0"]
        config["starttime"] = Time(*config["starttime"])
        config["endtime"] = Time(*config["endtime"])

    return config


def show_config(config_file: str) -> str:

    config = get_config(config_file)
    
    if config["type"] == "timed":
        display = """<div class="container"><p>El actuador <strong>'{name}'</strong> opera desde las <strong>{starttime}</strong> horas del día hasta las <strong>{endtime}</strong> horas del día. Es temporizado, se enciende durante <strong>{minuteson} Minutos</strong> y descansa durante <strong>{minutesoff} Minutos</strong>.</p></div>""".format(**config)
    else:
        display = """<div class="container"><p>El actuador <strong>'{name}'</strong> opera desde las <strong>{starttime}</strong> horas del día hasta las <strong>{endtime}</strong> horas del día. No es temporizado.</p></div>""".format(**config)

    return """<!DOCTYPE html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link href="https://templatemo.com/tm-style-20210719c.css" rel="stylesheet"><style>  body { font-family: Arial, sans-serif; margin: 0;padding: 20px;  }  .container { max-width: 600px; margin: 0 auto; border: 1px solid #ccc; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);  }  .button-container {margin-top: 20px;  }  .update-button {background-color: #007bff; color: #fff; border: none; padding: 10px 20px; border-radius: 5px;cursor: pointer;  }</style><title>Información del módulo</title></head><body>""" + """{}""".format(display) + """<br><br><div style="text-align:center"><button class="update-button" onclick="redirectToUpdateConfig()">Modificar configuración</button></div><script>function redirectToUpdateConfig() {window.location.href = '/updateConfig';}</script></body></html>"""

