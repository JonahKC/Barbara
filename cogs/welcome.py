from discord.ext import commands
from discord.utils import find, get
from discord import Embed
from textwrap import dedent

class JoinMessage(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def on_guild_join(self, guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        embed=Embed(title="Hi! I’m Barbara!", description=dedent(f"""
        Thanks for adding me to {guild.name}!
        Run `%help` to view all of my commands, and `%help admin` to set up my admin-y bits. Also, run `%config set nomees true` true to enable |||meese|| blocking (it’s disabled by default).
        If you need any help, go to https://barbara.jcwyt.com/
        {str(get(self.bot.emojis, name='nomeese'))}"""), color=0xd89522)
        await general.send(embed=embed)
  
def setup(bot):
  bot.add_cog(JoinMessage(bot))
