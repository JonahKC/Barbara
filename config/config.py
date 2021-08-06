import json
import os

secrets = False

def save(dict):
	if (secrets == False):	
		with open("config/config.json", "w") as fp:
			json.dump(dict,fp)
	else:
		os.environ["config"] = json.dumps(dict)
		print(os.environ["config"])

def load():
	try:
		if (secrets == False):
			with open('config/config.json') as fp:
				return json.load(fp)
		else:
			return json.loads(os.environ["config"])
		
	except json.decoder.JSONDecodeError:
		return

def load_global():
	try:
		if (secrets == False):
			with open('config/global_config.json') as fp:
				return json.load(fp)
		else:
			return json.loads(os.environ["global config"])
	except json.decoder.JSONDecodeError:
		return



def write(guild_id, option, value):
	guild_id = str(guild_id)
	conf = load()
	if conf.get(str(guild_id)) != None:
		conf[guild_id][option] = value
	else:
		serverGen(guild_id)
		conf = load()
		conf[guild_id][option] = value
	save(conf)

def read(guild_id, option):
	guild_id = str(guild_id)
	conf = load()
	if conf.get(str(guild_id)) != None:
		if conf[str(guild_id)].get(option) == None:
			conf[str(guild_id)][option] = default(option)
			save(conf)
		return conf[str(guild_id)][option]
	else:
		serverGen(str(guild_id))
		conf = load()
		return conf[str(guild_id)][option]

def fetch(guild_id, arr):
	guild_id = str(guild_id)
	conf = load()
	global_conf = load_global()
	if conf.get(str(guild_id)) == None:
		serverGen(guild_id)
		conf = load()
	elif conf[guild_id].get(arr) == None:
		conf[guild_id][arr] = default(arr)
		save(conf)
		conf = load()
	return list(tuple(conf[guild_id][arr])+tuple(global_conf[arr]))

def append(guild_id, arr, value):
	guild_id = str(guild_id)
	conf = load()
	if conf.get(str(guild_id)) == None:
		serverGen(guild_id)
		conf = load()
	elif conf[guild_id].get(arr) == None:
		conf[guild_id][arr] = default(arr)
		save(conf)
		conf = load()
	val = conf[guild_id][arr]
	val.append(value)
	conf[guild_id][arr] = list(set(val))
	save(conf)

def remove(guild_id, arr, value):
	guild_id = str(guild_id)
	conf = load()
	if conf.get(str(guild_id)) == None:
		serverGen(guild_id)
		conf = load()
	elif conf[guild_id].get(arr) == None:
		conf[guild_id][arr] = default(arr)
		save(conf)
		conf = load()
	conf[guild_id][arr].remove(value)
	save(conf)



def get(guild_id):
	guild_id = str(guild_id)
	conf = load()
	return conf[str(guild_id)]

def serverGen(guild_id):
	guild_id = str(guild_id)
	if (secrets == False):
		with open("config/default_config.json") as fp:
			conf = load()
			conf[guild_id] = json.load(fp)
			save(conf)
	else:
		defaultConf = os.environ["default config"]
		conf = load()
		conf[guild_id] = json.loads(defaultConf)
		save(conf)

def default(option):
	if (secrets == False):
		with open("config/default_config.json") as fp:
			data = json.load(fp)
			return data[option]
	else:
		defaultConf = os.environ["default config"]
		data = json.loads(defaultConf)
		return data[option]