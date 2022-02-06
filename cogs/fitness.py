import lib.voiceLib as vc
from discord.ext import commands
import discord
from asyncio import sleep
from textwrap import dedent

class Fitness(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name='fitness')
  async def fitness(self, ctx):
    await ctx.send(dedent("""
		The FitnessGram Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues. The 15 meter pacer test will begin in 30 seconds. Line up at the start. The running speed starts slowly, but gets faster each minute after you hear this signal. [beep] A single lap should be completed each time you hear this sound. [ding] Remember to run in a straight line, and run as long as possible. The second time you fail to complete a lap before the sound, your test is over. The test will begin on the word start. On your mark, get ready, start."""))
    if(ctx.author.voice):
      try:
        await vc.join(ctx)
        await sleep(1)
        await vc.play(ctx, 'fitnessgram-pacer-test.mp3', True)
        await vc.leave(ctx)
      except discord.ClientException:
        await ctx.send(f"Sorry, I'm already in a vc ({ctx.voice_client.channel.name}) and cannot play The FitnessGram Pacer Test.")
  
def setup(bot):
  bot.add_cog(Fitness(bot))