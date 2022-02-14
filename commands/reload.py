import os
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
    name='reload',
    description='[ㅈ] Reload a Cog.',
    
    # Only available in the JCWYT Discord, always not globally
    guild_ids=TESTING_GUILD_ID
  )
  async def reload_cog_command(
    self,
    interaction: nextcord.Interaction,
    cog: str=nextcord.SlashOption(
      required=True,
      name='cog',
      description='The name of the Cog to reload.',
      autocomplete=True
    )
  ):
    """
    Reload a Cog by name
    """

    try:

      # Attempt to reload the Cog
      self.bot.reload_extension(cog)

    # If there's an error loading the Cog
    except Exception as err:
      
      # Send an error message
      await interaction.send(util.get_message('jcwyt.reload_cog_failed', cog_name=cog, error_name=type(err).__name__, error_message=str(err)), ephemeral=True)
    
    # If there's not an error,
    else:

      # Send a success message
      await interaction.send(util.get_message('jcwyt.reload_cog_succeeded', cog_name=cog), ephemeral=True)
  
  @reload_cog_command.on_autocomplete('cog')
  async def reload_cog_command_autocomplete(self, interaction: nextcord.Interaction, cog: str):
  
    cog_names = []

    # os.walk through every file in the commands folder
    for root, dirs, files in os.walk('commands'):
      
      # For each file in the folder
      for file in files:
        
        # If the file is a .py file
        if file.endswith('.py'):
          
          # Get the name of the Cog
          cog_names.append('commands.'+os.path.splitext(file)[0])

    # os.walk through every file in the commands folder
    for root, dirs, files in os.walk('extensions'):
      
      # For each file in the folder
      for file in files:
        
        # If the file is a .py file
        if file.endswith('.py'):
          
          # Get the name of the Cog
          cog_names.append('extensions.'+os.path.splitext(file)[0])

    await interaction.response.send_autocomplete(cog_names)

def setup(bot):
  bot.add_cog(ReloadCommand(bot))