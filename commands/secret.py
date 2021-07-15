import resources.secret_messages
import random
async def main(message, prefix, client):
	if message.content.startswith(f"{prefix}secret"): 
		rand = random.randint(0, len(resources.secret_messages.secret_messages))
		await message.channel.send(resources.secret_messages.secret_messages[rand])