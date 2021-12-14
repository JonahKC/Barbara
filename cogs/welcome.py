from discord.ext import commands
from discord.utils import find, get
from textwrap import dedent

class JoinMessage(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_guild_join(self, guild):

    # Preferably, we'd send here (the system channel), but only if we have perms and it exists
    if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
        await guild.system_channel.send(dedent(f"""
        Hi everyone, I'm Barbara! Thank you for adding me to {guild.name}.
        Run `%help` to view all of my commands, and `%help admin` to set up my admin-y bits. Also, run `%meesedetect true` true to enable ||meese|| blocking (it’s disabled by default).
        If you need any help, go to <https://barbara.jcwyt.com/>
        {str(get(self.bot.emojis, name='barbara'))}"""))
    else:

      # Otherwise find #general and check for perms
      channel = find(lambda x: x.name == 'general',  guild.text_channels)
      if channel and channel.permissions_for(guild.me).send_messages:
        await channel.send(dedent(f"""
        Hi everyone, I'm Barbara! Thank you for adding me to {guild.name}.
        Run `%help` to view all of my commands, and `%help admin` to set up my admin-y bits. Also, run `%meesedetect true` true to enable ||meese|| blocking (it’s disabled by default).
        If you need any help, go to <https://barbara.jcwyt.com/>
        {str(get(self.bot.emojis, name='barbara'))}"""))
      else:

        # Nothing else has perms, loop through every channel and see if we have perms to send the welcome message in any of them
        for channel in guild.text_channels:
          if channel.permissions_for(guild.me).send_messages:
            await channel.send(dedent(f"""
            Hi everyone, I'm Barbara! Thank you for adding me to {guild.name}.
            Run `%help` to view all of my commands, and `%help admin` to set up my admin-y bits. Also, run `%meesedetect true` true to enable ||meese|| blocking (it’s disabled by default).
            If you need any help, go to <https://barbara.jcwyt.com/>
            {str(get(self.bot.emojis, name='barbara'))}"""))
            break

def setup(bot):
  bot.add_cog(JoinMessage(bot))
