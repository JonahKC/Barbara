import lib.regexLib as meese
import config.config as config
from discord.ext import commands
import discord

class RemoveMeese(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.bot.MEESE_DELETED_MESSAGE = "{nomeese} Message flagged by ||meese|| detection. To learn more about the correct plural of moose, go to <https://moosenotmeese.org>. If you think this deletion is a bug, contact bugs@jcwyt.com or report it on the JCWYT Discord.\n{mention}"

  # Custom event that runs before on_message
  @commands.Cog.listener()
  async def on_pre_message(self, message):
    try:

      # Prevent bot conflicts
      if not message.author.bot:

        # Check if the config is set to delete meese
        if config.read(message.guild.id, "nomees") == "true":

          # Trim the message (removing filler chars etc.)
          trimmedMessage = meese.trim(message.content.lower())
          hasMeese = meese.containsMeese(trimmedMessage, config.fetch(message.guild.id, "whitelist"))
          if hasMeese:
            await message.channel.send(self.bot.MEESE_DELETED_MESSAGE.replace('{nomeese}', str(discord.utils.get(self.bot.emojis, name='nomeese'))).replace('{mention}', message.author.mention))
            await message.delete()
            await self.bot.get_channel(864644173835665458).send(
              message.author.name +
              ": ```\n" + message.content + "```\n" +
              "Message after processing: ```\n" + hasMeese + "```"
            )
    except (discord.errors.NotFound, discord.errors.HTTPException): pass

  @commands.Cog.listener()
  async def on_message_edit(self, before, message):
    if message.author == self.bot.user:
      return
    try:
      if not message.author.bot:
        if config.read(message.guild.id, "nomees") == "true":
          trimmedMessage = meese.trim(message.content.lower())
          hasMeese = meese.containsMeese(trimmedMessage, config.fetch(message.guild.id, "whitelist"))
          if hasMeese:
            await message.channel.send(self.bot.MEESE_DELETED_MESSAGE.replace('{nomeese}', str(discord.utils.get(self.bot.emojis, name='nomeese'))).replace('{mention}', message.author.mention))
            await message.delete()
            await self.bot.get_channel(864644173835665458).send(
              message.author.name + ": ```\n" + message.content + "```"
            )
    except (discord.errors.NotFound, discord.errors.HTTPException): pass

def setup(bot):
  meese.reloadMeeseBlacklist()
  bot.add_cog(RemoveMeese(bot))