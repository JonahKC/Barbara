import json
import traceback
from console import fg
from nextcord.ext import commands

class ErrorHandler(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_application_command_error(self, err, interaction):

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

    # Convert the object to a formatted JSON string, for readability
    # use only the first three tracebacks
    trace = json.dumps(trace[0:3], indent=2)

    if hasattr(err, 'message'):
      err_message = err.message
    else:
      err_message = str(err)

    # Send an error message
    # trace[:1000] + (trace[1000:] and '...' automatically cuts off long tracebacks
    await interaction.send('\n'.join((
      f"Sorry sweetie, there was an unhandled exception running the command `/{interaction.data['name']}`",
      f"Error Name: `{type(err).__name__}`",
      f"Error Message: `{err_message}`",
      f"Traceback:```json\n{trace}\n```",
      f"Report bugs to us at bugs@jcwyt.com, or on the JCWYT Discord",
    )), ephemeral=False)

    # Log the error to the console
    #stack = traceback.extract_tb(err.__traceback__)
    #print(fg.red+f'Error: {type(err).__name__}\nMessage: {err_message}\nStacktrace:')
    #for i in stack.format():
    #  print(i)
    #print('\n\nEnd of Stacktrace\n\n'+'-'*50+'\n\n'+fg.default)


def setup(bot):
  bot.add_cog(ErrorHandler(bot))