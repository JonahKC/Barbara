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
    if not ctx.author.voice:
      await ctx.send(";)")
      return
    msgsToDelete = []
    try:
      await vc.join(ctx)
      await sleep(1)
      vc.play(ctx, 'neil-diamond-sweet-caroline.mp3')
      with open('./resources/sweet_caroline.txt') as file:
        for line in file:
          lineMatch = match(r"(?P<lyric>.*):(?P<time>\d*.\d*)",line)
          lyric = lineMatch.group("lyric")
          dur = lineMatch.group("time")
          msgsToDelete.append(await ctx.send(lyric.replace(r'\n', '\n')))
          await sleep(float(dur))
      await vc.leave(ctx)
      await ctx.channel.purge(limit=len(msgsToDelete), check=self.isMe)
    except discord.ClientException:
      await ctx.send(f"Sorry, I'm already in a vc ({ctx.voice_client.channel.name}).")
  
def setup(bot):
  bot.add_cog(SweetCaroline(bot))