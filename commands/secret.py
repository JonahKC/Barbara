import asyncio
import nextcord
from nextcord.ext import commands
import lib.random_msg as random_msg
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class SecretCommand(commands.Cog):
  """
  Get a secret from Barbara's list of secrets
  """
  def __init__(self, bot):
    self.bot = bot
    self.bot.secret_message_banks = {}

  @commands.Cog.listener()
  async def on_ready(self):
    self.bot.secret_message_banks = random_msg.create_message_bank_for_every_server(
      self.bot.guilds, "./resources/barbara_secrets.txt", "s-")

  @nextcord.slash_command(
    name="secret",
    description="Responds with a secret from a hand-curated list",
    guild_ids=TESTING_GUILD_ID,
    force_global=SLASH_COMMANDS_GLOBAL,
  )
  async def secret_command(self, interaction: nextcord.Interaction):

    # Get the secret line, and replace {author} with the command author's name
    secret_line_raw = self.bot.secret_message_banks[
      interaction.guild_id].get_random_message()

    # Split the secret line into an array using {answer} as a delimiter
    secret_line_array = secret_line_raw.split("{answer}")

    # Send the first part of the secret line and remove it from the array
    await interaction.send(secret_line_array.pop(0).format(author=interaction.user.display_name))

    # Loop through the remaining secret lines
    for secret_line in secret_line_array:
      try:
        # Wait for the author to respond with an answer
        answer = await self.bot.wait_for(event='message', check=lambda m: m.channel.id == interaction.channel_id and m.author.id == interaction.user.id, timeout=60.0)

      # User didn't respond. Just send the rest of the secret. Who the hell cares.
      except asyncio.TimeoutError:
        pass
        
      # Send the secret line, and format {answer_text} with the answer as well as
      # {author} with the author's name
      await interaction.send(secret_line.format(answer_text=answer.content, author=interaction.user.display_name))

def setup(bot):
  bot.add_cog(SecretCommand(bot))