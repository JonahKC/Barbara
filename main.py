print(f"\033[0;34mInitializing Bot...\033[0m")

import os
import time
import util
import nextcord
from console import fg
from nextcord.ext.commands import Bot

# Bot Version
__version__ = "4.0.0.jonahwashere"

# Give the bot intents
# She won"t be able to play audio, for example, without the proper intent
intents = nextcord.Intents.default()
intents.voice_states = True
intents.webhooks = True

# Set the activity of the bot to "Watching jcwyt.com"
activity = nextcord.Activity(
  type=nextcord.ActivityType.watching,
  name="jcwyt.com",
)

# Create the Bot object from the variables above
bot = Bot(

  # command_prefix is required for some dumb reason
  command_prefix="~~%~~",
  intents=intents,
  activity=activity,
  case_insensitive=True,
)

@bot.event
async def on_ready():

  # Log bot info
  print(f"Barbara Version: {fg.lightgreen}{__version__}{fg.default}")
  print(f"Connected to bot: {fg.lightgreen}{bot.user.name}{fg.default}")
  print(f"Bot ID: {fg.lightgreen}{bot.user.id}{fg.default}")
  print(
    f"I'm in {fg.blue}{str(len(bot.guilds))}{fg.default} server{'s' if len(bot.guilds) > 1 else ''}!"
  )

# Load all misc cogs in the extensions folder
util.load_directory(bot, "extensions")

# Load all commands in the commands folder
util.load_directory(bot, "commands")

# Run the bot!
while True:
  try:
    bot.run(os.getenv("TOKEN"))

  # Catch errors talking to the Discord API
  except nextcord.errors.HTTPException as err:

    # Catch ratelimits
    if err.status == 429:

      # Explain what's happening
      print(f"{fg.red}Rate limit exceeded.{fg.default}")
      print(
        f"{fg.green}Retrying in {err.response.headers['X-RateLimit-Reset-After']+1} seconds...{fg.default}"
      )

      # Wait for the specified duration (+1 second for padding)
      time.sleep(
        int(err.response.headers['X-RateLimit-Reset-After']) + 1)

      # Try to run the bot again
      continue