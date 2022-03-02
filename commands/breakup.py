import asyncio
import nextcord
import config
from nextcord.ext import commands
from lib.LCG import LCG
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class BreakupCommand(commands.Cog):
  """
  Get a breakup line from a hand-curated list of 400+
  """
  def __init__(self, bot):
    self.bot = bot


  @nextcord.slash_command(
    name="breakup",
    description="Responds with a random breakup line.",
    guild_ids=TESTING_GUILD_ID,
    force_global=SLASH_COMMANDS_GLOBAL,
  )
  async def breakup_command(self, interaction: nextcord.Interaction):

    guild_id = interaction.guild_id

    with open("./resources/breakup_lines.txt",'r') as breakup_file:
      breakups = breakup_file.readlines()

      lcg_data = config.read(guild_id,"_breakup_lcg")
      try:
        lcg_data.pop("last_num")
      except KeyError:
        pass
      lcg = LCG(len(breakups),**lcg_data)

    # Get the breakup line, and replace {author} with the command author's name
      last_num = config.read(guild_id,"_breakup_lcg").get("last_num")
      breakup_line_raw = breakups[lcg.gen(last_num)]

			# Update stored lcg data
      lcg_data = {"seed":lcg.seed,"additive":lcg.additive,"coefficient":lcg.coefficient,"last_num":lcg.last_num}
      config.write(guild_id,"_breakup_lcg",lcg_data)

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