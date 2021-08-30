import json

def save(dict):
	with open("./config/config.json", "w") as fp:
		json.dump(dict, fp)

def load():
  try:
    with open('./config/config.json') as fp:
      return json.load(fp)
  except json.decoder.JSONDecodeError:
    return default()

def load_global():
	try:
		with open('./config/global_config.json') as fp:
			return json.load(fp)
	except json.decoder.JSONDecodeError:
		return

def write(guild_id, option, value):
  guild_id = str(guild_id)
  conf = load()
  if default(option) == None:
    return f"ERROR: Config value `{option}` does not exist."
  if conf.get(str(guild_id)) != None:
    conf[guild_id][option] = value
  else:
    serverGen(guild_id)
    conf = load()
    conf[guild_id][option] = value
  save(conf)

def read(guild_id, option, isDM=False):
  if not isDM:
    guild_id = str(guild_id)
    conf = load()
    if conf.get(str(guild_id)) != None:
      if conf[str(guild_id)].get(option) == None and default(option) == None:
        return f"ERROR: Config value `{option}` does not exist."
      if conf[str(guild_id)].get(option) == None:
        conf[str(guild_id)][option] = default(option)
        save(conf)
        return conf[str(guild_id)][option]
      else:
        return conf[str(guild_id)][option]
    else:
      serverGen(str(guild_id))
      conf = load()
      return conf[str(guild_id)][option]
  else:
    return default(option)

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
  elif conf[guild_id].get(arr) == None and default(arr) == None:
    return f"ERROR: Config array `{arr}` does not exist."
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
  elif conf[guild_id].get(arr) == None and default(arr) == None:
    return f"ERROR: Config array `{arr}` does not exist."
  elif conf[guild_id].get(arr) == None:
    conf[guild_id][arr] = default(arr)
    save(conf)
    conf = load()
  conf[guild_id][arr].remove(value)
  save(conf)

def get(guild_id):
	guild_id = str(guild_id)
	conf = load()
	return conf[guild_id]

def serverGen(guild_id):
	guild_id = str(guild_id)
	with open("config/default_config.json") as fp:
		conf = load()
		conf[guild_id] = json.load(fp)
		save(conf)

def default(option=None):
  with open("config/default_config.json") as fp:
    data = json.load(fp)
    if option is None:
      return data
    try:
      return data[option]
    except KeyError:
      print("uh oh\n\n\n")
      return None