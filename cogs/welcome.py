from discord.ext import commands
from discord.utils import find, get
from textwrap import dedent

class JoinMessage(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
        await guild.system_channel.send(dedent(f"""
        Hi everyone, I'm Barbara! Thank you for adding me to {guild.name}.
        Run `%help` to view all of my commands, and `%help admin` to set up my admin-y bits. Also, run `%config set nomees true` true to enable ||meese|| blocking (it’s disabled by default).
        If you need any help, go to <https://barbara.jcwyt.com/>
        {str(get(self.bot.emojis, name='barbara'))}"""))
    else:
      await find(lambda x: x.name == 'general',  guild.text_channels).send(dedent(f"""
        Hi everyone, I'm Barbara! Thank you for adding me to {guild.name}.
        Run `%help` to view all of my commands, and `%help admin` to set up my admin-y bits. Also, run `%config set nomees true` true to enable ||meese|| blocking (it’s disabled by default).
        If you need any help, go to <https://barbara.jcwyt.com/>
        {str(get(self.bot.emojis, name='barbara'))}"""))
  
def setup(bot):
  bot.add_cog(JoinMessage(bot))
