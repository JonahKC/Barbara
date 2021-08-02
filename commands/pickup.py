import lib.messages as messages

NAME = "pickup"

previous_pickup_data = ["", 000000000000000000, 1]
rand = -1

async def main(message, prefix, client):
  global previous_pickup_data
  global rand
  global sent_pickups
  if previous_pickup_data[1] == message.author.id:
    await message.channel.send(previous_pickup_data[0][previous_pickup_data[2]])
    if len(previous_pickup_data[0]) - 1 == previous_pickup_data[2]:
      previous_pickup_data = ["", 000000000000000000, 1]
      return
    previous_pickup_data[2] += 1
  if message.content.startswith(f"{prefix}pickup"):
    pickup = await messages.random_message(message.guild.id, "pickup")
    if "{answer}" in pickup:
      pickup = pickup.split("{answer}")
      await message.channel.send(pickup[0])
      previous_pickup_data = [pickup, message.author.id, previous_pickup_data[2]]
      return
    await message.channel.send(pickup)