import lib.regexLib as meese
import config.config as config
from discord.ext import commands
import discord

class RemoveMeese(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.bot.MEESE_DELETED_MESSAGE = "{nomeese} Message flagged by ||meese|| detection. To learn more about the correct plural of moose, go to <https://moosenotmeese.org>. If you think this deletion is a bug, contact bugs@jcwyt.com or report it on the JCWYT Discord."
    self.bot.MEESE_DELETED_DM_MESSAGE = "{nomeese} Message flagged by ||meese|| detection. To learn more about the correct plural of moose, go to <https://moosenotmeese.org>. This is a DM however, so the message cannot be deleted. ||But know that you've commited a sin||"

  @commands.Cog.listener() # @bot.event for Cogs
  async def on_pre_message(self, message):
    if message.author == self.bot.user:
      return
    try:
      if not message.author.id in (798016639089901610, 870684721191981056, 863912165757026304): # prevent Botwinkle, Barb-Dev, and Barb getting mad
        if isinstance(message.channel, discord.channel.DMChannel):
          if meese.containsMeese(meese.replaceWords(config.load_global("whitelist"), message.content.lower(), "")):
            await message.reply(self.bot.MEESE_DELETED_DM_MESSAGE.replace('{nomeese}', str(discord.utils.get(self.bot.emojis, name='nomeese'))))
          return
        if config.read(message.guild.id, "nomees") == "true":
          string = meese.replaceWords(config.fetch(message.guild.id, "whitelist"), message.content.lower(), "")
          if meese.containsMeese(string):
            await message.reply(self.bot.MEESE_DELETED_MESSAGE.replace('{nomeese}', str(discord.utils.get(self.bot.emojis, name='nomeese'))))
            await message.delete()
            await self.bot.get_channel(864644173835665458).send(
              message.author.name + ": " + message.content.lower()
            )
    except (discord.errors.NotFound, discord.errors.HTTPException): pass

  @commands.Cog.listener()
  async def on_message_edit(self, before, message):
    if message.author == self.bot.user:
      return
    if isinstance(message.channel, discord.channel.DMChannel):
      await message.reply(self.bot.MEESE_DELETED_DM_MESSAGE.replace('{nomeese}', str(discord.utils.get(self.bot.emojis, name='nomeese'))))
      return
    try:
      if not message.author.id in (798016639089901610, 870684721191981056, 863912165757026304): # prevent Botwinkle, Barb-Dev, and Barb getting mad
        if config.read(message.guild.id, "nomees") == "true":
          string = meese.replaceWords(config.fetch(message.guild.id, "whitelist"), message.content.lower(), "")
          if meese.containsMeese(string):
            await message.reply(self.bot.MEESE_DELETED_MESSAGE.replace('{nomeese}', str(discord.utils.get(self.bot.emojis, name='nomeese'))))
            await message.delete()
            await self.bot.get_channel(864644173835665458).send(
              message.author.name + ": " + message.content.lower()
            ) # report in meese deletes
    except (discord.errors.NotFound, discord.errors.HTTPException): pass

def setup(bot):
  bot.add_cog(RemoveMeese(bot))