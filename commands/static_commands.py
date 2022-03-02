import util
import nextcord
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class StaticCommands(commands.Cog):
  """
	All of the commands with static text responses. As much as I hate cramming a bunch of stuff into one Cog, making 10 separate Cogs for various static commands seems like overkill.
	"""
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(
		name='vote',
		description='Vote for Barbara on top.gg!',
		guild_ids=TESTING_GUILD_ID,
		force_global=SLASH_COMMANDS_GLOBAL
	)
  async def vote_command(self, interaction: nextcord.Interaction):
    await interaction.send(util.get_message('info.vote'))

  @nextcord.slash_command(
		name='invite',
		description='Invite Barbara to your server!',
		guild_ids=TESTING_GUILD_ID,
		force_global=SLASH_COMMANDS_GLOBAL
	)
  async def invite_command(self, interaction: nextcord.Interaction):
    await interaction.send(util.get_message('info.invite'))

  @nextcord.slash_command(
    name='version',
    description='No idea why you\'d need this',
		guild_ids=TESTING_GUILD_ID,
		force_global=SLASH_COMMANDS_GLOBAL
  )
  async def version_command(self, interaction: nextcord.Interaction):
    await interaction.send(self.bot.__version__, ephemeral=True)

def setup(bot):
  bot.add_cog(StaticCommands(bot))