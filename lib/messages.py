#import heapq
import random

MESSAGE_PATHS = {
  "botwinkle": "./resources/botwinkle_sec rets.txt",
  "jokesonyoubot": "./resources/jokes_on_you_bot_secrets.txt",
  "normal": "./resources/secrets.txt",
  "normal (can be normal, jokesonyoubot, or botwinkle)": "./resources/secrets.txt",
	"pickup": "./resources/pickups.txt"
}

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