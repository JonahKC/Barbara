#import config.config as config
#from discord import VoiceChannel
from discord.ext import commands


class VCCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='vc')
    async def vc(ctx):
        await ctx.send("Feature not implemented yet.")

    ##@vc.command(name='ban-bots')
    ##async def vcBanBots(ctx, channel: VoiceChannel):
    ##	config.append(ctx.guild.id, "noBotVcs", channel.id)
    ##	await ctx.send(f"Succesfully banned bots from vc with id {channel.id}")

    #@vc.command(name='unban-bots')
    #async def vcUnbanBots(ctx, channel: VoiceChannel):
    #  config.remove(ctx.guild.id, "noBotVcs", channel.id)
    #  await ctx.send(f"Succesfully unbanned bots from vc with id {channel.id}")


def setup(bot):
    bot.add_cog(VCCommand(bot))
