import config.config as config
import lib.admin as admin
import lib.help as libHelp
from discord.ext import commands
import os

# Quick command explanation and syntax:
# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
# Cog explanation and syntax:
# https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html
# https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
# Subcommands syntax:
# https://github.com/Snaptraks/discord.py/blob/examples/examples/subcommands.py
# CommandError docs (used to check perms among other things)
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.CommandError

# Examples:
# https://github.com/AlexFlipnote/discord_bot.py


class BasicCommands(commands.Cog):
  def __init__(self, bot): # Allows us to access bot later on with self.bot
    self.bot = bot

  @commands.group(name='help',aliases=['h'])
  async def helpCommand(self, ctx): # %help
    if ctx.invoked_subcommand is not None: return
    await ctx.send(libHelp.helpText(ctx))

  @helpCommand.command(name='admin') # %help admin
  async def helpAdmin(self, ctx):
    with open('./resources/helpAdmin.txt') as helpText: # The help message is in a file now
      await ctx.send(helpText.read().replace("{prefix}", ctx.prefix)) # ctx.send() is shorthand for message.channel.send()

  @commands.command(name='invite') # %invite
  async def invite(self, ctx):
    await ctx.send(
      "**Invite Me to Your Other Discord Servers!**\n<https://barbara.jcwyt.com/invite>"
    )

  @commands.group(name='link',aliases=['info','about']) # %link
  async def link(self, ctx):
    link = config.read(ctx.guild.id, "link").replace(
      "{prefix}", ctx.prefix
    ) # read the link message for this server, and replace the text {prefix} with the bot's prefix.
    await ctx.send(link)

  @link.command(name='set') # %link set
  async def setLink(
    self,
    ctx,
    arg="Barbara is developed by JCWYT: <https://barbara.jcwyt.com>"
  ): # if you don't pass a link to set, it uses the default one
    config.write(ctx.guild.id, "link", arg)

  @commands.command(name='prefix') # %prefix !
  async def prefix(self, ctx, newPrefix: str):
    config.write(ctx.guild.id, "prefix", newPrefix)
    await ctx.send(f'My prefix is now \"{newPrefix}\"')

  @commands.command(name='reload',aliases=['cog','rld']) # %reload cogs.basicCommands
  @commands.check(admin.jcwytTeam)
  async def reloadCog(self, ctx, *, nameOfCog: str, stealthy="false"): # Reloads a Cog
    if stealthy == "true":
      await ctx.message.delete()
    try:
      self.bot.unload_extension(nameOfCog)
      self.bot.load_extension(nameOfCog)
    except Exception as e:
      await ctx.send(f'**ERROR:** `{type(e).__name__} - {e}`')
    else:
      await ctx.send(f'**SUCCESSFULLY RELOADED COG: **`{nameOfCog}`')
  @commands.command()
  async def ping(self, ctx):
   await ctx.send(f'Pong! 🏓\nPing: `{self.bot.latency} milliseconds`')

  @commands.command(name='restart')
  @commands.check(admin.jcwytTeam)
  @commands.guild_only()
  async def restartRepl(self, ctx): # Restarts the entire repl.
    shutdownMessage = await ctx.send("Shutting down bot...")
    sdRaw = open('./temp/shutdown-message.txt', 'w') # We want a "bot online again" message, so let's write the place that message should be in a file.
    sdRaw.write(str(shutdownMessage.channel.id))
    sdRaw.close()
    os.system('kill 1') # 1 is the main repl process, it autorestarts.
  
  @commands.Cog.listener()
  async def on_ready(self):
    try:
      sdRaw = open('./temp/shutdown-message.txt', 'r+') # Let's see if we need to send a message
      shutdownMessageData = sdRaw.read()
      sdRaw.truncate(0) # Delete contents so it doesn't send message next restart
      sdRaw.close()
      await self.bot.get_channel(int(shutdownMessageData)).send("Bot succesfully restarted!")
    except ValueError: # Repl didn't shutdown because of %restart
      pass

def setup(bot): # Builtin discord function
  bot.add_cog(BasicCommands(bot))
