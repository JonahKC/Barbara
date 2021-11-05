import lib.messages as messages
import aiohttp
from discord.ext import commands
import discord, asyncio

class RandomMessageCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command() # %secret
  async def secret(self, ctx):
    await ctx.send((await messages.formatString(messages.iterated_secret(ctx),ctx)))

  @commands.group(name='pickup', invoke_without_command=True) # %pickup
  async def pickup(self, ctx):
    def check(m: discord.Message):
      return m.channel.id == ctx.channel.id
    pickup = await messages.formatString(messages.iterated_pickup(ctx), ctx)
    if "{answer}" in pickup:
      pickup = pickup.split("{answer}")
      pickupMsg = await ctx.send(pickup[0])
      try:
        for i in range(len(pickup) - 1):
          await self.bot.wait_for(event='message', check=check, timeout=60.0)
          await ctx.send(pickup[i + 1])
      except asyncio.TimeoutError:
        await pickupMsg.reply('\n'.join(pickup))
      return
    await ctx.send(pickup)

  @pickup.command(name='breakup') # %pickup breakup
  async def pickupBreakup(self, ctx):
    await ctx.send("Try using `%breakup` instead!")

  @commands.command(name='breakup') # %breakup
  async def breakup(self, ctx):
    def check(m: discord.Message):
      return m.channel.id == ctx.channel.id
    breakup = await messages.formatString(messages.iterated_breakup(ctx), ctx)
    if "{answer}" in breakup:
      breakup = breakup.split("{answer}")
      breakupMsg = await ctx.send(breakup[0])
      try:
        for i in range(len(breakup) - 1):
          await self.bot.wait_for(event='message', check=check, timeout=60.0)
          await ctx.send(breakup[i + 1])
      except asyncio.TimeoutError:
        await breakupMsg.reply('\n'.join(breakup))
      return
    await ctx.send(breakup)

  @commands.command() # %fact
 # @commands.cooldown(rate=1, per=600, type=commands.BucketType.user)
  async def fact(self, ctx):
    factMessage = await ctx.send("Loading...")
    async with aiohttp.ClientSession() as cs:
      async with cs.get(
          'https://uselessfacts.jsph.pl/random.json?language=en'
      ) as r:
        res = await r.json()
        await factMessage.edit(content=res['text'].replace("`", "'"))

  @commands.command() # %dadjoke
 # @commands.cooldown(rate=1, per=600, type=commands.BucketType.user)
  async def dadjoke(self, ctx):
    dadjokeMessage = await ctx.send("Loading...")
    async with aiohttp.ClientSession() as cs:
      async with cs.get('https://icanhazdadjoke.com/',
               headers={
                 'Accept':
                 'text/plain',
                 'User-Agent':
                 'Barabara the Discord bot'
               }) as r:
        res = await r.text(encoding='utf-8')
        await dadjokeMessage.edit(content=res)

def setup(bot):
  bot.add_cog(RandomMessageCommands(bot))