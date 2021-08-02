import re
import os
import discord

NAME = "eval"
PERMITTED_USERS = [738843304057372702, 797282028344573992]

async def main(message, prefix, client):
  global PERMITTED_USERS
  if message.content.startswith(f"{prefix}eval") and message.author.id in PERMITTED_USERS:
    msg_content = message.content.replace(f"{prefix}eval", "", 1)
    try:
	    await eval(msg_content, {"message": message, "client": client, "prefix": prefix, "re": re,"os": os, "discord": discord})
    except Exception as e:
	    await message.channel.send(e)