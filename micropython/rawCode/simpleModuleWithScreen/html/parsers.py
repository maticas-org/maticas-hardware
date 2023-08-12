def parse_request(response):
	ifb"POST /update"in response:
		return parse_update_response(response)
	else:
		return None
def parse_update_response(response):
	response_str=response.decode("utf-8")
	start_idx=response_str.find("nombre-actuador=")
	end_idx=response_str.find("&",start_idx)
	nombre_actuador=response_str[start_idx+len("nombre-actuador="):end_idx]
	start_idx=response_str.find("hora-inicio=")
	end_idx=response_str.find("&",start_idx)
	hora_inicio=response_str[start_idx+len("hora-inicio="):end_idx]
	start_idx=response_str.find("hora-fin=")
	end_idx=response_str.find("&",start_idx)
	hora_fin=response_str[start_idx+len("hora-fin="):end_idx]
	start_idx=response_str.find("temporizado=")
	end_idx=response_str.find("&",start_idx)
	temporizado=response_str[start_idx+len("temporizado="):end_idx]
	start_idx=response_str.find("tiempo-encendido=")
	end_idx=response_str.find("&",start_idx)
	tiempo_encendido=response_str[start_idx+len("tiempo-encendido="):end_idx]
	start_idx=response_str.find("tiempo-apagado=")
	end_idx=response_str.find("'",start_idx)
	tiempo_apagado=response_str[start_idx+len("tiempo-apagado="):end_idx]
	return {"nombre_actuador":nombre_actuador,"hora_inicio":hora_inicio,"hora_fin":hora_fin,"temporizado":temporizado,"tiempo_encendido":tiempo_encendido,"tiempo_apagado":tiempo_apagado}