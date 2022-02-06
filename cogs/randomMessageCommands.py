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

  @commands.group(name='pickup', invoke_without_command=True)
  async def pickup(self, ctx):
    """Sends a random pickup line in the author's channel. Supports pickup lines that have responses"""
    
    # Make sure that the author of the message is the author of the entire command
    def check(m: discord.Message):
      return m.channel.id == ctx.channel.id
  
    # Get a random pickup line using messages.py (snippet below)
    pickup = await messages.formatString(messages.iterated_pickup(ctx), ctx)
  
    # Check to see if the pickup line is one that needs a response
    if "{answer}" in pickup:
    
      # If so, split the pickup line into all of it's parts
      pickup = pickup.split("{answer}")
  
      # Send the first part of the pickup line
      pickupMsg = await ctx.send(pickup[0])
  
      try:
        
        # For each of the other pickups
        for i in range(len(pickup) - 1):
        
          # Wait for a response from the author
          await self.bot.wait_for(event='message', check=check, timeout=60.0)
  
          # Send the next part of the pickup line
          await ctx.send(pickup[i + 1])
  
      # If the author doesn't respond in time
      except asyncio.TimeoutError:
      
        # Reply to the original message with the complete pickup line
        await pickupMsg.reply('\n'.join(pickup))
      return
  
    # If the pickup line doesn't need a response, just send it
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
  #@commands.cooldown(rate=1, per=600, type=commands.BucketType.user)
  async def fact(self, ctx):
    factMessage = await ctx.send("Loading...")
    async with aiohttp.ClientSession() as cs:
      async with cs.get(
          'https://uselessfacts.jsph.pl/random.json?language=en'
      ) as r:
        res = await r.json()
        await factMessage.edit(content=res['text'].replace("`", "'"))

  @commands.command() # %dadjoke
  #@commands.cooldown(rate=1, per=600, type=commands.BucketType.user)
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