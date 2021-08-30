import humanize
import datetime as dt
from discord.ext import commands
import discord

class Age(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name='howoldis', invoke_without_command=True)
  async def howOldIs(self, ctx, user: discord.User=None, precision="imprecisely"):
    age = user.created_at - dt.datetime.now()
    name = user.name.capitalize().replace('_', r'\_').replace('*', r'\*')
    if precision in ("accurately", "precisely"):
      await ctx.send(f"{name} is {humanize.precisedelta(age)} old.")
    else:
      await ctx.send(f"{name} is {humanize.naturaldelta(age)} old.")

  @howOldIs.command(name='theserver')
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
  async def howOldIsYourMom(self, ctx, precision="imprecisely"):
    await ctx.send("""Younger than yours.```(•_•)\n( •_•)>⌐■-■\n(⌐■_■)```""")

  @howOldIs.command(name='me')
  async def howOldIsMe(self, ctx, precision="imprecisely"):
    await self.howoldami(ctx, precision)

  @commands.command(name='howoldami')
  async def howoldami(self, ctx, precision="imprecisely"):
    age = ctx.author.created_at - dt.datetime.now()
    if precision in ("accurately", "precisely"):
      await ctx.send(f"I don't know your real age, but your account is {humanize.precisedelta(age)} old")
    else:
      await ctx.send(f"I don't know your real age, but your account is {humanize.naturaldelta(age)} old")

def setup(bot):
  bot.add_cog(Age(bot))
