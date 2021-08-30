from discord.ext import commands
from discord.channel import DMChannel
import lib.regexLib as rl
import config.config as config
import lib.admin as admin
import re

class RemoveNSFW(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.nsfwMsgs = []
  
  @commands.Cog.listener()
  async def on_message(self, message):
    try:
      if config.read(message.guild.id, "react-to-the-string-nsfw") == "true":
        processedMessage = re.sub(rl.trim_regex, '', message.content.lower()).replace("react-to-the-string-nsfw", "").replace("nsfw-detection-reactions", "")
        if "nsfw" in processedMessage:
          self.nsfwMsgs.append(message)
          for e in config.read(message.guild.id, "nsfw-detection-reactions"):
            await message.add_reaction(e)
    except AttributeError:
      pass

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if not isinstance(self.bot.get_channel(payload.channel_id), DMChannel) and payload.event_type == 'REACTION_ADD' and admin.perms(payload.member) and payload.emoji in config.read(payload.guild_id, "nsfw-detection-reactions"): # Not a DM, not removing a reaction, user is admin, and emoji is in config list of emojis to react to messages with the string 'nsfw'
      await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id).delete()

def setup(bot):
  bot.add_cog(RemoveNSFW(bot))