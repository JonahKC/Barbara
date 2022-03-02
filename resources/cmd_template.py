import nextcord
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class TemplateCommand(commands.Cog):
  """
	docstring
	"""
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(
		name='name',
		description='description',
		guild_ids=TESTING_GUILD_ID,
		force_global=SLASH_COMMANDS_GLOBAL
	)
  async def template_command(self, interaction: nextcord.Interaction):
    pass

def setup(bot):
  bot.add_cog(TemplateCommand(bot))