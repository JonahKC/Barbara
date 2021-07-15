import config.config as config
import commands.admin as admin
import re

async def main(message, prefix, client):
	if message.content.startswith(f"{prefix}config"):
		if admin.perms(message.guild.id,message.author):
			content = message.content.split(" ")
			if content[1] == "read":
				if len(content) == 2:
					conf = config.get(message.guild.id)
					conf = re.sub('<@([&!](\d+))>', '<\\\\@\\1>', str(conf))
					conf = re.sub('@everyone', '\\\\@ everyone', str(conf))
					await message.channel.send(str(conf))
				else:
					await message.channel.send(config.read(message.guild.id,content[2]))
			elif content[1] == "set":
				value =  " ".join(content[3:])
				#if type(bool(value)) == bool: value = bool(value)
				#elif type(float(value)) == float: value = float(value)
				config.write(message.guild.id, content[2], value)
				await message.channel.send("Successfully set config value.")