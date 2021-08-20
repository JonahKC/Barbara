import lib.meese as meese
import config.config as config
from discord.ext import commands
from discord.channel import DMChannel


class RemoveMeese(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()  # @bot.event for Cogs
    async def on_message(self, message):
        if isinstance(message.channel, DMChannel):
            return
        if message.author.id != self.bot.user.id and message.author.id != 798016639089901610:  # botwinkle is that ID
            if config.read(message.guild.id, "nomees") == "true":
                if ":meese:" in message.content.lower():
                    foo = message.content
                    await message.delete()
                    await self.bot.get_channel(864644173835665458).send(
                        message.author.name + ": " + foo
                    )  # report in meese deletes
                else:
                    string = message.content.lower()
                    whitelist = config.fetch(message.guild.id, "whitelist")
                    for i in whitelist:
                        string = string.replace(i, "")
                    if meese.containsMeese(string):
                        await message.delete()
                        await self.bot.get_channel(864644173835665458).send(
                            message.author.name + ": " + message.content
                        )  # report in meese deletes


def setup(bot):
    bot.add_cog(RemoveMeese(bot))
