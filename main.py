import discord
import os
import lib.keep_alive
from commands import *
import commands.__init__ as init
import config.config as config
from discord_components import DiscordComponents

commandArray = init.commands

intents = discord.Intents(messages=True, guilds=True)
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='jcwyt.com'))
	DiscordComponents(client)
	lib.keep_alive.keep_alive()
	print('Connected to bot: {}'.format(client.user.name))
	print('Logged in as: {0.user}'.format(client))
	print('Bot ID: {}'.format(client.user.id))
	print("Servers: " + str(len(client.guilds)))

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	for i in commandArray:
		await i.main(message, config.read(message.guild.id, "prefix"), client)
		#eval(f"await {commands.__init__.__all__[i]}.main(message, config.read(message.guild.id, \"prefix\"), client)")
	#await Ceval.main(message, config.read(message.guild.id, "prefix"), client)
	#await Chelp.main(message, config.read(message.guild.id, "prefix"), client)
	#await hibarbara.main(message, config.read(message.guild.id, "prefix"), client)
	#await link.main(message, config.read(message.guild.id, "prefix"), client)
	#await pickup.main(message, config.read(message.guild.id, "prefix"), client)
	#await removemeese.main(message, config.read(message.guild.id, "prefix"), client)
	#await sayb.main(message, config.read(message.guild.id, "prefix"), client)
	#await secret.main(message, config.read(message.guild.id, "prefix"), client)
	#await prefix.main(message, config.read(message.guild.id,"prefix"), client)
	#await Cconfig.main(message, config.read(message.guild.id,"prefix"), client)

client.run(os.getenv('TOKEN'))