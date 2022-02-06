import util
import config
import nextcord
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class VCBanBots(commands.Cog):
  """
  Ban or unban (music) bots from a VC.
  """
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(
    name="vc",
    description="Ban or unban (music) bots from a VC.",
    guild_ids = TESTING_GUILD_ID,
		force_global = SLASH_COMMANDS_GLOBAL,
  )
  async def vc(self, interaction: nextcord.Interaction):
    """
    Ban or unban (music) bots from a vc, kicking them as soon as they join.
    """
    pass

  @vc.subcommand(
    name='ban',
    description="Ban bots from a VC.",
  )
  async def vc_ban_bots_command(self, interaction: nextcord.Interaction, vc: nextcord.abc.GuildChannel=nextcord.SlashOption(name="vc", description="Voice channel to ban bots from.", required=False)):
    """
    Ban bots from a vc, kicking them as soon as they join.
    """

    # If the user mentions a vc, the string will start with #! so we have to remove it
    #if vc.startswith("#!"):
    #  vc = vc[2:]

    # Get the VoiceChannel object from the name
    #vc_object = nextcord.utils.find(lambda channel: channel.name == vc, interaction.guild.voice_channels)

    vc_object = vc

    # If you didn't specify a vc in the command
    if not vc_object:

      # Get the current channel you're in
      try:
        vc_object = interaction.user.voice.channel

      # If the user isn't in a vc
      except AttributeError:

        # Tell them that they need to specify a vc, or be in one
        await interaction.send(util.get_message("vc.not_in_channel"))
        
        # Stop the rest of the function from running
        return

    # If it's already banned
    if vc_object.id in config.fetch(interaction.guild_id, "banned-vcs"):
      
      # Send the already banned message
      await interaction.send(util.get_message("vc.already_banned", name=vc_object.name))
    else:

      # Otherwise add the vc id to the list of banned vcs
      try:
        config.append(interaction.guild_id, "banned-vcs", vc_object.id)
        await self.bot.logger.log(interaction.guild_id, "vc ban", subaction="banned",vc=vc_object,user=interaction.user)
      
      # If there's an error editing config
      except config.ConfigException as err:

        # Send the error message
        await interaction.send(err.__repr__())
        
        # And stop the rest of the function
        return

      # Send a success message
      await interaction.send(util.get_message("vc.success", name=vc_object.name))

  @vc.subcommand(
    name='unban',
    description="Unban bots from a VC.",
  )
  async def vc_unban_bots_command(self, interaction: nextcord.Interaction, vc: nextcord.abc.GuildChannel=nextcord.SlashOption(name="vc", description="Voice channel to ban bots from.", required=False)):
    """
    Unban bots from a vc, making them able to connect to the specified channel again.
    """

    # If the user mentions a vc, the string will start with #! so we have to remove it
    #if vc.startswith("#!"):
    #  vc = vc[2:]

    # Get the VoiceChannel object from the name
    #vc_object = nextcord.utils.find(lambda channel: channel.name == vc, interaction.guild.voice_channels)

    vc_object = vc

    # If you didn't specify a vc in the command
    if not vc_object:

      # Get the current channel you're in
      try:
        vc_object = interaction.user.voice.channel

      # If the user isn't in a vc
      except AttributeError:

        # Tell them that they need to specify a vc, or be in one
        await interaction.send(util.get_message("vc.not_in_channel"))
        
        # Stop the rest of the function from running
        return

    # If it's already banned
    if vc_object.id not in config.fetch(interaction.guild_id, "banned-vcs"):
      
      # Send the already banned message
      await interaction.send(util.get_message("vc.already_unbanned", name=vc_object.name))
    else:

      # Otherwise remove the vc id from the list of banned vcs
      try:
        config.remove(interaction.guild_id, "banned-vcs", vc_object.id)
        await self.bot.logger.log(interaction.guild_id, "vc ban", subaction="unbanned",vc=vc_object,user=interaction.user)
      
      # If there's an error editing config
      except config.ConfigException as err:

        # Send the error message
        await interaction.send(err.__repr__())
        
        # And stop the rest of the function
        return

      # Send a success message
      await interaction.send(util.get_message("vc.unban_success", name=vc_object.name))

  # When someone leaves/joins a vc
  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    try:

      # If the user is a bot, in a banned vc
      if member.voice.channel.id in config.fetch(member.guild.id, "banned-vcs") and member.bot:
        
        # Kick 'em
        await member.edit(voice_channel=None)

    # Maybe the user just left or something
    except AttributeError:

      # I couldn't care less
      pass

def setup(bot):
  bot.add_cog(VCBanBots(bot))