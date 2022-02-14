"""
API for interacting with server config.
"""

import os
import json

def make_file_if_not_exists(path):
  """
  Make the file if it doesn't exist.
  """  

  # If the guild file doesn't exist
  if not os.path.isfile(path):

    # Create it
    with open(path, 'x'):
      pass
make_file_if_not_exists('./config/default_config.json')
make_file_if_not_exists('./config/global_config.json')
make_file_if_not_exists('./config/backup.json')

# Check if the guilds directory exists (for guild-specific config files)
if not os.path.isdir('./config/guild'):
  os.mkdir('./config/guild')

# To throw a catchable exception
class ConfigException(Exception):
  def __init__(self, *args, **kwargs):
    super(*args, **kwargs)

class OptionNotFoundException(ConfigException):
  def __init__(self, option, *args, **kwargs):
    self.option=option
    super(*args, **kwargs)

  def __repr__(self):
    return f"ERROR: Config value `{self.option}` does not exist."

### Internal Functions

def save(dict, guild_id):
  """
  Saves the config to the guild file for the guild.
  """

  # Open the guild file for that guild
  with open(f'./config/guild/{guild_id}', 'w+') as fp:
    json.dump(dict, fp)


def load(guild_id):
  """
  Loads the guild file for the guild as a JSON object.
  """

  # Convert it to a string (it might be an int)
  guild_id = str(guild_id)

  try:

    # Try to open the guild file for that guild
    with open(f'./config/guild/{guild_id}') as fp:

      # If it exists, return the JSON object
      return json.load(fp)

  # If the guild file doesn't exist set it to the default config
  except FileNotFoundError:
    serverGen(guild_id)
    return load(guild_id)

def load_global(option=None):
  """
  Load the config global on all servers
  """

  # Attempt to open the global config file
  with open('./config/global_config.json') as fp:

    # If you don't specify an option, return the entire JSON object
    if option == None:
      return json.load(fp)
    else:

      # Otherwise, return the value of the specific option
      return json.load(fp)[option]


### External Functions

def write(guild_id, option, value):
  """
  Write a value to a config option for a guild.
  """  

  # Load the guild file for that guild
  conf = load(guild_id)

  # If the option doesn't exist and the default value doesn't exist
  if conf.get(option) == None and default(option) == None:

    # Return an error
    raise OptionNotFoundException(option)

  # Otherwise write the value to the option
  conf[option] = value

  # And save the new config to the file
  save(conf, guild_id)


def read(guild_id, option):
  """
  Read a value from a config option for a guild.
  """  

  # Load the config for that guild
  conf = load(guild_id)

  # If the option doesn't exist and the default value doesn't exist
  if conf.get(option) == None and default(option) == None:

    # Return an error
    raise OptionNotFoundException(option)

  # If just the guild option doesn't exist, and the default value does
  if conf.get(option) == None:

    # Set the option to the default value
    conf[option] = default(option)

    # And save it to the file
    save(conf, guild_id)

    # And then return it
    return conf[option]
  else:

    # Otherwise just return the value
    return conf[option]

def reset(guild_id, option):
  """
  Reset a config option to the default value.
  """  

  # Load the guild file for that guild
  conf = load(guild_id)

  # If the option doesn't exist and the default value doesn't exist
  if conf.get(option) == None and default(option) == None:

    # Return an error
    raise OptionNotFoundException(option)

  # Reset the option to default
  conf[option] = default()

  # Write the new config (with the reset option) to the guild file
  save(conf, guild_id)

def fetch(guild_id, arr):
  """
  Fetch a list of values from a config array for a guild.
  """  

  # Load the guild file for that guild
  conf = load(guild_id)

  # Load the global config file
  global_conf = load_global()

  # If the option doesn't exist and the default value doesn't exist
  if conf.get(arr) == None and default(arr) == None:

    # Return an error
    raise OptionNotFoundException(arr)

  # If just the guild option doesn't exist, and the default value does
  elif conf.get(arr) == None:

    # Set the option to the default value
    conf[arr] = default(arr)

    # And save it to the file
    save(conf, guild_id)
  
  # Return an array with the guild config array and the global config array
  return list(tuple(conf[arr])+tuple(global_conf[arr]))

def append(guild_id, arr, value):
  """
  Append a value to a config array for a guild.
  """  

  # Load the guild file for that guild
  conf = load(guild_id)

  # If the option doesn't exist and the default value doesn't exist
  if conf.get(arr) == None and default(arr) == None:

    # Return an error
    raise OptionNotFoundException(arr)

  # If just the guild option doesn't exist, and the default value does
  elif conf.get(arr) == None:

    # Set the option to the default value
    conf[arr] = default(arr)

    # And save it to the file
    save(conf, guild_id)

  # Get the config array
  val = conf[arr]

  # Append the new value to the array
  val.append(value)

  # Convert it to a set to remove duplicates, then back to a list
  conf[arr] = list(set(val))

  # Write the new config (with the appended value) to the guild file
  save(conf, guild_id)

def remove(guild_id, arr, value):
  """
  Remove a value from a config array for a guild.
  """  

  # Load the guild file for that guild
  conf = load(guild_id)


  # If the option doesn't exist and the default value doesn't exist
  if conf.get(arr) == None and default(arr) == None:

    # Return an error
    raise OptionNotFoundException(arr)

  # If just the guild option doesn't exist, and the default value does
  elif conf.get(arr) == None:

    # Set the option to the default value
    conf[arr] = default(arr)

    # And save it to the file
    save(conf, guild_id)
  
  # Remove the value from the array
  conf[arr].remove(value)

  # Save the new config to the guild file
  save(conf, guild_id)

def get(guild_id):
  """
  Get the entire config for a guild.
  """

  # Load the guild file for that guild as a JSON object
  conf = load(guild_id)

  # Return all of it it
  return conf

def serverGen(guild_id):
  """
  Generate a guildig file from the default config file.
  """

  # Open the default config file
  with open("config/default_config.json") as fp:

    # Load the default config file
    conf = json.load(fp)

    # Write the default config file to the guildig file
    save(conf, guild_id)

def default(option=None):
  """
  Get the default value of a config option, or the entire default config.
  """

  # Open the default config file
  with open("config/default_config.json") as fp:

    # Load the default config file
    data = json.load(fp)

    # If the option is not specified
    if option is None:

      # Return the entire default config
      return data
    try:

      # Otherwise return the default value of the option
      return data[option]

    # If the option doesn't exist
    except KeyError:

      # Return an error
      raise OptionNotFoundException(option)

def backup():
  """
  Backup every guild file into a large json file called backup.json
  """

  # Initialize two empty sets
  backup = {}

  # Loop through every guild file
  for i in os.listdir('./config/guild'):

    # Open it
    with open('./config/guild/'+i) as fp:

      # Add it to the backup object
      backup[i] = json.load(fp)
  
  # Open backup.json for writing
  with open('./config/backup.json', 'w') as fp:

    # Write the entire backup object to it as JSON
    json.dump(backup, fp)

def revert():
  """
  Revert all of the guild files to their previous backup stored in backup.json
  """
  backup = {}

  # Open backup.json
  with open('./config/backup.json') as fp:

    # Load the backup object
    backup = json.load(fp)

  # Loop through every guild in backup.json
  for i in backup:

    # Write each one to the corresponding guild file
    save(backup[i], i)