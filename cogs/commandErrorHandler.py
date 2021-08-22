from discord.ext import commands
from datetime import timedelta
from humanize import naturaldelta
from sys import stderr
from math import ceil
import lib.help as libHelp

import discord, traceback


class ErrorHandler(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

# Slightly modified from https://gist.github.com/AileenLumina/510438b241c16a2960e9b0b014d9ed06
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    # if command has local error handler, return
    if hasattr(ctx.command, 'on_error'):
      return

    # get the original exception
    error = getattr(error, 'original', error)

    if isinstance(error, commands.CommandNotFound):
      return

    if isinstance(error, commands.BotMissingPermissions):
      missing = [
        perm.replace('_', ' ').replace('guild', 'server').title()
        for perm in error.missing_perms
      ]
      if len(missing) > 2:
        fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
      else:
        fmt = ' and '.join(missing)
        _message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
      await ctx.send(_message)
      return

    if isinstance(error, commands.DisabledCommand):
      await ctx.send('This command has been disabled.')
      return

    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send("This command is on cooldown, please retry in {}.".format(naturaldelta(timedelta(seconds=ceil(error.retry_after)))))
      return

    if isinstance(error, commands.MissingPermissions):
      missing = [
        perm.replace('_', ' ').replace('guild', 'server').title()
        for perm in error.missing_perms
      ]
      if len(missing) > 2:
        fmt = '{}, and {}'.format("**, **".join(missing[:-1]),missing[-1])
      else:
        fmt = ' and '.join(missing)
        _message = 'You need the **{}** permission(s) to use this command.'.format(
        fmt)
      await ctx.send(_message)
      return

    if isinstance(error, commands.UserInputError):
      await ctx.send(f"Invalid syntax for command `{ctx.prefix}{ctx.command}`.")
      await ctx.send(libHelp.helpText(ctx))
      return

    if isinstance(error, commands.NoPrivateMessage):
      try:
        await ctx.author.send('This command cannot be used in direct messages.')
      except discord.Forbidden:
        pass
      return

    if isinstance(error, commands.CheckFailure):
      await ctx.send("You do not have permission to use this command.")
      return

    # ignore all other exception types, but print them to stderr
    print('Ignoring exception in command {}:'.format(ctx.command), file=stderr)
    await ctx.send(f"An unknown error was encountered executing the command `{ctx.prefix}{ctx.command}`: ```{error}```Please report bugs you find on the JCWYT Discord (<https://jcwyt.com/discord>), or email bugs@jcwyt.com")

    traceback.print_exception(type(error), error, error.__traceback__, file=stderr)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
