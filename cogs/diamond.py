import lib.voiceLib as vc
from discord.ext import commands
import discord
from asyncio import sleep
from re import match

class SweetCaroline(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  def isMe(self, m):
    return m.author == self.bot.user

  @commands.group(name='sweet', invoke_without_subcommand=False, aliases=['sweeet','sweeeet','sweeeeet','sweeeeeet','sweeeeeeet','sweeeeeeeet','sweeeeeeeeet'])
  async def sweet(self, ctx):
    pass

  @sweet.command(name='caroline')
  async def caroline(self, ctx):
    await ctx.message.delete()
    try:
      await vc.join(ctx)
      await sleep(1)
      await vc.play(ctx, 'neil-diamond-sweet-caroline.mp3')
      msg = await ctx.send("😉")
      await sleep(14)
      with open('./resources/sweet_caroline.txt') as file:
        for line in file:
          lineMatch = match(r"(?P<lyric>.*):(?P<time>\d*.\d*)",line)
          lyric = lineMatch.group("lyric")
          dur = lineMatch.group("time")
          await msg.edit(content=lyric.replace(r'\n', '\n'))
          await sleep(float(dur))
      await vc.leave(ctx)
    except Exception as e:
      if e.__class__ == AttributeError:
        await ctx.send("Try again in a voice call 😉")
      elif e.__class__ == discord.ClientException:
        await ctx.send(f"Sorry, I'm already in a vc ({ctx.voice_client.channel.name}).")
  
def setup(bot):
  bot.add_cog(SweetCaroline(bot))