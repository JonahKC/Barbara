async def main(message, prefix, client):
	if message.content.startswith(f"{prefix}invite"):
		await message.channel.send("**Invite Me to Your Other Discord Servers!**\n<https://barbara.jcwyt.com/invite>");