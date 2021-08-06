import os, discord
import lib.keep_alive
import commands.__init__ as init
import commands.init as onMessageInit
import config.config as config

from discord_components import DiscordComponents

commandArray = init.commands

intents = discord.Intents(messages=True, guilds=True)
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(
	    type=discord.ActivityType.watching, name='jcwyt.com'))
  DiscordComponents(client)
  lib.keep_alive.keep_alive()
  print('Connected to bot: {0.name}'.format(client.user))
  print('Logged in as: {}'.format(client.user))
  print('Bot ID: {0.id}'.format(client.user))
  print("I'm in {} servers!".format(str(len(client.guilds))))

@client.event
async def on_voice_state_update(member, before, after):
    vcnotfchannel = client.get_channel(863922969667567646)
    if before.channel is None and after.channel is not None:
        await vcnotfchannel.send("<@" + str(member.id) + "> joined " + str(after.channel) + " VC!")
    elif before.channel is not None and after.channel is None:
        await vcnotfchannel.send("<@" + str(member.id) + "> left " + str(before.channel) + " VC!")
    elif before.channel != after.channel:
        await vcnotfchannel.send("<@" + str(member.id) + "> moved from " + str(before.channel) + " VC to " + str(after.channel) + " VC!")

@client.event
async def on_message(message):
  global client, commandArray
  if message.author == client.user:
    return
  prefix = config.read(message.guild.id, "prefix")
  await onMessageInit.main(message, prefix, client)
  for c in commandArray:
    if message.content.startswith(prefix + c.NAME) or c.NAME == "*":
      await c.main(message, prefix, client)
    
client.run(os.getenv('TOKEN'))