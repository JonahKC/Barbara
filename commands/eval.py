import io
import sys
import util
import inspect
import textwrap
import nextcord
from nextcord.ext import commands
from contextlib import redirect_stdout, redirect_stderr
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class EvalCommand(commands.Cog):
  """
	Run code compiled at runtime.
	"""
  def __init__(self, bot):
    self.bot = bot
    self._last_result = None

  def cleanup_code(self, content):
    """
    Remove single/multiline codeblocks if they exist
    """

    # If there's a ``` at the beginning and end of content
    if content.startswith('```') and content.endswith('```'):

      # Remove the first and last lines (which will remove the ```(py))
      return '\n'.join(content.split('\n')[1:-1])

    # Otherwise just remove newlines and single `
    return content.strip('` \n')

  def get_syntax_error(self, err):
    """
    Format syntax errors in a way that's easy-ish to debug
    """
    
    # If there's a line of code the error originated on
    if hasattr(err, 'text'):

      # Point to where the error is, and then describe it
      return f'```py\n{err.text}{"^":>{err.offset}}\n{err.__class__.__name__}: {err}```'

    # Otherwise just describe it
    return f'```py\n{err.__class__.__name__}: {err}\n```'

  @util.jcwyt()
  @nextcord.slash_command(
		name='eval',
		description='Evaluate an expression as code.',
    guild_ids=TESTING_GUILD_ID,
    force_global=SLASH_COMMANDS_GLOBAL,
	)
  async def eval_command(self, interaction: nextcord.Interaction, code: str):
    """
		Run code compiled at runtime.
		"""

    # Local and Global variables to use
    env = {
      'bot': self.bot,
      'interaction': interaction,
      'channel': interaction.channel,
      'user': interaction.user,
      'guild': interaction.guild,
      'message': interaction.message,
      '_': self._last_result,
      'nextcord': nextcord,
      'console': sys.stdout
    }
    env.update(globals())

    code = self.cleanup_code(code)

		# Wrap code in a function we can call
    to_compile = f'async def func():\n{textwrap.indent(code, " ")}'

    # Seperate STDOUT and STDERR
    out = io.StringIO()
    err = io.StringIO()

    # Redirect console output to our two variables
    with redirect_stdout(out), redirect_stderr(err):
      try:

        # Compile the code
        async_func = compile(to_compile, "<user code>", 'exec')

				# Execute code and await it if needed
        if inspect.isawaitable(async_func):
          await exec(async_func, env)
        else:
          exec(to_compile, env)
        
        # Run the compiled function
        await env['func']()
			
			# For some reason stderr doesn't always redirect
      except Exception as e:

        # Report the error
        err.write(self.get_syntax_error(e))

    # Program has actually returned something
    has_output = False

    # If terminal output exists
    if out.getvalue() != '':

      # Send it
      await interaction.send(out.getvalue())

      # Program just returned, so let's update the variable
      has_output = True


    # If STDERR output exists
    if err.getvalue() != '':

      # Send it as well
      await interaction.send(err.getvalue())

      # Program just returned, so let's update the variable
      has_output = True

    # Always return something so discord doesn't throw a fit
    if not has_output:
      await interaction.send(util.get_message('eval.default_output'),ephemeral=True)

def setup(bot):
  bot.add_cog(EvalCommand(bot))
