from random import randint
import config.config as config

async def random_message(message_guild_id, messageType):
  if messageType == "pickup":
    with open('./resources/pickups.txt', 'r') as pickups:
      return pickups.readline()[randint(0, len(pickups))]
  elif messageType == "secret":
    flavorOfSecrets = config.read(message_guild_id, "flavorOfSecrets")
    if flavorOfSecrets == "botwinkle":
      with open('./resources/botwinkle_secrets.txt', 'r') as secrets:
        secrets = secrets.readlines()
        return secrets[randint(0, len(secrets))]
    elif flavorOfSecrets == "jokesonyoubot":
      with open('./resources/jokes_on_you_bot_secrets.txt', 'r') as secrets:
        secrets = secrets.readlines()
        return secrets[randint(0, len(secrets))]
    if flavorOfSecrets != "normal" or flavorOfSecrets != "normal (can be normal, jokesonyoubot, or botwinkle)":
        config.write(message_guild_id, "flavorOfSecrets", "normal (can be normal, jokesonyoubot, or botwinkle)")
    with open('./resources/secrets.txt', 'r') as secrets:
      secrets = secrets.readlines()
      return secrets[randint(0, len(secrets))]