import json, os

def save(dict, guild):
  if guild != None:
    with open('./config/server conf/'+guild, 'w+') as fp:
      json.dump(dict, fp)
#  else:
#	  with open("./config/config.json", "w") as fp:
#		  json.dump(dict, fp)

def load(guild):
  if guild != None:
    try:
      with open('./config/server conf/'+guild) as fp:
        return json.load(fp)
    except FileNotFoundError:
      try:
        with open('./config/config.json') as fp:
          conf = json.load(fp)
          if guild in conf:
            save(conf[guild], guild)
            conf[guild] = "migrated"
            return load(guild)
          else:
            serverGen(guild)
            return load(guild)
      except FileNotFoundError:
        serverGen(guild)
        return load(guild)

  else:
    with open('./config/config.json') as fp:
      return json.load(fp)

def load_global(option=None):
  try:
    with open('./config/global_config.json') as fp:
      if option == None:
        return json.load(fp)
      else:
        return json.load(fp)[option]
  except json.decoder.JSONDecodeError:
    return

def write(guild_id, option, value):
  guild_id = str(guild_id)
  conf = load(guild_id)
  if conf[option] == None and default(option) == None:
    return f"ERROR: Config value `{option}` does not exist."
  conf[option] = value
  save(conf, guild_id)

def read(guild_id, option, isDM=False):
  if not isDM:
    guild_id = str(guild_id)
    conf = load(guild_id)
    if conf.get(option) == None and default(option) == None:
      return f"ERROR: Config value `{option}` does not exist."
    if conf.get(option) == None:
      conf[option] = default(option)
      save(conf, guild_id)
      return conf[option]
    else:
      return conf[option]
  else:
    return default(option)

def reset(guild_id, option):
  guild_id = str(guild_id)
  conf = load(guild_id)
  if conf.get(option) == None and default(option) == None:
    return f"ERROR: Config value `{option}` does not exist."
  conf[option] = default()
  save(conf, guild_id)

def fetch(guild_id, arr):
	guild_id = str(guild_id)
	conf = load(guild_id)
	global_conf = load_global()
	if conf.get(arr) == None:
		conf[arr] = default(arr)
		save(conf, guild_id)
		conf = load(guild_id)
	return list(tuple(conf[arr])+tuple(global_conf[arr]))

def append(guild_id, arr, value):
  guild_id = str(guild_id)
  conf = load(guild_id)
  if conf.get(arr) == None and default(arr) == None:
    return f"ERROR: Config array `{arr}` does not exist."
  elif conf.get(arr) == None:
    conf[arr] = default(arr)
    save(conf, guild_id)
    conf = load(guild_id)
  val = conf[arr]
  val.append(value)
  conf[arr] = list(set(val))
  save(conf, guild_id)

def remove(guild_id, arr, value):
  guild_id = str(guild_id)
  conf = load(guild_id)
  if conf.get(arr) == None and default(arr) == None:
    return f"ERROR: Config array `{arr}` does not exist."
  elif conf.get(arr) == None:
    conf[arr] = default(arr)
    save(conf, guild_id)
    conf = load(guild_id)
  conf[arr].remove(value)
  save(conf, guild_id)

def get(guild_id):
	guild_id = str(guild_id)
	conf = load(guild_id)
	return conf

def serverGen(guild_id):
	guild_id = str(guild_id)
	with open("config/default_config.json") as fp:
		conf = json.load(fp)
		save(conf, guild_id)

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

def backup():
  backup = {}
  conf = {}
  with open('./config/config.json') as fp:
    conf = json.load(fp)
  for i in conf:
    backup[i] = load(i)
    conf[i] = "migrated"
  with open('./config/config.json', 'w') as fp:
    json.dump(conf, fp)
  for i in os.listdir('./config/server conf'):
    with open('./config/server conf/'+i) as fp:
      backup[i] = json.load(fp)
  
  with open('./config/backup.json', 'w') as fp:
    json.dump(backup, fp)

def revert():
  backup = {}
  with open('./config/backup.json') as fp:
    backup = json.load(fp)

  for i in backup:
    save(backup[i], i)