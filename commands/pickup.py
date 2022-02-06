import nextcord
from nextcord.ext import commands
import lib.random_msg as random_msg
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class PickupCommand(commands.Cog):
  """
  Get a pickup line from a hand-curated list of 400+
  """
  def __init__(self, bot):
    self.bot = bot
    self.bot.pickup_message_banks = {}

  @commands.Cog.listener()
  async def on_ready(self):
    self.bot.pickup_message_banks = random_msg.create_message_bank_for_every_server(
      self.bot.guilds, "./resources/pickup_lines.txt", "p-")

  @nextcord.slash_command(
    name="pickup",
    description="Responds with a pickup line from a hand-curated list of 400+",
    guild_ids=TESTING_GUILD_ID,
    force_global=SLASH_COMMANDS_GLOBAL,
  )
  async def pickup_command(self, interaction: nextcord.Interaction):

    # Get the pickup line, and replace {author} with the command author's name
    pickup_line_raw = self.bot.pickup_message_banks[
      interaction.guild_id].get_random_message()

    # Split the pickup line into an array using {answer} as a delimiter
    pickup_line_array = pickup_line_raw.split("{answer}")

    # Send the first part of the pickup line and remove it from the array
    await interaction.send(pickup_line_array.pop(0).format(author=interaction.user.display_name))

    # Loop through the remaining pickup lines
    for pickup_line in pickup_line_array:
      
      # Wait for the author to respond with an answer
      answer = await self.bot.wait_for(event='message', check=lambda m: m.channel.id == interaction.channel_id and m.author.id == interaction.user.id, timeout=60.0)

      # Send the pickup line, and format {answer_text} with the answer as well as
      # {author} with the author's name
      await interaction.send(pickup_line.format(answer_text=answer.content, author=interaction.user.display_name))

def setup(bot):
  bot.add_cog(PickupCommand(bot))