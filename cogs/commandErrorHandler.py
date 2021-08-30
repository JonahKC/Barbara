from discord.ext import commands
from datetime import timedelta
from humanize import naturaldelta
from math import ceil

import discord, traceback, console


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
      await ctx.send(f"Invalid syntax for command `{ctx.prefix}{ctx.command}`.\nIf you don't know the syntax, try `%help` or `%help admin`, and if the syntax isn't listed there go to <https://barbara.jcwyt.com>")
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
    #print('Ignoring exception in command {}:'.format(ctx.command))
    trace = []
    tb = error.__traceback__
    while tb is not None:
      trace.append({
          "filename": tb.tb_frame.f_code.co_filename,
          "name": tb.tb_frame.f_code.co_name,
          "line": tb.tb_lineno
      })
      tb = tb.tb_next
    errorMsg = f"An unknown error was encountered executing command `{ctx.prefix}{ctx.command}`: ```Error: {type(error).__name__}\nMessage: {str(error)[:500] + (str(error)[500:] and '...')}\nTraceback: {trace[-25:]}```Please report bugs you find on the JCWYT Discord (<https://jcwyt.com/discord>), or email bugs@jcwyt.com"
    errorMsg = errorMsg[:1992] + (errorMsg[1992:] and '...')
    await ctx.send(errorMsg)

    #traceback.print_exception(type(error), error, error.__traceback__, file=stderr)
    stack = traceback.extract_tb(error.__traceback__)
    print(console.fg.red+f'Error: {str(error)}')
    for i in stack.format():
      print(i)
    print('\n\nEnd of Stacktrace\n\n'+'-'*50+'\n\n'+console.fg.default)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
