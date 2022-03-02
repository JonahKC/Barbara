import asyncio
import nextcord
import config
from nextcord.ext import commands
from lib.LCG import LCG
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class PickupCommand(commands.Cog):
  """
  Get a pickup line from a hand-curated list of 400+
  """
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(
    name="pickup",
    description="Responds with a random pickup line.",
    guild_ids=TESTING_GUILD_ID,
    force_global=SLASH_COMMANDS_GLOBAL,
  )
  async def pickup_command(self, interaction: nextcord.Interaction):

    guild_id = interaction.guild_id

    with open("./resources/pickup_lines.txt",'r') as fp:
      lines = fp.readlines()

      lcg_data = config.read(guild_id,"_pickup_lcg")
      try:
        lcg_data.pop("last_num")
      except KeyError:
        pass
      lcg = LCG(len(lines),**lcg_data)

      # Get the breakup line, and replace {author} with the command author's name
      last_num = config.read(guild_id,"_pickup_lcg").get("last_num")
      pickup_line_raw = lines[lcg.gen(last_num)]

			# Update stored lcg data
      lcg_data = {"seed":lcg.seed,"additive":lcg.additive,"coefficient":lcg.coefficient,"last_num":lcg.last_num}
      config.write(guild_id,"_pickup_lcg",lcg_data)

    # Split the pickup line into an array using {answer} as a delimiter
    pickup_line_array = pickup_line_raw.split("{answer}")

    # Send the first part of the pickup line and remove it from the array
    await interaction.send(pickup_line_array.pop(0).format(author=interaction.user.display_name))

    # Loop through the remaining pickup lines
    for pickup_line in pickup_line_array:
      try:
        
        # Wait for the author to respond with an answer
        answer = await self.bot.wait_for(event='message', check=lambda m: m.channel.id == interaction.channel_id and m.author.id == interaction.user.id, timeout=60.0)

      # User didn't respond. Just send the rest of the pickup. Who the hell cares.
      except asyncio.TimeoutError:
        pass
        
      # Send the pickup line, and format {answer_text} with the answer as well as
      # {author} with the author's name
      await interaction.send(pickup_line.format(answer_text=answer.content, author=interaction.user.display_name))

def setup(bot):
  bot.add_cog(PickupCommand(bot))