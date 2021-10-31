#import heapq
import random, os
import config.config as config

MESSAGE_PATHS = {
  "botwinkle": "./resources/botwinkle_sec rets.txt",
  "jokesonyoubot": "./resources/jokes_on_you_bot_secrets.txt",
  "normal": "./resources/secrets.txt",
  "normal (can be normal, jokesonyoubot, or botwinkle)": "./resources/secrets.txt",
}

def shuffle_pickups(id: int=1):
  shuffledPickupsRaw = open(f'./temp/shuffled/shuffled-pickups-{id}.txt', 'w')
  pickupsRaw = open('./resources/pickups.txt', 'r')
  pickupLines = pickupsRaw.readlines()
  random.shuffle(pickupLines)
  shuffledPickupsRaw.writelines(pickupLines)
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
  shuffledBreakupsRaw.writelines(breakupLines)
  breakupsRaw.close()
  shuffledBreakupsRaw.close()

def reset_breakups(ctx):
  config.write(ctx.guild.id, 'breakup-internal', 0)
  shuffle_breakups(ctx.guild.id)
  with open(f'./temp/shuffled/shuffled-breakups-{ctx.guild.id}.txt', 'r') as f:
    return f.readline()

def iterated_breakup(ctx):
  breakupIndex = config.read(ctx.guild.id, 'breakup-internal')
  result = "`INTERNAL_BREAKUP_ERROR (messages.py)`"
  if not os.path.exists(f'./temp/shuffled/shuffled-breakups-{ctx.guild.id}.txt'):
    open(f'./temp/shuffled/shuffled-breakups-{ctx.guild.id}.txt', 'x').close()
    reset_breakups(ctx)
  with open(f'./temp/shuffled/shuffled-breakups-{ctx.guild.id}.txt', 'r') as f:
    breakups = f.readlines()
    if(breakupIndex < len(breakups) - 2): # f.writelines appends a \n to the end, so -2 prevents that from getting sent
      result = breakups[breakupIndex]
  config.write(ctx.guild.id, 'breakup-internal', breakupIndex + 1)
  if(breakupIndex >= len(breakups) - 1):
    return reset_breakups(ctx)
  return result.replace(r'{author}', ctx.author.display_name).replace(r'\n', '\n')

def iterated_pickup(ctx):
  pickupIndex = config.read(ctx.guild.id, 'pickup-internal')
  result = "`INTERNAL_PICKUP_ERROR (messages.py)`"
  if not os.path.exists(f'./temp/shuffled/shuffled-pickups-{ctx.guild.id}.txt'):
    open(f'./temp/shuffled/shuffled-pickups-{ctx.guild.id}.txt', 'x').close()
    reset_pickups(ctx)
  with open(f'./temp/shuffled/shuffled-pickups-{ctx.guild.id}.txt', 'r') as f:
    pickups = f.readlines()
    if(pickupIndex < len(pickups) - 2):
      result = pickups[pickupIndex]
  config.write(ctx.guild.id, 'pickup-internal', pickupIndex + 1)
  if(pickupIndex >= len(pickups) - 1):
    return reset_pickups(ctx)
  return result.replace(r'{author}', ctx.author.display_name).replace(r'\n', '\n')

def random_message(path, ctx):
  return _get_rand(path).replace("{author}", ctx.author.display_name).replace(r'\n', '\n').replace(r'{prefix}', config.read(ctx.guild.id, "prefix"))

# Converts flavorOfSecret config value to a filepath to the secret's location
def flavorOfSecret(flavorOfSecret):
  global MESSAGE_PATHS
  if MESSAGE_PATHS[flavorOfSecret] is None:
    return MESSAGE_PATHS["normal"]
  return MESSAGE_PATHS[flavorOfSecret]

def _get_rand(path):
  with open(path) as f:
    return random.choice(f.readlines())
    # Less random but also less memory intensive alternative
		#return heapq.nlargest(1, f, key=lambda L: random.random())[0]