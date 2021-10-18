from discord.ext import commands
import discord
from discord_components import (
    Button,
    ButtonStyle,
)
from lib.admin import perms
from lib.customErrors import ArgumentsInvalid
import config.config as config
import lib.regexLib as meese


class MessageSendingCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='say') # %say
    async def say(self, ctx,*, content: str):
      if config.read(ctx.guild.id, "nomees") == "true":
        if ":meese:" in ctx.message.content.lower():
          await ctx.message.reply(self.bot.MEESE_DELETED_MESSAGE.replace('{nomeese}', str(discord.utils.get(self.bot.emojis, name='nomeese'))))
          await ctx.message.delete()
          await self.bot.get_channel(864644173835665458).send(
            ctx.author.name + ": " + ctx.message.content.lower()
          ) # report in meese deletes
          return
        else:
          string = meese.replaceWords(config.fetch(ctx.guild.id, "whitelist"), ctx.message.content.lower(), "")
          if meese.containsMeese(string):
            await ctx.message.reply(self.bot.MEESE_DELETED_MESSAGE.replace('{nomeese}', str(discord.utils.get(self.bot.emojis, name='nomeese'))))
            await ctx.message.delete()
            await self.bot.get_channel(864644173835665458).send(
              ctx.author.name + ": " + ctx.message.content.lower()
            )
            return
      if isinstance(ctx.channel, discord.channel.DMChannel):
        if ctx.message.content.startswith(f"{ctx.prefix}say button"):
            await self.button(ctx, content)
        elif perms(ctx):
            await ctx.send(content)
        else:
            await ctx.send(ctx.author.mention + ": " + content)
        return
      if ctx.message.content.startswith(f"{ctx.prefix}say button"):
        await ctx.message.delete()
        await self.button(ctx, content)
        return
      elif perms(ctx):
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
            try:
              await ctx.send(messageContent, components=[Button(style=ButtonStyle.URL, label=linkTitle, url=link)])
            except Exception as e:
            	await ctx.send(repr(e))
        else:
            try:
              await ctx.send(ctx.author.mention + ": " + messageContent,components=[Button(style=ButtonStyle.URL,label=linkTitle,url=link)])
            except Exception as e:
              await ctx.send(repr(e))


def setup(bot):
    bot.add_cog(MessageSendingCommands(bot))
