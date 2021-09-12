import lib.messages as messages
import config.config as config
import aiohttp
from discord.ext import commands
from discord.channel import DMChannel


class RandomMessageCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command() # %secret
  async def secret(self, ctx):
    if isinstance(ctx.channel, DMChannel):
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

  @commands.Cog.listener()
  async def on_message(
    self, message
  ): # honestly I don't really understand this code myself, but it allows for pickup lines to have replies
    global previous_pickup_data
    try:
      if previous_pickup_data[1] == message.author.id:
        await message.channel.send(
          previous_pickup_data[0][previous_pickup_data[2]])
        if len(previous_pickup_data[0]) - 1 == previous_pickup_data[2]:
          previous_pickup_data = ["", 000000000000000000, 1]
          return
        previous_pickup_data[2] += 1
    except NameError:
      previous_pickup_data = ["", 000000000000000000, 1]

  @commands.command() # %pickup
  async def pickup(self, ctx):
    global previous_pickup_data
    pickup = messages.random_message(messages.MESSAGE_PATHS["pickup"], ctx)
    if "{answer}" in pickup:
      pickup = pickup.split("{answer}")
      await ctx.send(pickup[0])
      previous_pickup_data = [
        pickup, ctx.author.id, previous_pickup_data[2]
      ]
      return
    await ctx.send(pickup)

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
                 'Barabara / 2.0.0 Barbara the Discord bot'
               }) as r:
        res = await r.text(encoding='utf-8')
        await dadjokeMessage.edit(content=res)


def setup(bot):
  bot.add_cog(RandomMessageCommands(bot))
