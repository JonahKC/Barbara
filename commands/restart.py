import sys
import util
import nextcord
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class RestartCommand(commands.Cog):
  """
	docstring
	"""
  def __init__(self, bot):
    self.bot = bot

  @util.jcwyt()
  @nextcord.slash_command(
		name='restart',
		description='Restart the entire bot',
		guild_ids=TESTING_GUILD_ID,
		force_global=SLASH_COMMANDS_GLOBAL
	)
  async def restart_command(self, interaction: nextcord.Interaction):
    await interaction.send("Restarting bot...")

    # We want a "bot online again" message, so let's write the place
    # that message should be in a file.
    shutdown_message_file = open('./temp/shutdown-message.txt', 'w')
    shutdown_message_file.write(str(interaction.channel_id))
    shutdown_message_file.close()

    # Clear the terminal
    util.clear_terminal()

    # Kill the process
    # (since it's running under autorestart.sh, it will automatically turn back on again)
    sys.exit(0)

  @commands.Cog.listener()
  async def on_ready(self):
    try:

      # Let's see if we need to send a success message, since we just restarted
      shutdown_message_file = open('./temp/shutdown-message.txt', 'r+')
      shutdown_message_data = shutdown_message_file.read()

      # Delete contents so it doesn't send message next restart
      shutdown_message_file.truncate(0)
      shutdown_message_file.close()

      # Get the channel to send success message in
      channel = self.bot.get_channel(int(shutdown_message_data))

      # Send the success message!
      await channel.send("Succesfully restarted!")

    # If there's no success message to send
    # or the file doesn't exist
    except (ValueError, FileNotFoundError):

      # We don't care
      pass

def setup(bot):
  bot.add_cog(RestartCommand(bot))