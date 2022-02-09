import util
import nextcord
from nextcord.ext import commands
from constants import TESTING_GUILD_ID

class ReloadCommand(commands.Cog):
  """
  Reload a Cog.
  """
  def __init__(self, bot):
    self.bot = bot

  @util.jcwyt()
  @nextcord.slash_command(
    name="reload",    description="[ㅈ] Reload a Cog.",
    
    # Only available in the JCWYT Discord, always not globally
    guild_ids=TESTING_GUILD_ID
  )
  async def reload_cog_command(
    self,
    interaction: nextcord.Interaction,
    cog_name: str=nextcord.SlashOption(
      required=True,
      name="cog",
      description="The name of the Cog to reload.",
      autocomplete=True
    )
  ):
    """
    Reload a Cog by name
    """

    try:

      # Attempt to reload the Cog
      self.bot.reload_extension(cog_name)

    # If there's an error loading the Cog
    except Exception as err:
      
      # Send an error message
      await interaction.send(util.get_message("jcwyt.reload_cog_failed", cog_name=cog_name, error_name=type(err).__name__, error_message=str(err)), ephemeral=True)
    
    # If there's not an error,
    else:

      # Send a success message
      await interaction.send(util.get_message("jcwyt.reload_cog_succeeded", cog_name=cog_name), ephemeral=True)
  
  @reload_cog_command.on_autocomplete("cog_name")
  async def reload_cog_command_autocomplete(self, interaction: nextcord.Interaction, cog_name: str):
  
    # Get all of the bot's Cog objects
    cogs = self.bot.cogs.values()

    # Get the name (ex. commands.reload, not ReloadCommand) of the Cog
    cogs = map(lambda x: x.qualified_name, cogs)

    await interaction.response.send_autocomplete(cogs)

def setup(bot):
  bot.add_cog(ReloadCommand(bot))