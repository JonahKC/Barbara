import discord
#from discord.ext import commands
#from discord_slash import SlashCommand, SlashContext
import os
import random
import re
import keep_alive
import meese
import secret_messages
import asyncio

intents = discord.Intents(messages=True, guilds=True)
client = discord.Client(intents=intents)

#PREFIX = ("!")
#bot = commands.Bot(command_prefix=PREFIX, description=f'{"~~Bull~~"}#Botwinkle')
#slash = SlashCommand(bot)

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='jcwyt.com'))
  keep_alive.keep_alive()
  print('Connected to bot: {}'.format(client.user.name))
  print('Bot ID: {}'.format(client.user.id))
  print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if f'<@!{client.user.id}>' in message.content:
		nick = message.author.nick
		if message.author.nick == None:
			nick = message.author.name
		await message.channel.send(f'Hello there, {nick}!')
	if message.content.startswith("!secret"):
		rand = random.randint(0, len(secret_messages.secret_messages))
		await message.channel.send(secret_messages.secret_messages[rand])
	if ":meese:" in message.content:
		foo = message.content
		await message.delete()
		await client.get_channel(860680588562006027).send(message.author.nick+": "+foo)
	if meese.containsMeese(message.content):
		print("meese")
		foo = message.content
		await message.delete()
		await client.get_channel(860680588562006027).send(message.author.nick+": "+foo)
	if message.content.startswith("!links"):
	  await message.channel.send(
		    "Check out our projects at <https://jcwyt.com>!"
		)
	if message.content.startswith("!help"):
		await message.channel.send(
		    "**Hey there sweetie! I'm Barbara! Here's some things you can ask me:**\n!secret - I'll tell you a secret!\n!links - Check out some links to our projects.\n!pickup - I'll give you a pickup line!\nAlso, I filter out the word ||meese||!\n<https://barbara.jcwyt.com>"
		)		
	if message.content.startswith("!eval"):
	  permitted_users = [738843304057372702, 797282028344573992]
	  if message.author.id in permitted_users:
	  	msg_content = message.content[5:]
	  	try:
	  		await eval(msg_content, {"message": message, "re": re, "os": os, "discord": discord})
  		except Exception as e:
  			await message.channel.send(e)
client.run(os.getenv('TOKEN'))