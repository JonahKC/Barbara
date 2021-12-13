#import lib.graph as graph
#graph.init()

import os, discord, traceback
#from multiprocessing import Process
from console import fg
#import lib.shell as shell
from discord.ext import commands
import config.config as config
import lib.admin as admin
from discord_components.client import DiscordComponents

# Version constant
BARBARA_VERSION = '3.17.114'

# Pass a function to command_prefix that returns the correct per-server prefix
def get_prefix(bot, message):

  # Attempt to read the server's prefix from config
  try:
  	pfx = config.read(message.guild.id, "prefix")

  # If it doesn't exist in config, use the default prefix
  except AttributeError:
    pfx = config.default("prefix")

  # You can mention Barbara instead of using her prefix
  return commands.when_mentioned_or(pfx)(bot, message)

# Give the bot all intents
# She won't be able to play audio, for example, without the proper intent
intents = discord.Intents.all()

# Set the activity of the bot to "Watching jcwyt.com"
activity = discord.Activity(type=discord.ActivityType.watching,
                            name='jcwyt.com')

# Create the Bot object from the variables above
bot = commands.Bot(command_prefix=get_prefix,
                   intents=intents,
                   activity=activity,
									 case_insensitive=True)

# Remove the default help command
bot.remove_command('help')

# Initialize DiscordComponents, this overrides some functions adding capability for things like buttons
DiscordComponents(bot)

@bot.event
async def on_ready():

  # Log bot info
  print(f'Connected to bot: {fg.lightgreen}{bot.user.name}{fg.default}')
  print(f'Logged in as: {fg.lightgreen}{bot.user}{fg.default}')
  print(f'Bot ID: {fg.lightgreen}{bot.user.id}{fg.default}')
  print(f'Discord.py Version: {fg.blue}{discord.__version__}{fg.default}')
  print(f'Barbara-Core Version: {fg.blue}{BARBARA_VERSION}{fg.default}')
  print(f"I'm in {fg.blue}{str(len(bot.guilds))}{fg.default} server{'s' if len(bot.guilds) > 1 else ''}!")
  #shellThread = Process(target=shell.run, name="Thread-Shell")
  #shellThread.start()

# Loop through every file (not counting subfolders) in the cogs directory
for filename in os.listdir('./cogs'):

  # If the file is a Python file
	if filename.endswith('.py'):

    # Attempt to load it as a Cog
		try:
			bot.load_extension(f'cogs.{filename[:-3]}')
			
      # Log the Cog that was loaded
      print(f'{fg.t_5865f2}Loaded and initialized{fg.default} {fg.yellow}cogs.{filename[:-3]}{fg.default}')
		
    # An error was encountered trying to load a Cog
    except Exception as error:

      # Get the stacktrace from the exception
			stack = traceback.extract_tb(error.__traceback__)
			
      # Debug it to the console with pretty red text
      print(fg.red + f'Error: {str(error)}')
			for i in stack.format():
				print(i)
			print('\n\nEnd of Stacktrace\n\n' + '-' * 50 + '\n\n' + fg.default)

#shell.initialize(bot)  # initialize shell evaluation

@bot.event
async def on_message(message):  # Perms

  # If the command was run in a DM channel
  if type(message.channel) == discord.channel.DMChannel and message.author != bot.user:
    
    # Tell the author that isn't supported right now
    await message.channel.send("Sorry, Barbara is not support in DM conversations at this time.")
    return

  # Get the context object from the message
  ctx = await bot.get_context(message)

  # Before any commands or anything are run, run the pre_message event for meese detection
  bot.dispatch('pre_message', message)

  # If the text command is valid
  if ctx.valid:

    # If this command is restricted to admins only, and the user is not an admin
    if ctx.command.name in admin.RESTRICTED_COMMANDS and not admin.perms(ctx):

      # DM them, saying they lack perms
      await message.author.send(admin.NO_PERMS_MESSAGE(ctx))
    else:

      # If the message sent was a command
      if ctx.prefix is not None:

        # Write commands that are executed to a log
        with open('./cmds.log', 'a') as log:
          log.write("Executing command: " + message.content + "\n")
        await bot.process_commands(message)
      else:
        pass  # The message sent isn't a command

@bot.command(name='version') # %version
async def versionCommand(ctx):
  await ctx.send(f'Barbara `v{BARBARA_VERSION}`\nDiscord.py `v{discord.__version__}`')

bot.run(os.getenv('TOKEN'))