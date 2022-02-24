import nextcord
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class FactCommand(commands.Cog):
  """
	Get a random fact from uselessfacts.jsph.pl
	"""
  def __init__(self, bot):
    self.bot = bot
    self.RANDOM_FACT_URL = 'https://uselessfacts.jsph.pl/random.json?language=en'

  @nextcord.slash_command(
		name='fact',
		description='Get a random fact from the Random Facts API!',
		guild_ids=TESTING_GUILD_ID,
		force_global=SLASH_COMMANDS_GLOBAL
	)
  async def fact_command(self, interaction: nextcord.Interaction):
    async with self.bot.session.get(self.RANDOM_FACT_URL) as res:
      
      # Get the JSON response
      # The 'text' property contains the fact string
      fact = (await res.json())['text']

      await interaction.send(fact)

def setup(bot):
  bot.add_cog(FactCommand(bot))