import re
from discord_components import DiscordComponents, Button, ButtonStyle
# %sayb https://geekveggie.dev MyWebsite! The button will take you to my website!
async def main(message, prefix, client):
	if message.content.startswith(f"{prefix}sayb"):
		content = message.content.split(" ")
		text = ' '.join(content[3:])
		await message.channel.send(
			text,
			components=[Button(style=ButtonStyle.URL, label=content[2], url=content[1])]
			)
		await message.delete()