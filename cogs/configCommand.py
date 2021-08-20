import config.config as config
import re
from discord.ext import commands
from discord.channel import DMChannel


class ConfigCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='config', invoke_without_subcommand=False)
    async def config(self, ctx):  # %config
        pass

    @config.command(name='read')  # %config read or %config read [property]
    async def configRead(self, ctx, property=None):
        if isinstance(ctx.channel, DMChannel):
            await ctx.send(str(config.default()))
            return
        if property is None:
            conf = config.get(ctx.guild.id)
            conf = re.sub('<@([&!](\d+))>', '<\\\\@\\1>', str(conf))
            conf = re.sub('@everyone', '\\\\@ everyone', str(conf))
            await ctx.send(str(conf))
        else:
            await ctx.send(config.read(ctx.guild.id, property))

    @config.command(name='set')
    async def configSet(self, ctx, property: str, value: str):
        if isinstance(ctx.channel, DMChannel):
            await ctx.send("Sorry, config in DMs is not supported.")
            return
        config.write(ctx.guild.id, property, value)
        await ctx.send("Set config value.")


def setup(bot):
    bot.add_cog(ConfigCommand(bot))
