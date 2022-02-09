import util
import nextcord
from nextcord.ext import commands

class Permissions(commands.Cog):
  """
	Permissions manager for Barbara. Ties in with util.py's admin/jcwyt decorator
	"""
  def __init__(self, bot):
    self.bot = bot

  # This is for permissions
  # Called every time the bot receives an Interaction (for example, a slash command)
  @commands.Cog.listener()
  async def on_interaction(self, interaction: nextcord.Interaction):

    # If the Interaction type is a slash command
    if interaction.type == nextcord.InteractionType.application_command:

      # If the command is in the list of admin commands
      if interaction.data['name'] in util.admin_commands:

        # If the user is NOT an admin
        if not util._has_permissions(interaction.user):

          # Send the no permissions message
          await interaction.send(
            util.get_message('admin.user_not_admin'), ephemeral=True)

          # And then stop the command from running
          return

      # If the command is in the list of JCWYT-only commands
      elif interaction.data['name'] in util.jcwyt_commands:

        # If the user is NOT a JCWYT user
        if not interaction.user.id in util.JCWYT_TEAM:

          # Send the no permissions message
          await interaction.send(
            util.get_message('admin.user_not_jcwyt'), ephemeral=True)

          # And then stop the command from running
          return

      try:

        # If there's permissions to run the command, run it
        await self.bot.process_application_commands(interaction)
      except Exception as err:

        # Send out a custom event for the error handler
        self.bot.dispatch("application_command_error", err, interaction)

def setup(bot):
  bot.add_cog(Permissions(bot))