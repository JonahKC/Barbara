from random import randint
import config.config as config

normal_secrets = ""
jokes_on_you_bot_secrets = ""
botwinkle_secrets = ""
pickups = ""

async def init():
  global normal_secrets, jokes_on_you_bot_secrets, botwinkle_secrets, pickups
  with open('./resources/secrets.txt', 'r') as secrets:
    normal_secrets = secrets.readlines()
  with open('./resources/jokes_on_you_bot_secrets.txt', 'r') as secrets:
    jokes_on_you_bot_secrets = secrets.readlines()
  with open('./resources/botwinkle_secrets.txt', 'r') as secrets:
    botwinkle_secrets = secrets.readlines()
  with open('./resources/pickups.txt', 'r') as pickups_:
    pickups = pickups_.readlines()

async def random_message(message_guild_id, messageType):
  global normal_secrets, jokes_on_you_bot_secrets, botwinkle_secrets, pickups
  if messageType == "pickup":
    return pickups[randint(0, len(pickups))]
  elif messageType == "secret":
    flavorOfSecrets = config.read(message_guild_id, "flavorOfSecrets")
    if flavorOfSecrets == "botwinkle":
      return botwinkle_secrets[randint(0, len(botwinkle_secrets))]
    elif flavorOfSecrets == "jokesonyoubot":
      return jokes_on_you_bot_secrets[randint(0, len(jokes_on_you_bot_secrets))]
    else:
      if flavorOfSecrets != "normal" or flavorOfSecrets != "normal (can be normal, jokesonyoubot, or botwinkle)":
        config.write(message_guild_id, "flavorOfSecrets", "normal (can be normal, jokesonyoubot, or botwinkle)")
    return normal_secrets[randint(0, len(normal_secrets))]
  return "ERROR: Invalid messageType parameter passed to lib.messages.random_message(). Valid types are: [pickup, secret]"