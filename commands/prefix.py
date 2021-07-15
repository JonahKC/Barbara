import config.config as config
import commands.admin as admin

async def main(message, prefix, client):
	if message.content.startswith(f"{prefix}prefix"):
		if admin.perms(message.guild.id,message.author):
			content = message.content.split(" ")
			if len(content) > 1:
				config.write(message.guild.id, "prefix", content[1])
				await message.channel.send(f'My prefix is now \"{config.read(message.guild.id,"prefix")}\"')
		else:
			await admin.noperm(message)