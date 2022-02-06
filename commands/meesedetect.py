import util
import config
import nextcord
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class MeeseDetectCommand(commands.Cog):
  """
  Enable/disable meese detection. Alias of /config set nomees [true/false]
  """
  def __init__(self, bot):
    self.bot = bot

  @util.admin()
  @nextcord.slash_command(
    name="meesedetect",
    description="Enables or disables Meese detection.",
    guild_ids=TESTING_GUILD_ID,
    force_global=SLASH_COMMANDS_GLOBAL,
  )
  async def meesedetect_command(self, interaction: nextcord.Interaction, detect_meese: bool):
    """
    Whether or not to detect and censor the incorrect plural of moose. For more information check <https://moosenotmeese.org>
    """
    try:

      # Attempt to write the new config value
      config.write(interaction.guild_id, "nomees", detect_meese)

      # Send a success message equivalent to /config set nomees true/false
      await interaction.send(util.get_message('config.write_success', option="nomees", value=detect_meese))
    
    # If there's an error writing the new config value
    except config.ConfigException as err:

      # Send the error
      await interaction.send(err.__repr__())

def setup(bot):
  bot.add_cog(MeeseDetectCommand(bot))