import ujson
def update_json_file(filepath:str,fiedldname:str,value:str)->None:
	with open(filepath,"r")as f:
		data=ujson.load(f)
		data[fiedldname]=value
	with open(filepath,"w")as f:
		ujson.dump(data,f)