import util
from nextcord.ext import commands
from nextcord.utils import find, get

class Welcome(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_guild_join(self, guild):

    # Preferably, we'd send here (the system channel), but only if we have perms and it exists
    if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
        await guild.system_channel.send(util.get_message("guild.welcome", barbara=str(get(self.bot.emojis, name='barbara')), guild_name=guild.name))
    else:

      # Otherwise find #general and check for perms
      channel = find(lambda x: x.name == 'general',  guild.text_channels)
      if channel and channel.permissions_for(guild.me).send_messages:
        await channel.send(util.get_message("guild.welcome", barbara=str(get(self.bot.emojis, name='barbara')), guild_name=guild.name))
      else:

        # Nothing else has perms, loop through every channel and see if we have perms to send the welcome message in any of them
        for channel in guild.text_channels:
          if channel.permissions_for(guild.me).send_messages:
            await channel.send(util.get_message("guild.welcome", barbara=str(get(self.bot.emojis, name='barbara')), guild_name=guild.name))
            break

def setup(bot):
  bot.add_cog(Welcome(bot))