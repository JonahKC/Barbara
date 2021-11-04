# Some of this code yoinked from RoboDanny (https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py)

from discord.ext import commands
from contextlib import redirect_stdout
import inspect
import lib.admin as admin
import io, textwrap, traceback
import lib.evalUtils as evalUtils

class EvalCommand(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_result = None
    self.sessions = set()

  def cleanup_code(self, content):
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    return content.strip('` \n')

  def get_syntax_error(self, e):
    if e.text is None:
      return f'```py\n{e.__class__.__name__}: {e}\n```'
    return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

  @commands.check(admin.jcwytTeam)
  @commands.command(name='eval')
  async def _eval(self, ctx, *, body: str):
    env = {
      'bot': self.bot,
      'ctx': ctx,
      'channel': ctx.channel,
      'author': ctx.author,
      'guild': ctx.guild,
      'message': ctx.message,
      '_': self._last_result,
      'in_each_channel': evalUtils.in_each_channel
    }

    env.update(globals())

    body = self.cleanup_code(body)
    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, " ")}'

    try:
      code = compile(to_compile, '<User Code>', 'exec')
      if inspect.isawaitable(code):
        await exec(code, env)
      else:
        exec(to_compile, env)
    except Exception as e:
      return await ctx.send(f'```py\n{e.__class__.__name__}: {e}  \n```')

    func = env['func']
    try:
      with redirect_stdout(stdout):
        ret = await func()
    except Exception as e:
      value = stdout.getvalue()
      await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
      value = stdout.getvalue()
      try:
        await ctx.message.add_reaction('\u2705')
      except:
        pass

      if ret is None:
        if value:
          await ctx.send(f'```\n{value}\n```')
      else:
        self._last_result = ret
        await ctx.send(f'```\n{value}{ret}\n```')

def setup(bot):
 bot.add_cog(EvalCommand(bot))