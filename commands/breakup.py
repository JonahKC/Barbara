import asyncio
import nextcord
from nextcord.ext import commands
import lib.random_msg as random_msg
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class BreakupCommand(commands.Cog):
  """
  Get a breakup line from a hand-curated list of 400+
  """
  def __init__(self, bot):
    self.bot = bot
    self.bot.breakup_message_banks = {}

  @commands.Cog.listener()
  async def on_ready(self):
    self.bot.breakup_message_banks = random_msg.create_message_bank_for_every_server(
      self.bot.guilds, "./resources/breakup_lines.txt", "b-")

  @nextcord.slash_command(
    name="breakup",
    description="Responds with a random breakup line.",
    guild_ids=TESTING_GUILD_ID,
    force_global=SLASH_COMMANDS_GLOBAL,
  )
  async def breakup_command(self, interaction: nextcord.Interaction):

    # Get the breakup line, and replace {author} with the command author's name
    breakup_line_raw = self.bot.breakup_message_banks[
      interaction.guild_id].get_random_message()

    # Split the breakup line into an array using {answer} as a delimiter
    breakup_line_array = breakup_line_raw.split("{answer}")

    # Send the first part of the breakup line and remove it from the array
    await interaction.send(breakup_line_array.pop(0).format(author=interaction.user.display_name))

    # Loop through the remaining breakup lines
    for breakup_line in breakup_line_array:
      
      try:
        # Wait for the author to respond with an answer
        answer = await self.bot.wait_for(event='message', check=lambda m: m.channel.id == interaction.channel_id and m.author.id == interaction.user.id, timeout=60.0)
      
      # User didn't respond. Just send the rest of the pickup. Who the hell cares.
      except asyncio.TimeoutError:
        pass

      # Send the pickup line, and format {answer_text} with the answer as well as
      # {author} with the author's name
      await interaction.send(breakup_line.format(answer_text=answer.content, author=interaction.user.display_name))

def setup(bot):
  bot.add_cog(BreakupCommand(bot))