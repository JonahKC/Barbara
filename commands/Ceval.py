import re
import os
import discord

async def main(message, prefix, client):
	permitted_users = [738843304057372702, 797282028344573992]
	if message.content.startswith(f"{prefix}eval") and message.author.id in permitted_users:
		msg_content = message.content[5:]
		try:
			await eval(msg_content, {"message": message, "client": client, "prefix": prefix, "re": re,"os": os, "discord": discord})
		except Exception as e:
			await message.channel.send(e)