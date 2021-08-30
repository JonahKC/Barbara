import heapq
from random import random

MESSAGE_PATHS = {
  "botwinkle": "./resources/botwinkle_secrets.txt",
  "jokesonyoubot": "./resources/jokes_on_you_bot_secrets.txt",
  "normal": "./resources/secrets.txt",
  "normal (can be normal, jokesonyoubot, or botwinkle)": "./resources/secrets.txt",
	"pickup": "./resources/pickups.txt"
}

def random_message(path, ctx):
  return _get_rand(path,1)[0].replace("{author}", ctx.author.name).replace(r"\n", '\n')

# Converts flavorOfSecret config value to a filepath to the secret's location
def flavorOfSecret(flavorOfSecret):
  global MESSAGE_PATHS
  if MESSAGE_PATHS[flavorOfSecret] is None:
    return MESSAGE_PATHS["normal"]
  return MESSAGE_PATHS[flavorOfSecret]

def _get_rand(path,number):
  with open(path) as f:
    return heapq.nlargest(number, f, key=lambda L: random())