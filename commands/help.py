import util
import nextcord
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class HelpCommand(commands.Cog):
  """
  Get help on every command in the bot.
  """
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(
    name="help",
    description="All commands and what they do.",
    guild_ids=TESTING_GUILD_ID,
    force_global=SLASH_COMMANDS_GLOBAL
  )
  async def help_command(self, interaction: nextcord.Interaction):
    """
    Get help on every command in the bot.
    """

    # Use interaction.response.defer() to send the "Bot is thinking" message
    await interaction.response.defer(ephemeral=True)

    # Open the file with the help text
    with open("./resources/help.txt", "r") as f:

      # Read the file
      help_text = f.read().split("ADMIN_ONLY\n")

      # If the user is an admin, send the admin-only help text as well as the normal help text
      if(util._has_permissions(interaction.user)):
        await interaction.send(help_text[0] + help_text[1], ephemeral=True)
      
      # If the user is not an admin, send the normal help text only
      else:
        await interaction.send(help_text[0], ephemeral=True)
  
def setup(bot):
  bot.add_cog(HelpCommand(bot))