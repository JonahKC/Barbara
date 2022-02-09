import nextcord
import traceback
from console import fg
from nextcord.ext import commands

class ErrorHandler(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_application_command_error(self, err, interaction):

    # Happens sometimes. No idea why. Prob. not important
    if type(err) == nextcord.errors.NotFound:
      return

    trace = []

    # Get the tracebac,
    tb = err.__traceback__

    # Loop through it
    while tb is not None:

      # Add each entry to an object
      trace.append({
          
        # Cut off the very long file path at 22 characters
        "filename": tb.tb_frame.f_code.co_filename,
        "name": tb.tb_frame.f_code.co_name,
        "line": tb.tb_lineno
      })
      tb = tb.tb_next
    
    # Invert the whole thing
    trace = trace[::-1]

    # Find the first entry that's filename starts with /home/runner (the bot's directory)
    trace = nextcord.utils.find(lambda x: x["filename"].startswith("/home/runner"), trace)

    if hasattr(err, 'text'):
      err_message = err.text
    else:
      err_message = str(err)

    try:
      # Send an error message
      # trace[:1000] + (trace[1000:] and '...' automatically cuts off long tracebacks
      await interaction.send('\n'.join((
        f"There was an error running your command. To report this, send us an email at bugs@jcwyt.com, or let us know on the JCWYT Discord with this error:",
        f"Command: `/{interaction.data['name']}`",
        f"Error Name: `{type(err).__name__}`",
        f"Error Message: `{err_message if err_message is not None else 'None'}`",
        f"Error File: `{trace['filename']}`",
        f"Error Line: `{trace['line']}`"
      )))

    # If there's an error sending it, log it instead
    except:

      # Log the error to the console instead
      stack = traceback.extract_tb(err.__traceback__)
      print(fg.red+f'Error: {type(err).__name__}\nMessage: {err_message}\nStacktrace:')
      for i in stack.format():
        print(i)
      print('\n\nEnd of Stacktrace\n\n'+'-'*50+'\n\n'+fg.default)

def setup(bot):
  bot.add_cog(ErrorHandler(bot))