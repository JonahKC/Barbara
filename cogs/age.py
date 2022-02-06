import humanize
from datetime import timedelta, datetime
from discord.ext import commands
import discord

SCHOOL_DAYS_OFF = 16

class Age(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name='howoldis', invoke_without_command=True)
  async def howOldIs(self, ctx, user: discord.User=None, precision="imprecisely"):
    age = user.created_at - datetime.now()
    name = user.name.capitalize().replace('_', r'\_').replace('*', r'\*')
    if precision in ("accurately", "precisely"):
      await ctx.send(f"{name} is {humanize.precisedelta(age)} old.")
    else:
      await ctx.send(f"{name} is {humanize.naturaldelta(age)} old.")

  @howOldIs.command(name='theschoolyear')
  async def howOldIsTheSchoolYear(self, ctx, precision="imprecisely"):
    fromDate = datetime(2021, 9, 1, 8, 45)
    rawAge = datetime.now() - datetime(2021, 9, 1, 8, 45)
    daygenerator = (fromDate + timedelta(x + 1) for x in range((datetime.now() - fromDate).days + 1))
    weekdays = sum(1 for day in daygenerator if day.weekday() < 5) - SCHOOL_DAYS_OFF
    if precision in ("accurately", "precisely"):
      await ctx.send(f"The SPS School Year:\nThe school year started `{humanize.precisedelta(rawAge)}` ago.\nThere have been `{weekdays} school days`")
    else:
      await ctx.send(f"The SPS School Year:\nThe school year started `{humanize.naturaldelta(rawAge)}` ago.\nThere have been `{weekdays} school days`")		

  @howOldIs.command(name='theserver')
  async def howOldIsTheServer(self, ctx, precision="imprecisely"):
    age = datetime.now() - ctx.guild.created_at
    if precision in ("accurately", "precisely"):
      await ctx.send(f"This server is {humanize.precisedelta(age)} old.")
    else:
      await ctx.send(f"This server is {humanize.naturaldelta(age)} old.")

  @howOldIs.command(name='barbara')
  async def howOldIsBarbara(self, ctx, precision="imprecisely"):
    age = self.bot.user.created_at - datetime.now()
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
    age = ctx.author.created_at - datetime.now()
    if precision in ("accurately", "precisely"):
      await ctx.send(f"I don't know your real age, but your account is {humanize.precisedelta(age)} old")
    else:
      await ctx.send(f"I don't know your real age, but your account is {humanize.naturaldelta(age)} old")

def setup(bot):
  bot.add_cog(Age(bot))
