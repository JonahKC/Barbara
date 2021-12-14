from discord.ext import commands
import discord
import typing
import lib.admin as admin
import config.config as config

class ChannelCommand(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name='channel', invoke_without_subcommand=False)
  async def channel(self, ctx):
    pass

def setup(bot):
  bot.add_cog(ChannelCommand(bot))