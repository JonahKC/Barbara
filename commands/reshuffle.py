import util
import nextcord
import lib.random_msg as random_msg
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class ReshuffleCommand(commands.Cog):
  """
	Force-reshuffle the breakup/pickup line cache.
	"""
  def __init__(self, bot):
    self.bot = bot

  @util.jcwyt()
  @nextcord.slash_command(
		name='reshuffle',
		description='Force reshuffle the breakup/pickup line cache for this guild, or all guilds.',
		guild_ids=TESTING_GUILD_ID,
		force_global=SLASH_COMMANDS_GLOBAL
	)
  async def reshuffle_command(self, interaction: nextcord.Interaction, reshuffle_all: bool = False):
    await interaction.response.defer()
    
    if reshuffle_all:
      
      # Loop through all guilds' pickup cache
      for message_bank in self.bot.pickup_message_banks.keys():
        message_bank.reshuffle()

      # Loop through all guilds' breakup cache
      for message_bank in self.bot.breakup_message_banks.keys():
        message_bank.reshuffle()

      # Send a success message
      await interaction.response.send(util.get_message('jcwyt.reshuffle_global_success'), ephemeral=True)
    else:

      # Get the guild's caches
      message_banks = (self.bot.pickup_message_banks[interaction.guild_id], self.bot.breakup_message_banks[interaction.guild_id])
      
      # Reshuffle them
      map(lambda message_bank: message_bank.reshuffle(), message_banks)
      
      # Send a success message
      await interaction.response.send(util.get_message('jcwyt.reshuffle_guild_success'), ephemeral=True)

def setup(bot):
  bot.add_cog(ReshuffleCommand(bot))