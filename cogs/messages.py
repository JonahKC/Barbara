from discord.ext import commands
import discord
import pandas as pd

class MessageDoer(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name='messages', aliases=['msg', 'monosodiumglutemate'], invoke_without_subcommand=False)
  async def messages(self, ctx): pass

  @messages.command(name='purge', aliases=['wipe', 'clear'])
  async def messagesPurge(self, ctx, limit: int=50, fromUser: discord.User=None):
    limit = min(limit, 200)
    def userCheck(msg):
      if fromUser == None: return True
      return msg.author.id == fromUser.id
    await ctx.channel.purge(limit=limit, check=userCheck, before=None, after=None)
    await ctx.send(f"Deleted up to {limit} messages from channel {ctx.channel.mention}{' by user {}'.format(fromUser.name) if fromUser else ''}", delete_after=30.0)

  @messages.command(name='collect', aliases=['acquire', 'gather'])
  async def messagesCollect(self, ctx, limit: int=50, fromUser: discord.User=None):
    msg = await ctx.send(f"Collecting up to {limit} messages from channel {ctx.channel}{' by user {}'.format(fromUser) if fromUser else ''}")
    if fromUser:
      data = pd.DataFrame(columns=['content', 'time'])
      async for m in ctx.channel.history(limit=limit):
        if m.author == fromUser:
          data.append({'content': m.content,'time': m.created_at}, ignore_index=True)
    else:
      data = pd.DataFrame(columns=['content', 'time', 'author'])
      async for m in ctx.channel.history(limit=limit):
        data = data.append({'content': m.content, 'time': m.created_at, 'author': m.author.name}, ignore_index=True)
    data.to_csv('./temp/collect.csv')
    await msg.reply("Collected messages!", file=discord.File('./temp/collect.csv'))

def setup(bot):
  bot.add_cog(MessageDoer(bot))