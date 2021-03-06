import util
import config
import nextcord
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class LogCommand(commands.Cog):
  """
	Configure logging bot actions.
	"""
  def __init__(self, bot):
    self.bot = bot

  @util.admin()
  @nextcord.slash_command(
		name='log',
		description='Toggle/set the channel to log actions to.',
		guild_ids=TESTING_GUILD_ID,
		force_global=SLASH_COMMANDS_GLOBAL
	)
  async def log_command(self, interaction: nextcord.Interaction, channel: nextcord.abc.GuildChannel=nextcord.SlashOption(
		required=False,
    name='channel',
    description="The channel to log actions to.",
    #autocomplete=True
	)):
    if not channel:
      await interaction.send(util.get_message('log.read_channel', channel=self.bot.get_channel(config.read(interaction.guild_id, 'log_channel'))))

    # If the channel is already set to log
    elif config.read(interaction.guild_id, 'log_channel') == channel.id:

      # Remove the logging channel (0 means don't log)
      config.write(interaction.guild_id,'log_channel', 0)

      # Send the success message
      await interaction.send(util.get_message('log.unset_channel', channel=channel))
    else:
      config.write(interaction.guild_id,'log_channel', channel.id)
      await interaction.send(util.get_message('log.set_channel', channel=channel))
  
  # Autocompletions are broken rn
  #@log_command.on_autocomplete('channel')
  #async def log_command_autocomplete(self, interaction: nextcord.Interaction, channel: str):
  #  
  #  # Get all text channels in the server
  #  text_channels = filter(
  #    lambda channel: type(channel) == nextcord.channel.TextChannel,
  #    interaction.guild.channels
  #  )

  #  # Get their names
  #  text_channels = map(lambda x: x.name, text_channels)
  #  
  #  await interaction.response.send_autocomplete(text_channels)

def setup(bot):
  bot.add_cog(LogCommand(bot))