 #import heapq
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
  name = ctx.author.display_name
  string = string.replace(r'{author}', name)
  string = string.replace(r'\n', '\n')
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
  shuffledPickupsRaw = open(f'./temp/shuffled/shuffled-pickups-{id}.txt', 'w')
  pickupsRaw = open('./resources/pickups.txt', 'r')
  pickupLines = pickupsRaw.readlines()
  random.shuffle(pickupLines)
  shuffledPickupsRaw.write(''.join(pickupLines))
  pickupsRaw.close()
  shuffledPickupsRaw.close()

def reset_pickups(ctx):
  config.write(ctx.guild.id, 'pickup-internal', 0)
  shuffle_pickups(ctx.guild.id)
  with open(f'./temp/shuffled/shuffled-pickups-{ctx.guild.id}.txt', 'r') as f:
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
  if isinstance(ctx.channel, discord.channel.DMChannel):
    return "Sorry, pickup lines are not supported in DM conversation."
  pickupIndex = config.read(ctx.guild.id, 'pickup-internal')
  result = "`INTERNAL_PICKUP_ERROR (messages.py)`"
  if not os.path.exists(f'./temp/shuffled/shuffled-pickups-{ctx.guild.id}.txt'):
    with open(f'./temp/shuffled/shuffled-pickups-{ctx.guild.id}.txt', 'w'):
      pass
    reset_pickups(ctx)
  with open(f'./temp/shuffled/shuffled-pickups-{ctx.guild.id}.txt', 'r') as f:
    pickups = f.readlines()
    if(pickupIndex < len(pickups) - 2):
      result = pickups[pickupIndex]
  config.write(ctx.guild.id, 'pickup-internal', pickupIndex + 1)
  if(pickupIndex >= len(pickups) - 1):
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