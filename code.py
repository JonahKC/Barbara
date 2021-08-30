from discord.ext import commands

class RuntimeFile(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
	
  async def main(self):
    guild = await self.bot.fetch_guild(863919587825418241)
    print(guild)

def setup(bot):
  bot.add_cog(RuntimeFile(bot))