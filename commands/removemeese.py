import lib.meese as meese
import config.config as config
async def main(message, prefix, client):
	if config.read(message.guild.id, "nomees") == "true":
		if ":meese:" in message.content:
			foo = message.content
			await message.delete()
			await client.get_channel(864644173835665458).send	(message.author.nick+": "+foo)
		if meese.containsMeese(message.content):
			foo = message.content
			await message.delete()
			await client.get_channel(864644173835665458).send	(message.author.name + ": " + foo)