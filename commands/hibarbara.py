async def main(message, prefix, client):
	if f'<@!{client.user.id}>' in message.content:
		nick = message.author.nick
		if message.author.nick == None:
			nick = message.author.name
		await message.channel.send(f'Hello there, {nick}!\nTip: Type `{prefix}help` to see what commands I run!')