import resources.pickup_lines
import random
async def main(message, prefix, client):
	if message.content.startswith(f"{prefix}pickup"):
		rand = random.randint(0, len(resources.pickup_lines.pickup_lines))
		await message.channel.send(resources.pickup_lines.pickup_lines[rand])