import nextcord
import util
import config
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL, LOG_ACTIONS

class LogCommand(commands.Cog):
  """
	Configure logging bot actions.
	"""
  def __init__(self, bot):
    self.bot = bot

  @util.admin()
  @nextcord.slash_command(
		name = 'log',
		description = 'Configure logging bot actions.',
		guild_ids = TESTING_GUILD_ID,
		force_global = SLASH_COMMANDS_GLOBAL
	)
  async def log_command(self, interaction: nextcord.Interaction):
    pass

  @log_command.subcommand(
		name = 'channel',
		description = 'Read or set the channel to log actions to.'
	)
  async def log_channel_command(self, interaction: nextcord.Interaction, channel: nextcord.abc.GuildChannel=nextcord.SlashOption(
		required = False,
		name = "channel"
	)):
    if not channel:
      await interaction.send(util.get_message('log.read_channel',channel=self.bot.get_channel(config.read(interaction.guild_id, 'log channel'))))
    else:
      config.write(interaction.guild_id,'log channel', channel.id)
      await interaction.send(util.get_message('log.set_channel', channel=channel))

  @log_command.subcommand(
		name = 'action',
		description = 'Enable or disable logging of a certain action.'
	)
  async def log_action_command(self, interaction: nextcord.Interaction,  action:str=nextcord.SlashOption(
		required = True,
		name = 'action',
		choices = tuple(LOG_ACTIONS)
	), enabled: bool=nextcord.SlashOption(
		required = False,
		name = 'enabled'
	)):
    if enabled != None:
      if enabled and not action in config.fetch(interaction.guild_id, 'log actions'):
        config.append(interaction.guild_id,'log actions',action)
      elif not enabled:
        config.remove(interaction.guild_id,'log actions',action)
      message = util.get_message('log.set_action',enabled,action = action)
      await interaction.send(message)
    else:
      actions = config.fetch(interaction.guild_id,'log actions')
      value = action in actions
      message = util.get_message('log.read_action',value,action=action)
      await interaction.send(message)

def setup(bot):
  bot.add_cog(LogCommand(bot))