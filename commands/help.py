import util
import nextcord
from nextcord.ext import commands
from lib.paginator import Paginator
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

    # Open the file with the help text
    with open("./resources/help.txt", "r") as f:

      # Read the file
      help_text = f.read().split("ADMIN_ONLY\n")

      # Split each section into individual pages
      non_admin_help_pages = help_text[0].split("PAGE\n")
      admin_help_pages = help_text[1].split("PAGE\n")

      ## If the user is an admin, send the admin-only help pages as well as the normal help text
      if(util._has_permissions(interaction.user)):
        help_pages_ui = Paginator(interaction, self.bot, non_admin_help_pages + admin_help_pages)
      
      # If the user is not an admin, send the normal help pages only
      else:
        help_pages_ui = Paginator(interaction, self.bot, non_admin_help_pages)

      # Run the paginator in a message
      await help_pages_ui.start(ephemeral=True)

def setup(bot):
  bot.add_cog(HelpCommand(bot))