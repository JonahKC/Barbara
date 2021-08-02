import lib.messages as messages

NAME = "secret"

async def main(message, prefix, client):
  if message.content.startswith(f"{prefix}secret"):
    await message.channel.send(await messages.random_message(message.guild.id, "secret"))