import util
import nextcord
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class SayCommand(commands.Cog):
  """
	Have Barbara say a specific message.
  """
  def __init__(self, bot):
    self.bot= bot
	
  @nextcord.slash_command(
		name = "say",
		description = "Have Barbara say a message.",
		guild_ids = TESTING_GUILD_ID,
		force_global = SLASH_COMMANDS_GLOBAL,
	)
  async def say_command(self, interaction: nextcord.Interaction, message: str=nextcord.SlashOption(description='Message to say.')):

    # Don't send an empty message
    if message != '':

      # Replace @everyone and @here with @ everyone and @ here
      message = message.replace("@everyone", "@ everyone").replace("@here", "@ here")

		  # User is an admin
      if util._has_permissions(interaction.user):

				# Send message in channel
        await interaction.channel.send(message)
      
				# Send a success message
        await interaction.send(util.get_message("say.success"), ephemeral=True)
      else:

				# Send message in channel with reply
        await interaction.send(message)
    else:

			# Tell them off for giving me an empty string
      await interaction.send(util.get_message('say.empty_string'), ephemeral=True)

def setup(bot):
  bot.add_cog(SayCommand(bot))