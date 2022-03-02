import nextcord
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class CreditsCommand(commands.Cog):
  """
  Get credits for the bot
  """
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(
    name="credits",
    description = "View everyone who contributed to Barbara and the APIs we use.",
    guild_ids=TESTING_GUILD_ID,
    force_global=SLASH_COMMANDS_GLOBAL,
  )
  async def help_command(self, interaction: nextcord.Interaction):
    """
    Get credits for the bot
    """

    # Open the credits file
    with open("./resources/credits.txt", "r") as credits_file:

      # Read it
      credits = credits_file.read()

      # Send the credits
      await interaction.send(credits, ephemeral=False)

  
def setup(bot):
  bot.add_cog(CreditsCommand(bot))