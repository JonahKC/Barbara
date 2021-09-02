from discord.ext import commands
from discord_components import (
    Button,
    ButtonStyle,
)
from lib.admin import perms
from lib.customErrors import ArgumentsInvalid


class MessageSendingCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='say') # %say
    async def say(self, ctx,*, content: str):
        if ctx.message.content.startswith(f"{ctx.prefix}say button"):
            await self.button(ctx, content)
            return
        if perms(ctx):
            await ctx.message.delete()
            await ctx.send(content)
        else:
            await ctx.message.delete()
            await ctx.send(ctx.author.mention + ": " + content)

    async def button(self, ctx, content: str): 
        c = content.split(" ")
        cl = len(c)
        if cl < 3:
          raise ArgumentsInvalid(f"%say button requires at least 3 arguments. Got {cl - 1} argument{'s' if cl == 1 else ''}.")
        link = c[1]
        linkTitle = c[2]
        messageContent = " ".join(c[3:])
        if perms(ctx):
            await ctx.message.delete()
            try:
              await ctx.send(messageContent, components=[Button(style=ButtonStyle.URL, label=linkTitle, url=link)])
            except Exception as e:
            	await ctx.send(repr(e))
        else:
            await ctx.message.delete()
            try:
              await ctx.send(ctx.author.mention + ": " + messageContent,components=[Button(style=ButtonStyle.URL,label=linkTitle,url=link)])
            except Exception as e:
              await ctx.send(repr(e))


def setup(bot):
    bot.add_cog(MessageSendingCommands(bot))
