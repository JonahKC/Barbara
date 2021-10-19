#import heapq
import random
import config.config as config

MESSAGE_PATHS = {
  "botwinkle": "./resources/botwinkle_sec rets.txt",
  "jokesonyoubot": "./resources/jokes_on_you_bot_secrets.txt",
  "normal": "./resources/secrets.txt",
  "normal (can be normal, jokesonyoubot, or botwinkle)": "./resources/secrets.txt",
}

def shuffle_pickups():
  shuffledPickupsRaw = open('./temp/shuffled-pickups.txt', 'w')
  pickupsRaw = open('./resources/pickups.txt', 'r')
  pickupLines = pickupsRaw.readlines()
  random.shuffle(pickupLines)
  shuffledPickupsRaw.writelines(pickupLines)
  pickupsRaw.close()
  shuffledPickupsRaw.close()

def reset_pickups(ctx):
  config.write(ctx.guild.id, 'pickup-internal', 0)
  shuffle_pickups()
  with open('./temp/shuffled-pickups.txt', 'r') as f:
    return f.readline()

def iterated_pickup(ctx):
  pickupIndex = config.read(ctx.guild.id, 'pickup-internal')
  result = "INTERNAL_PICKUP_ERROR (messages.py)"
  with open('./temp/shuffled-pickups.txt', 'r') as f:
    pickups = f.readlines()
    if(pickupIndex < len(pickups) - 1):
      result = pickups[pickupIndex]
      config.write(ctx.guild.id, 'pickup-internal', pickupIndex + 1)
  if(pickupIndex >= len(pickups) - 1):
    return reset_pickups(ctx)
  return result

def random_message(path, ctx):
  return _get_rand(path,1).replace("{author}", ctx.author.name).replace(r"\n", '\n') # for heapq add [0] after _get_rand

# Converts flavorOfSecret config value to a filepath to the secret's location
def flavorOfSecret(flavorOfSecret):
  global MESSAGE_PATHS
  if MESSAGE_PATHS[flavorOfSecret] is None:
    return MESSAGE_PATHS["normal"]
  return MESSAGE_PATHS[flavorOfSecret]

def _get_rand(path,number):
  with open(path) as f:
    return random.choice(f.readlines())
    # Less random but also less memory intensive alternative
		#return heapq.nlargest(number, f, key=lambda L: random.random())