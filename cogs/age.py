import humanize
import datetime as dt
from discord.ext import commands


class Age(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name='howoldis')
  async def howOldIs(self, ctx):
    pass

  @howOldIs.command(name='theserver')
  @commands.guild_only()
  async def howOldIsTheServer(self, ctx, precision="imprecisely"):
    age = dt.datetime.now() - ctx.guild.created_at
    if precision in ("accurately", "precisely"):
      await ctx.send(f"This server is {humanize.precisedelta(age)} old.")
    else:
      await ctx.send(f"This server is {humanize.naturaldelta(age)} old.")

  @howOldIs.command(name='barbara')
  async def howOldIsBarbara(self, ctx, precision="imprecisely"):
    age = self.bot.user.created_at - dt.datetime.now()
    if precision in ("accurately", "precisely"):
      await ctx.send(f"I'm {humanize.precisedelta(age)} old.")
    else:
      await ctx.send(f"I'm {humanize.naturaldelta(age)} old.")
  
  @howOldIs.command(name='yourmom', aliases=['urmom', 'joe', 'joseph', 'joemama', 'yomama', 'josephmother'])
  async def howOldIsYourMom(self, ctx):
    await ctx.send("""Younger than yours.```(•_•)\n( •_•)>⌐■-■\n(⌐■_■)```""")

def setup(bot):
  bot.add_cog(Age(bot))
