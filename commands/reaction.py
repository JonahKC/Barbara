import util
import nextcord
from nextcord.ext import commands
from nextcord.errors import HTTPException
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class ReactionCommand(commands.Cog):
  """
  Add/remove reactions from messages.
  """
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(
    name="reaction",
    description="Have Barbara add or remove reactions from the previous message.",
    guild_ids=TESTING_GUILD_ID,
    force_global=SLASH_COMMANDS_GLOBAL,
  )
  async def reaction(self, ctx):
    pass

  @reaction.subcommand(
    name="add",
    description="Adds a reaction to the previous message.",
  )
  async def reaction_add_command(self, interaction: nextcord.Interaction, reaction: str):
    """
    Add a reaction to the previous message
    """

    # Tell Discord we've acknowledged the Interaction
    # make the "bot is thinking" message client-only
    await interaction.response.defer(ephemeral=True)

    # Find the message to react to
    message_to_react = (await interaction.channel.history(limit=1).flatten())[0]
    try:

      # Add the specified reaction to the message
      await message_to_react.add_reaction(reaction)

      # Send a client-only success message
      await interaction.send("Successfully added reaction!", ephemeral=True)
      await self.bot.logger.log(interaction.guild_id,'reaction',subaction='added',user=interaction.user, interaction=interaction)
    except HTTPException:

      # Send a message that only the slash command sender can see (ephemeral)
      # saying that the reaction was invalid
      await interaction.send(content=f"Invalid Reaction: {str(reaction)}", ephemeral=True)


  @util.admin()
  @reaction.subcommand(
    name="clear",
    description="Removes all reactions from the previous message.",
  )
  async def reaction_remove_command(self, interaction: nextcord.Interaction):
    """
    Remove Barbara's reactions from the previous message
    """

    # Tell Discord we've acknowledged the Interaction
    # make the "bot is thinking" message client-only
    await interaction.response.defer(ephemeral=True)

    # Attempt to unreact from everything
    try:
      ## Find the message to react to
      #message_to_unreact = (await interaction.channel.history(limit=1).flatten())[0]

      ## Find all the reactions Barbara added
      #reactions_to_unreact = filter(lambda x: x.me, message_to_unreact.reactions)

      ## Go through each one and remove it
      #for reaction in reactions_to_unreact:

      #  # Remove Barbara's reaction
      #  await reaction.remove(self.bot.user)

      # Clear all reactions
      await (await interaction.channel.history(limit=1).flatten())[0].clear_reactions()

      # Send a client-only success message
      await interaction.followup.send("Successfully removed reactions!", ephemeral=True)
      await self.bot.logger.log(interaction.guild_id,'reaction',subaction='removed',user=interaction.user,interaction=interaction)
    except Exception as e:

      # Send a client-only error message
      await interaction.followup.send("Error encountered: " + e.__name__, ephemeral=True)

  @nextcord.message_command(
    name="Thumbsdown",
    guild_ids=TESTING_GUILD_ID,
    force_global=SLASH_COMMANDS_GLOBAL,
  )
  async def add_thumbsdown_message_command(self, interaction: nextcord.Interaction, message: nextcord.Message):
    """
    Right click a message to have Barbara react with a thumbsdown
    """

    # Send the "bot is thinking..." message to confirm that we got the Interaction
    await interaction.response.defer(ephemeral=True)

    # Add the reaction to the message
    await message.add_reaction("👎")
    await self.bot.logger.log(interaction.guild_id,'reaction',subaction='added',user=interaction.user, interaction=interaction)

    # Send a success message
    await interaction.followup.send("Added reaction!", ephemeral=True)

  @nextcord.message_command(
    name="Thumbsup",
    guild_ids=TESTING_GUILD_ID,
    force_global=SLASH_COMMANDS_GLOBAL,
  )
  async def add_thumbsup_message_command(self, interaction: nextcord.Interaction, message: nextcord.Message):
    """
    Right click a message to have Barbara react with a thumbsup
    """

    # Send the "bot is thinking..." message to confirm that we got the Interaction
    await interaction.response.defer(ephemeral=True)

    # Add the reaction to the message
    await message.add_reaction("👍")
    await self.bot.logger.log(interaction.guild_id,'reaction',subaction='added',user=interaction.user, interaction=interaction)

    # Send a success message
    await interaction.followup.send("Added reaction!", ephemeral=True)

def setup(bot):
  bot.add_cog(ReactionCommand(bot))