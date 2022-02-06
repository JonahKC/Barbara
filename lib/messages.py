import random, os, discord
import config.config as config
import discord.ext.commands as commands

MESSAGE_PATHS = {
  "botwinkle": "./resources/botwinkle_sec rets.txt",
  "jokesonyoubot": "./resources/jokes_on_you_bot_secrets.txt",
  "normal": "./resources/secrets.txt",
  "normal (can be normal, jokesonyoubot, or botwinkle)": "./resources/secrets.txt",
}

async def formatString(string: str, ctx: commands.Context):
  """Formats a string by replacing {author} with the author's name, and {prefix} with the prefix of the command, and making \\n a real newline"""
  
  # Get the author's server name
  name = ctx.author.display_name

  # Replace {author} with the author's name
  string = string.replace(r'{author}', name)

  # Replace \\n with \n
  string = string.replace(r'\n', '\n')

  # Replace {prefix} with the server-specific prefix of the command
  string = string.replace('{prefix}', config.read(ctx.guild.id, "prefix"))
  return string

def shuffle_secrets(id: int=1):
  shuffledSecretsRaw = open(f'./temp/shuffled/shuffled-secrets-{id}.txt', 'w')
  secretsRaw = open(MESSAGE_PATHS[config.read(id, "flavor-of-secrets")], 'r')
  secretLines = secretsRaw.readlines()
  random.shuffle(secretLines)
  shuffledSecretsRaw.write(''.join(secretLines)) # instead of writelines so a newline isn't appended to the end
  secretsRaw.close()
  shuffledSecretsRaw.close()

def reset_secrets(ctx):
  config.write(ctx.guild.id, 'secret-internal', 0)
  shuffle_secrets(ctx.guild.id)
  with open(f'./temp/shuffled/shuffled-secrets-{ctx.guild.id}.txt', 'r') as f:
    return f.readline()

def shuffle_pickups(id: int=1):
  """Shuffles the order of the pickup lines (so there aren't ever repeats)"""

  # Get the server-specific pickup line file
  shuffledPickupsRaw = open(f'./temp/shuffled/shuffled-pickups-{id}.txt', 'w')

  # Get the original pickup line list
  pickupsRaw = open('./resources/pickups.txt', 'r')

  # Turn the pickup line list into an array
  pickupLines = pickupsRaw.readlines()
  
  # Shuffle the pickup line list
  random.shuffle(pickupLines)

  # Write the shuffled pickup line list back to the file
  shuffledPickupsRaw.write(''.join(pickupLines))
  pickupsRaw.close()
  shuffledPickupsRaw.close()

def reset_pickups(ctx):
  """Resets the server-specific pickup line file and shuffles the array, then returns the first pickup line"""

  # Reset the server-specific pickup line index
  config.write(ctx.guild.id, 'pickup-internal', 0)

  # Shuffle the pickup lines
  shuffle_pickups(ctx.guild.id)

  with open(f'./temp/shuffled/shuffled-pickups-{ctx.guild.id}.txt', 'r') as f:
    
    # Return the first pickup line
    return f.readline()

def shuffle_breakups(id: int=1):
  shuffledBreakupsRaw = open(f'./temp/shuffled/shuffled-breakups-{id}.txt', 'w')
  breakupsRaw = open('./resources/breakups.txt', 'r')
  breakupLines = breakupsRaw.readlines()
  random.shuffle(breakupLines)
  shuffledBreakupsRaw.writelines(''.join(breakupLines))
  breakupsRaw.close()
  shuffledBreakupsRaw.close()

def reset_breakups(ctx):
  config.write(ctx.guild.id, 'breakup-internal', 0)
  shuffle_breakups(ctx.guild.id)
  with open(f'./temp/shuffled/shuffled-breakups-{ctx.guild.id}.txt', 'r') as f:
    return f.readline()

