from discord.ext import commands
from asyncio import sleep
from random import choice

# This is *not* the vc command 😉
class EasterEggsNStuff(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='wiggle', aliases=['wave'])
  async def wiggle(self, ctx):
    message = await ctx.send("¸")
    wave = "¸¸¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸¸¸¸"
    for i in range(0, len(wave)):
      await message.edit('`' + wave[i:i+4].replace('`', r'\`') + '`')
      await sleep(0.8)

  @commands.command(name='amogus', aliases=['amongus', 'whentheimposterissus', 'sus'])
  async def sussy(self, ctx):
    await ctx.send(""":black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:
:black_large_square::black_large_square::black_large_square::red_square::red_square::red_square::black_large_square::black_large_square::black_large_square::green_square::green_square::green_square::black_large_square:
:black_large_square::black_large_square::black_large_square::red_square::blue_square::blue_square::black_large_square::black_large_square::black_large_square::blue_square::blue_square::green_square::sweat_drops:
:black_large_square::black_large_square::black_large_square::red_square::red_square::red_square::knife::black_large_square::black_large_square::green_square::green_square::green_square::black_large_square:
:yellow_square::yellow_square::black_large_square::red_square::black_large_square::red_square::black_large_square::black_large_square::black_large_square::green_square::black_large_square::green_square::black_large_square:
:yellow_square::yellow_square::bone::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:""")

  @commands.command(name='everyminute', aliases=['slime', 'aminutewasted'])
  async def everyminute(self, ctx):
    await ctx.send("\"Every minute is a minute wasted of precious slime-hunting time.\" - The wisest man")

  @commands.group(name='dem', invoke_without_subcommand=False)
  async def dem(self, ctx):
    pass
  @dem.command(name='crops')
  async def demCrops(self, ctx):
    await ctx.send("stomping on the crops")

  @commands.command(name='alex', aliases=['fakealex', 'imposteralex'])
  async def realAlex(self, ctx):
    await ctx.send(choice(("we don't want the real alex", "FAKE, I CALL IMPOSTER")))

  @commands.command(name='dream', aliases=['dreamminecraft', 'dreammc', 'minecraft'])
  async def dream(self, ctx):
    await ctx.send("You mean Dream Minecraft SMP Speedrun World Record Manhunt???")

  @commands.command(name='jonah')
  async def jonah(self, ctx):
    await ctx.send(choice(("||moose||", "<https://jonahkc.com>", "<a:moose_party:866868789370159144>")))

  @commands.command(name='callum')
  async def callum(self, ctx):
    await ctx.send(choice(("nerd", "more like,,,, , ,, cool", "https://www.youtube.com/watch?v=ejc5zic4q2A")))

  @commands.command(name='baz', aliases=['foobarbaz'])
  async def fooBar(self, ctx):
    await ctx.send("zi")

  @commands.command(name='caroline')
  async def caroline(self, ctx):
     await ctx.send("o.0")

def setup(bot):
  bot.add_cog(EasterEggsNStuff(bot))