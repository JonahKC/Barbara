import lib.graph as graph

graph.init()

import os, discord, traceback
from multiprocessing import Process
from console import fg
import lib.shell as shell
from discord.ext import commands
import config.config as config
import lib.admin as admin
from discord_components.client import DiscordComponents

BARBARA_VERSION = '3.4.40'


def get_prefix(
    bot, message
):  # Pass a function to command_prefix that returns the correct per-server prefix
	try:
		pfx = config.read(message.guild.id, "prefix")
	except AttributeError:
		pfx = config.default("prefix")
	return commands.when_mentioned_or(pfx)(bot, message)


intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching,
                            name='jcwyt.com')
bot = commands.Bot(command_prefix=get_prefix,
                   intents=intents,
                   activity=activity)
bot.remove_command('help')

DiscordComponents(bot)


@bot.event
async def on_ready():
	#graph setup
	#graph.setStatic("RAM")
	#graph.setStatic("CPU")
	#graph.setStatic(">>> ")
	#graph.setInput(4,graph.getHeight()-2,1)
	#graph.emit(graph.setScroll(15))
	#graph.flush()
	print(f'Connected to bot: {fg.lightgreen}{bot.user.name}{fg.default}')
	print(f'Logged in as: {fg.lightgreen}{bot.user}{fg.default}')
	print(f'Bot ID: {fg.lightgreen}{bot.user.id}{fg.default}')
	print(f'Discord.py Version: {fg.blue}{discord.__version__}{fg.default}')
	print(f'Barbara-Core Version: {fg.blue}{BARBARA_VERSION}{fg.default}')
	print(
	    f"I'm in {fg.blue}{str(len(bot.guilds))}{fg.default} server{'s' if len(bot.guilds) > 1 else ''}!"
	)
	#graph.setStatic(fg.purple + "-" * 50 + fg.default)
	shellThread = Process(target=shell.run, name="Thread-Shell")
	shellThread.start()


for filename in os.listdir(
        './cogs'):  # Loop through every file in the commands folder
	if filename.endswith('.py'):
		try:
			bot.load_extension(
			    f'cogs.{filename[:-3]}')  # Load the stuff in the file
			print(
			    f'{fg.t_5865f2}Loaded and initialized{fg.default} {fg.yellow}cogs.{filename[:-3]}{fg.default}'
			)
		except Exception as error:
			stack = traceback.extract_tb(error.__traceback__)
			print(fg.red + f'Error: {str(error)}')
			for i in stack.format():
				print(i)
			print('\n\nEnd of Stacktrace\n\n' + '-' * 50 + '\n\n' + fg.default)

shell.initialize(bot)  # initialize shell evaluation


@bot.event
async def on_message(
        message):  # If user doesn't have permission, tell them here
	ctx = await bot.get_context(message)
	if ctx.valid:
		if ctx.command.name in admin.RESTRICTED_COMMANDS and not admin.perms(
		    ctx):
			await message.author.send(admin.NO_PERMS_MESSAGE(ctx))
		else:
			if ctx.prefix is not None:
				await bot.process_commands(message)
			else:
				pass  # The message sent isn't a command


bot.run(os.getenv('TOKEN'))
