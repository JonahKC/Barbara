import util
import config
import nextcord
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class LinkCommand(commands.Cog):
  """
	/link returns a customizable server-specific message
	"""
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(
		name='link',
		description='Sends a custom server-specific message',
		guild_ids=TESTING_GUILD_ID,
		force_global=SLASH_COMMANDS_GLOBAL
	)
  async def link_command(self, interaction: nextcord.Interaction, link: str=nextcord.SlashOption(
    required=False,
    description='Admin-only parameter for setting the link of the server.'
  )):

    # If you're an admin and you specified a custom link
    if util._has_permissions(interaction.user) and link:

      # Write the new link to config
      config.write(interaction.guild_id, 'link', link)

      # Send a success message
      await interaction.send(util.get_message('config.write_success', option='link', value=link), ephemeral=True)
      return

    link = config.read(interaction.guild_id, 'link')

    # If the link is not disabled
    if not link == 'None':

      # Send the link
      await interaction.send(link.replace('{prefix}', config.read(interaction.guild_id, 'prefix')), ephemeral=True)

def setup(bot):
  bot.add_cog(LinkCommand(bot))