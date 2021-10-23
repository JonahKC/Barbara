from discord.ext import commands
from discord.utils import find, get
from textwrap import dedent

class JoinMessage(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def on_guild_join(self, guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(dedent(f"""
        Hi everyone, I'm Barbara! Thank you for adding me to {guild.name}.
        Run `%help` to view all of my commands, and `%help admin` to set up my admin-y bits. Also, run `%config set nomees true` true to enable ||meese|| blocking (it’s disabled by default).
        If you need any help, go to <https://barbara.jcwyt.com/>
        {str(get(self.bot.emojis, name='barbara'))}"""))
  
def setup(bot):
  bot.add_cog(JoinMessage(bot))
