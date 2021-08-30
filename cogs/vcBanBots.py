from discord.ext import commands
import config.config as config
from discord import VoiceChannel

class VCBanBots(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name='vc', invoke_without_command=True) # invoke_without_command makes it so this command doesn't run when there's a subcommand
  async def vc(self, ctx):
    await ctx.send("You must have either `ban-bots` or `unban-bots` as a subcommand.")

  @vc.command(name='ban-bots')
  async def vcBanBotsCommand(self, ctx, vc: VoiceChannel=None):
    if not vc:
      vc = ctx.author.voice.channel
    if vc.id in config.fetch(ctx.guild.id, "banned-vcs"):
      await ctx.send(f"Sorry, vc {vc.name} is already listed as a bot-banned vc.")
    else:
      config.append(ctx.guild.id, "banned-vcs", vc.id)
      await ctx.send(f"Banned bots from vc {vc.name}")

  @vc.command(name='unban-bots')
  async def vcUnbanBots(self, ctx, vc: VoiceChannel=None):
    if not vc:
      vc = ctx.author.voice.channel
    if vc.id in config.fetch(ctx.guild.id, "banned-vcs"):
      config.remove(ctx.guild.id, "banned-vcs", vc.id)
      await ctx.send(f"Unbanned bots from vc {vc.name}")
    else:
      await ctx.send(f"Sorry, vc {vc.name} is not listed as a bot-banned vc, and you cannot unban it.")

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    try:
      if member.voice.channel.id in config.fetch(member.guild.id, "banned-vcs") and member.bot and not member == self.bot.user:
          await member.edit(voice_channel=None)
    except AttributeError:
      pass

def setup(bot):
  bot.add_cog(VCBanBots(bot))