import os, discord
from discord.ext import commands
import config.config as config
import lib.admin as admin
from discord_components.client import DiscordComponents

def get_prefix(
    bot, message
):  # Pass a function to command_prefix that returns the correct per-server prefix
    if isinstance(message.channel, discord.channel.DMChannel):
        return "%"
    else:
        return commands.when_mentioned_or(
            config.read(message.guild.id, "prefix"))(bot, message)


intents = discord.Intents(messages=True, guilds=True)
activity = discord.Activity(
    type=discord.ActivityType.watching,
    name='jcwyt.com')  # Changes bot's activity to "Watching jcwyt.com"
bot = commands.Bot(command_prefix=get_prefix,
                   intents=intents,
                   case_insensitive=True,
                   activity=activity)
bot.remove_command(
    'help'
)  # There's a default help command, so let's remove that so we can add our own.
DiscordComponents(bot)



@bot.event
async def on_ready():
    print('Connected to bot: {0.name}'.format(bot.user))
    print('Logged in as: {}'.format(bot.user))
    print('Bot ID: {0.id}'.format(bot.user))
    print(f'Discord.py Version: {discord.__version__}')
    print(
        f"I'm in {str(len(bot.guilds))} server{'s' if len(bot.guilds) > 1 else ''}!"
    )


for filename in os.listdir(
        './cogs'):  # Loop through every file in the commands folder
    if filename.endswith('.py'):
        bot.load_extension(
            f'cogs.{filename[:-3]}')  # Load the stuff in the file
        print(f'Loaded and initialized cogs.{filename[:-3]}')


@bot.event
async def on_message(
        message):  # If user doesn't have permission, tell them here
    ctx = await bot.get_context(message)
    if ctx.valid:
        if ctx.command.name in admin.RESTRICTED_COMMANDS and not admin.perms(
                ctx):
            await message.author.send(admin.NO_PERMS_MESSAGE(ctx))
        else:
            await bot.process_commands(message)
    else:
        pass  # The message sent isn't a command


# Was causing duplicate Barbaras, probably an easy fix, but until you get around to it I've disabled the feature to prevent it. Since we're using the new system (discord.ext.commands) you should put this in it's own Cog
#def reloadFile(file):
#	imp.reload(file)
#
#def shellStart():
#	shell.start(bot)
#
#shellThread = threading.Thread(target=shellStart,name="Thread-Shell")
#shellThread.start()
bot.run(os.getenv('TOKEN'))
