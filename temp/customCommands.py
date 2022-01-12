from discord.ext import commands
class CustomCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(name="dummycommand")
  async def dummy(self, ctx):
    await ctx.send("mega brain")
def setup(bot):
  bot.add_cog(CustomCommands(bot))