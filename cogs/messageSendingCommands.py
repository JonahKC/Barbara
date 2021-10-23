from discord.ext import commands
import discord
from discord_components import (
  Button,
  ButtonStyle,
)
from lib.admin import perms

class MessageSendingCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name='say') # %say
  async def say(self, ctx, *, content: str):
    if isinstance(ctx.channel, discord.channel.DMChannel):
      if perms(ctx):
        await ctx.send(content)
      else:
        await ctx.send(ctx.author.mention + ": " + content)
      return
    elif perms(ctx):
      await ctx.message.delete()
      await ctx.send(content)
    else:
      await ctx.message.delete()
      await ctx.send(ctx.author.mention + ": " + content)

  async def button(self, ctx, url: str, urlLabel: str, *, content: str):
    if perms(ctx):
      await ctx.send(content, components=[Button(style=ButtonStyle.URL, label=urlLabel, url=url)])
    else:
      await ctx.send(ctx.author.mention + ": " + content,components=[Button(style=ButtonStyle.URL,label=urlLabel,url=url)])


def setup(bot):
  bot.add_cog(MessageSendingCommands(bot))