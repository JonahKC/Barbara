import lib.messages as messages
import config.config as config
import aiohttp
from discord.ext import commands
import discord, asyncio


class RandomMessageCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command() # %secret
  async def secret(self, ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
      await ctx.send(
        messages.random_message(messages.flavorOfSecret("normal")), ctx)
      return
    await ctx.send(
      messages.random_message(
        messages.flavorOfSecret(
          config.read(ctx.guild.id, "flavor-of-secrets")), ctx))

  @commands.command()
  async def secrets(self, ctx):
    secretsMessage = await ctx.send("Gathering all secrets...")
    secrets = ["All Secrets:"]
    with open(messages.MESSAGE_PATHS['botwinkle']) as s:
      secrets += s.readlines()
    with open(messages.MESSAGE_PATHS['jokesonyoubot']) as s:
      secrets += s.readlines()
    with open(messages.MESSAGE_PATHS['normal']) as s:
      secrets += s.readlines()
    secretsMessageText = "".join(secrets)
    await secretsMessage.edit(secretsMessageText[:1993] + (secretsMessageText[1993:] and '...'))

  @commands.group(name='pickup', invoke_without_subcommand=False) # %pickup
  async def pickup(self, ctx):
    def check(m: discord.Message):
      return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
    pickup = messages.iterated_pickup(ctx)
    if "{answer}" in pickup:
      pickup = pickup.split("{answer}")
      pickupMsg = await ctx.send(pickup.pop(0))
      try:
        for pickupLine in pickup:
          await self.bot.wait_for(event='message', check=check, timeout=60.0)
          await ctx.send(pickup.pop(0))
      except asyncio.TimeoutError:
        await pickupMsg.reply('\n'.join(pickup))
      return
    await ctx.send(pickup)

  @pickup.command(name='breakup') # %breakup
  async def breakup(self, ctx):
    def check(m: discord.Message):
      return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
    breakup = messages.iterated_breakup(ctx)
    if "{answer}" in breakup:
      breakup = breakup.split("{answer}")
      breakupMsg = await ctx.send(breakup.pop(0))
      try:
        for breakupLine in breakup:
          await self.bot.wait_for(event='message', check=check, timeout=60.0)
          await ctx.send(breakup.pop(0))
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