def iterated_breakup(ctx):
  if isinstance(ctx.channel, discord.channel.DMChannel):
    return "Sorry, breakup lines are not supported in DM conversation."
  breakupIndex = config.read(ctx.guild.id, 'breakup-internal')
  result = "`INTERNAL_BREAKUP_ERROR (messages.py)`"
  if not os.path.exists(f'./temp/shuffled/shuffled-breakups-{ctx.guild.id}.txt'):
    with open(f'./temp/shuffled/shuffled-breakups-{ctx.guild.id}.txt', 'w'):
      pass
    reset_breakups(ctx)
  with open(f'./temp/shuffled/shuffled-breakups-{ctx.guild.id}.txt', 'r') as f:
    breakups = f.readlines()
    if(breakupIndex < len(breakups) - 2): # f.writelines appends a \n to the end, so -2 prevents that from getting sent
      result = breakups[breakupIndex]
  config.write(ctx.guild.id, 'breakup-internal', breakupIndex + 1)
  if(breakupIndex >= len(breakups) - 1):
    return reset_breakups(ctx)
  return result

def iterated_pickup(ctx):
  """Iterates through the pickup lines, returning the next one in the randomized server-specific pickup line file"""

  # DMs don't have their own pickup line file, so send a message to the author telling them to run the command in a server
  if isinstance(ctx.channel, discord.channel.DMChannel):
    return "Sorry, pickup lines are not supported in DM conversation."

  # Get the server-specific pickup line index
  pickupIndex = config.read(ctx.guild.id, 'pickup-internal')

  # If this result doesn't change, then the we've run into a weird bug that should not ever happen
  result = "`INTERNAL_PICKUP_ERROR (messages.py)`"

  # If the server-specific pickup line file doesn't exist, create it and shuffle the pickups into it
  if not os.path.exists(f'./temp/shuffled/shuffled-pickups-{ctx.guild.id}.txt'):
    with open(f'./temp/shuffled/shuffled-pickups-{ctx.guild.id}.txt', 'w'):
      pass
    reset_pickups(ctx)

  # Get the server-specific pickup line file
  with open(f'./temp/shuffled/shuffled-pickups-{ctx.guild.id}.txt', 'r') as f:

    # Get the pickup line list as an array
    pickups = f.readlines()

    # if the index is NOT at the end of the list, reset it to 0
    if(pickupIndex < len(pickups) - 2):
      result = pickups[pickupIndex]

  # Update the server-specific pickup line index
  config.write(ctx.guild.id, 'pickup-internal', pickupIndex + 1)

  # If the index is at the end of the list
  if(pickupIndex >= len(pickups) - 1):

    # Reset the server-specific pickup line index and shuffle the pickups
    return reset_pickups(ctx)

  return result

def iterated_secret(ctx):
  if isinstance(ctx.channel, discord.channel.DMChannel):
    return "Sorry, secrets are not supported in DM conversation."
  secretIndex = config.read(ctx.guild.id, 'secret-internal')
  result = "`INTERNAL_SECRET_ERROR (messages.py)`"
  if not os.path.exists(f'./temp/shuffled/shuffled-secrets-{ctx.guild.id}.txt'):
    with open(f'./temp/shuffled/shuffled-secrets-{ctx.guild.id}.txt', 'w'):
      pass
    reset_secrets(ctx)
  with open(f'./temp/shuffled/shuffled-secrets-{ctx.guild.id}.txt', 'r') as f:
    secrets = f.readlines()
    if(secretIndex < len(secrets) - 2):
      result = secrets[secretIndex]
  config.write(ctx.guild.id, 'secret-internal', secretIndex + 1)
  if(secretIndex >= len(secrets) - 1):
    return reset_secrets(ctx)
  return result

# Converts flavorOfSecret config value to a filepath to the secret's location
def flavorOfSecret(flavorOfSecret):
  global MESSAGE_PATHS
  if MESSAGE_PATHS[flavorOfSecret] is None:
    return MESSAGE_PATHS["normal"]
  return MESSAGE_PATHS[flavorOfSecret]