import nextcord
import datetime
import humanize
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class AgeCommand(commands.Cog):
  """
	Get the age of someone or something.
	"""
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(
		name='age',
		description='Get the age of someone or something.',
		guild_ids=TESTING_GUILD_ID,
		force_global=SLASH_COMMANDS_GLOBAL
	)
  async def age_command(self, interaction: nextcord.Interaction, member:nextcord.Member=nextcord.SlashOption(
		name="member",
		description="The member to check the age of."
		), precision:int=nextcord.SlashOption(
		name= "precision",
		description= "How precisely I should give you the age.",
		required= False,
		default= 1,
		choices= {"imprecise":1,"precise":2}
	)):

    # Time Zone Finnicky-ness
    naive = member.created_at.replace(tzinfo=None)

		# Get the time since they were born
    age = datetime.datetime.now() - naive

		# Smth from v3 idk probably important
    # Josh this backslashes Discord formatting shenanigans
    name = member.name.replace('_', r'\_').replace('*', r'\*')

		# Send the result
    await interaction.send(f"{name} is {humanize.precisedelta(age)} old.")

def setup(bot):
  bot.add_cog(AgeCommand(bot))
