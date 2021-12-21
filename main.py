import os
import traceback
import discord
import config.config as config
import lib.admin as admin
import click
import logging
from   threading import Thread
from   flask import Flask
from   discord.ext import commands
from   discord_components.client import DiscordComponents
from   console import fg

# Version constant
BARBARA_VERSION = "3.18.116"

# Pass a function to command_prefix that returns the correct per-server prefix
def get_prefix(bot, message):

  # Attempt to read the server"s prefix from config
  try:
  	pfx = config.read(message.guild.id, "prefix")

  # If it doesn"t exist in config, use the default prefix
  except AttributeError:
    pfx = config.default("prefix")

  # You can mention Barbara instead of using her prefix
  return commands.when_mentioned_or(pfx)(bot, message)

# Give the bot all intents
# She won"t be able to play audio, for example, without the proper intent
intents = discord.Intents.all()

# Set the activity of the bot to "Watching jcwyt.com"
activity = discord.Activity(type=discord.ActivityType.watching,
                            name="jcwyt.com")

# Create the Bot object from the variables above
bot = commands.Bot(command_prefix=get_prefix,
                   intents=intents,
                   activity=activity,
									 case_insensitive=True)

# Remove the default help command
bot.remove_command("help")

# Initialize DiscordComponents, this overrides some functions adding capability for things like buttons
DiscordComponents(bot)

@bot.event
async def on_ready():

  # Start a flask server so that you can ping her to see if she's alive
  web_app = Flask('')

  # Flask we don't care about your spam

  # These are overrides to the logging functions
  def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass
  def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

  # Replace the default ones Flask uses with ours that do nothing
  click.echo = echo
  click.secho = secho

  # Make Flask only log errors. This is needed as well as the above code. Idk why.
  log = logging.getLogger('werkzeug')
  log.setLevel(logging.ERROR)

  @web_app.route('/')
  def webserver_ping():
  	return str(len(bot.guilds))

  def run_webserver():
  	web_app.run(host="0.0.0.0", port=8080)

  server = Thread(target=run_webserver)
  server.start()

  # Log bot info
  print(f"Connected to bot: {fg.lightgreen}{bot.user.name}{fg.default}")
  print(f"Logged in as: {fg.lightgreen}{bot.user}{fg.default}")
  print(f"Bot ID: {fg.lightgreen}{bot.user.id}{fg.default}")
  print(f"Discord.py Version: {fg.blue}{discord.__version__}{fg.default}")
  print(f"Barbara-Core Version: {fg.blue}{BARBARA_VERSION}{fg.default}")
  print(f"I'm in {fg.blue}{str(len(bot.guilds))}{fg.default} server{'s' if len(bot.guilds) > 1 else ''}!")

# Loop through every file (not counting subfolders) in the cogs directory
for filename in os.listdir("./cogs"):

  # If the file is a Python file
  if filename.endswith(".py"):

    # Attempt to load it as a Cog
    try:
      bot.load_extension(f"cogs.{filename[:-3]}")

      # Log the Cog that was loaded
      print(f"{fg.t_5865f2}Loaded and initialized{fg.default} {fg.yellow}cogs.{filename[:-3]}{fg.default}")
		
    # An error was encountered trying to load a Cog
    except Exception as error:

      # Get the stacktrace from the exception
      stack = traceback.extract_tb(error.__traceback__)
    
      # Debug it to the console with pretty red text
      print(fg.red + f"Error: {str(error)}")
      for i in stack.format():
      	print(i)
      print("\n\nEnd of Stacktrace\n\n" + "-" * 50 + "\n\n" + fg.default)

@bot.event
async def on_message(message):  # Perms

  # If the command was run in a DM channel
  if type(message.channel) == discord.channel.DMChannel and message.author != bot.user:
    
    # Tell the author that isn"t supported right now
    await message.channel.send("Sorry, Barbara is not support in DM conversations at this time.")
    return

  # Get the context object from the message
  ctx = await bot.get_context(message)

  # Before any commands or anything are run, run the pre_message event for meese detection
  bot.dispatch("pre_message", message)

  # If the text command is valid
  if ctx.valid:

    # If this command is restricted to admins only, and the user is not an admin
    if ctx.command.name in admin.RESTRICTED_COMMANDS and not admin.perms(ctx):

      # DM them, saying they lack perms
      await message.author.send(admin.NO_PERMS_MESSAGE(ctx))
    else:

      # If the message sent was a command
      if ctx.prefix is not None:

        # Process the text command
        await bot.process_commands(message)
      else:
        pass  # The message sent isn"t a command

# The %version command returns Barbara's version as well as Discord.py's version
@bot.command(name="version")
async def versionCommand(ctx):
  await ctx.send(f"Barbara `v{BARBARA_VERSION}`\nDiscord.py `v{discord.__version__}`")

# Run the bot with the token environment variable
bot.run(os.getenv("TOKEN"))