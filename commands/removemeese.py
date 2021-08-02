import lib.meese as meese
import config.config as config
async def main(message, prefix, client):
	if message.author.id != client.user.id and message.author.id != 798016639089901610:
		if config.read(message.guild.id, "nomees") == "true":
			if ":meese:" in message.content:
				foo = message.content
				await message.delete()
				await client.get_channel(864644173835665458).send	(message.author.name+": "+foo)
			else:
				string = message.content
				whitelist = config.fetch(message.guild.id, "whitelist")
				for i in whitelist:
					string = string.replace(i,"")
				if meese.containsMeese(string):
					await message.delete()
					await client.get_channel(864644173835665458).send	(message.author.name + ": " + message.content)