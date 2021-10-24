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

  @commands.group(name='say', invoke_without_command=True) # %say
  async def say(self, ctx, *, content: str):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
      await ctx.message.delete()
    if perms(ctx):
      await ctx.send(content)
    else:
      await ctx.send(ctx.author.mention + ": " + content)

  @say.command(name='in')
  async def sayIn(self, ctx, channelID: int, *, content: str):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
      await ctx.message.delete()
    if perms(ctx):
      await self.bot.get_channel(channelID).send(content)
    else:
      await ctx.send('in' + content)

  @say.command(name='button')
  async def button(self, ctx, url: str, urlLabel: str, *, content: str):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
      await ctx.message.delete()
    if perms(ctx):
      await ctx.send(content, components=[Button(style=ButtonStyle.URL, label=urlLabel, url=url)])
    else:
      await ctx.send(ctx.author.mention + ": " + content,components=[Button(style=ButtonStyle.URL,label=urlLabel,url=url)])


def setup(bot):
  bot.add_cog(MessageSendingCommands(bot))