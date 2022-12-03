print(f'\033[0;34mInitializing Bot...\033[0m')

from dotenv import load_dotenv

load_dotenv()

import os
import time
import util
import config
import signal
import aiohttp
import platform
import nextcord
import threading
from console import fg
from nextcord.ext import commands
import lib.randommer as randommer
import lib.huggingface as huggingface


def die():
    # get the current PID for safe terminate server if needed:
    PID = os.getpid()
    if platform.system() != 'Windows':
        PGID = os.getpgid(PID)
    if platform.system() != 'Windows':
        os.killpg(PGID, signal.SIGKILL)
    else:
        os.kill(PID, signal.SIGTERM)


# Bot Version
__version__ = '4.1.1'

# Give the bot intents
# She won't be able to play audio, for example, without the proper intent
intents = nextcord.Intents.default()
intents.voice_states = True
intents.webhooks = True

# Watching jcwyt.com
activity = nextcord.Activity(
    type=nextcord.ActivityType.watching,
    name='jcwyt.com',
)

# Create the Bot object from the variables above
bot = commands.Bot(

    # command_prefix is required for some reason
    command_prefix='~~%~~',
    intents=intents,
    activity=activity,
    case_insensitive=True,
)

# Commandline "interpreter"
stop = False


def interpreter():
    global bot

    @bot.listen()
    async def on_ready():
        global bot, stop
        print('')

        while not stop:
            text = input('> ')
            if text.lower() == 'stop':
                stop = True
                await bot.close()
            elif text.lower() == 'test':
                await (await bot.fetch_channel(880164840147157070)
                       ).send('Testing...`' + str(bot.latency * 1000) + '`ms')


# Remove the default help command
bot.remove_command('help')

bot.__version__ = __version__


@bot.event
async def on_ready():

    # Setup all of our clientsessions
    bot.session = aiohttp.ClientSession()

    # Give our libs access to the central ClientSession
    huggingface.session = bot.session
    randommer.session = bot.session

    # Log bot info
    print(f'Barbara Version: {fg.lightgreen}{__version__}{fg.default}')
    print(f'Connected to bot: {fg.lightgreen}{bot.user.name}{fg.default}')
    print(f'Bot ID: {fg.lightgreen}{bot.user.id}{fg.default}')
    print(
        f'I\'m in {fg.blue}{str(len(bot.guilds))}{fg.default} server{"s" if len(bot.guilds) > 1 else ""}!'
    )


# Text commands? More like,, bad
@bot.event
async def on_message(message):
    try:
        if message.content.startswith(config.read(message.guild.id, 'prefix')):
            await message.channel.send(
                util.get_message('legacy.slash_commands'))
    except Exception:
        pass


# This is for permissions
# Called every time the bot receives an Interaction (for example, a slash command)
@bot.event
async def on_interaction(interaction: nextcord.Interaction):

    # If the Interaction type is a slash command
    if interaction.type == nextcord.InteractionType.application_command:

        # If the command is in the list of admin commands
        if interaction.data['name'] in util.admin_commands:

            # If the user is NOT an admin
            if not util._has_permissions(interaction.user):

                # Send the no permissions message
                await interaction.send(
                    util.get_message('admin.user_not_admin'), ephemeral=True)

                # And then stop the command from running
                return

        # If the command is in the list of JCWYT-only commands
        elif interaction.data['name'] in util.jcwyt_commands:

            # If the user is NOT a JCWYT user
            if not interaction.user.id in util.JCWYT_TEAM:

                # Send the no permissions message
                await interaction.send(
                    util.get_message('admin.user_not_jcwyt'), ephemeral=True)

                # And then stop the command from running
                return

        try:

            # If there's permissions to run the command, run it
            await bot.process_application_commands(interaction)
        except Exception as err:

            # Send out a custom event for the error handler
            bot.dispatch('application_command_error', err, interaction)


# Load all misc cogs in the extensions folder
util.load_directory(bot, 'extensions')

# Load all commands in the commands folder
util.load_directory(bot, 'commands')

# Run the bot!
while not stop:
    try:
        interpreter_thread = threading.Thread(target=interpreter)
        interpreter_thread.start()
        bot.run(os.getenv('TOKEN'))

    # Catch errors talking to the Discord API
    except nextcord.errors.HTTPException as err:

        # Catch ratelimits
        if err.status == 429:

            # Clear the terminal
            util.clear_terminal()

            # Explain what's happening
            print(f'{fg.red}Rate limit exceeded.{fg.default}')
            retry_after = err.response.headers['Retry-After']
            print(
                f'{fg.green}Retrying in {retry_after} seconds...{fg.default}')

            # Wait for the specified duration (+1 second for padding)
            time.sleep(int(retry_after))

            #Try to run the bot again
            continue

interpreter_thread.join(0)
die()
