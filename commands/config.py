import util
import json
import config
import nextcord
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class ConfigCommand(commands.Cog):
  """
  Commands for interfacing directly with a server's config
  """
  def __init__(self, bot):
    self.bot = bot

  @util.admin()
  @nextcord.slash_command(
		name='config',
		description='Directly read and modify the server config file.',
		guild_ids=TESTING_GUILD_ID,
		force_global=SLASH_COMMANDS_GLOBAL,
	)
  async def config_command(self, interaction: nextcord.Interaction):
    """
		Admin commands for interacting directly with the server config
    """
    pass

  @config_command.subcommand(
		name='read',
		description='Read the value of a config option, or all of config.'
	)
  async def config_read_command(self, interaction: nextcord.Interaction,
  
  # A specific config option is optional, if not provided will read the whole config
  option: str=nextcord.SlashOption(
    required=False,
    default=False,
  )):
    """
    Read the value of a specific config option.
    """
    try:

      # If you want a specific config option
      if option:

        # Send a formatted message with the option
        await interaction.send(util.get_message('config.read_success',option=option, value=config.read(interaction.guild_id, option)))
      else:

        # Otherwise send a formatted message with the entire config
        await interaction.send(util.get_message('config.entire_config_read_success', guild_name=interaction.guild.name, config_json=json.dumps(config.load(interaction.guild_id), indent=2)))  
    
    # Ruh roh you tried to read an option that doesn't exist or something
    except config.ConfigException as err:

      # Send whatever to error is since we're certainly not dealing with it
      await interaction.send(err.__repr__())
      

  @config_command.subcommand(
		name='set',
		description='Set the value of a config option.'
	)
  async def config_set_command(self, interaction: nextcord.Interaction, option: str, value):
    """
    Set the value of a config option. Get all configuration options by running /config read without a specific option
    """
    try:

      # Attempt to write value to option in the guild's config
      config.write(interaction.guild_id, option,value)

      # Send a success message
      await interaction.send(util.get_message('config.write_success', option=option, value=value))

    # If there's an error writing the config
    except config.ConfigException as err:

      # Send the error
      await interaction.send(err.__repr__())

  @config_command.subcommand(
	  name='reset',
		description='Reset a config option to the default value.'
	)
  async def config_reset_command(self, interaction: nextcord.Interaction, option: str):
    """
    Reset a config option to it's default. Get all configuration options by running /config read without a specific option
    """
    try:

      # Attempt to reset the config option to default
      config.reset(interaction.guild_id, option)

      # Send a success message
      await interaction.send(util.get_message('config.reset_success', option=option))

    # If there's an error resetting the config option
    except config.ConfigException as err:

      # Send the error
      await interaction.send(err.__repr__())

  @config_command.subcommand(
		name='append',
		description='Add an item to a config list.'
	)
  async def config_append_command(self, interaction: nextcord.Interaction, list: str, value):
    """
    Append a value to a list in config. Get all configuration options by running /config read without a specific option
    """
    try:

      # Attempt to append the value to the array in config
      config.append(interaction.guild_id, list, value)

      # Send a success message
      await interaction.send(util.get_message('config.append_success', arr=list, value=value))

    # If there's an error appending to the array
    except config.ConfigException as err:

      # Send it in string format
      await interaction.send(err.__repr__())

  @config_command.subcommand(
		name='remove',
		description='Remove an item from a config list.'
	)
  async def config_remove_command(self, interaction: nextcord.Interaction, list: str, value):
    """
    Remove a value from a config list. Get all configuration options by running /config read without a specific option
    """
    try:

      # Attempt to remove the value from the config array
      config.remove(interaction.guild_id, list, value)

      # Send a success message customized with the array name and the value appended
      await interaction.send(util.get_message('config.remove_success', arr=list, value=value))

    # Catch all errors appending to the config array
    except config.ConfigException as err:

      # Send the error
      await interaction.send(err.__repr__())

  @util.jcwyt()
  @config_command.subcommand(
    name='backup',
    description='[ㅈ] Backup all config to a file'
  )
  async def config_backup_command(self, interaction: nextcord.Interaction):
    config.backup()
    await interaction.send(util.get_message("jcwyt.config.backup_success"), ephemeral=True)

  @util.jcwyt()
  @config_command.subcommand(
    name='restore',
    description='[ㅈ] Restore all config from the most recent backup'
  )
  async def config_restore_command(self, interaction: nextcord.Interaction):
    config.revert()
    await interaction.send(util.get_message("jcwyt.config.revert_success"), ephemeral=True)

def setup(bot):
  bot.add_cog(ConfigCommand(bot))