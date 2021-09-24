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

  @channel.command(name='rename', aliases=['ren'])
  async def channelRename(self, ctx, channelToRename: typing.Optional[typing.Union[discord.TextChannel, discord.VoiceChannel]], newName: str):
    if ctx.author.voice.channel != None and channelToRename == None:
      channelToRename = ctx.author.voice.channel
    else:
      await ctx.send("Sorry, you must specify a channel to rename, or be in a channel.")
      return
    oldName = channelToRename.name
    if admin.perms(ctx):
        await channelToRename.edit(reason=f'{ctx.author.name} edited channel {channelToRename.name}\'s name to {newName}.', name=newName)
    else:
      if channelToRename.id in config.fetch(ctx.guild.id, 'publicly-renameable-channels'):
        await channelToRename.edit(reason=f'{ctx.author.name} edited channel {channelToRename.name}\'s name to {newName}.', name=newName)
      else:
        await ctx.send("Sorry, you don't have the require permissions and the channel is not marked as publicly renameable.")
        return
    await ctx.send(f"Succesfully renamed channel `{oldName}` to `{channelToRename.name}`.")

def setup(bot):
  bot.add_cog(ChannelCommand(bot))