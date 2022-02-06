import nextcord
import config
import util
from nextcord.ext import commands

class Logger(commands.Cog):
  def __init__(self,bot):
    bot.logger = self
    self.bot = bot

  async def log(self, guild_id: int, action: str, **kwargs):
    channel_id = config.read(guild_id, 'log channel')
    allowed_actions = config.read(guild_id, 'log actions')
    if channel_id == 0 or not action in allowed_actions:
      return
    else:
      action = action.replace(' ','_')
      channel = self.bot.get_channel(channel_id)
      message = util.get_message(f'log.{action}',**kwargs)
      await channel.send(message)

def setup(bot):
  bot.add_cog(Logger(bot))