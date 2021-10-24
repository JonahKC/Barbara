import config.config as config
import re, json
from discord.ext import commands
import discord

class ConfigCommand(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  def fancifyCfg(self, cfg):
    processedConf = "**All Config Options:**\n"
    processedConf += '```json\n' + json.dumps(cfg, indent=2) + '```'
    processedConf += '\n'
    return processedConf

  @commands.group(name='config', aliases=['cfg'], invoke_without_subcommand=False)
  async def config(self, ctx): pass # %config

  @config.command(name='read') # %config read or %config read [property]
  async def configRead(self, ctx, property=None):
    if isinstance(ctx.channel, discord.channel.discord.channel.DMChannel):
      await ctx.send(str(config.default()))
      return
    if property is None:
      conf = config.get(ctx.guild.id)
      conf = self.fancifyCfg(conf)
      conf = re.sub('<@([&!](\d+))>', '<\\\\@\\1>', str(conf))
      conf = re.sub('@everyone', '\\\\@ everyone', str(conf))
      await ctx.send(conf)
    else:
      await ctx.send(self.fancifyCfg(config.read(ctx.guild.id, property)))

  @config.command(name='set')
  async def configSet(self, ctx, property: str, value: str):
    if isinstance(ctx.channel, discord.channel.DMChannel):
      await ctx.send("Sorry, config in DMs is not supported.")
      return
    try:
      value = int(value)
    except ValueError:
      pass
    result = config.write(ctx.guild.id, property, value)
    if result == None:
      await ctx.send(f"Set config value `{property}` to `{value}`.")
    else:
      await ctx.send(result) # When the value doesn't exist, this is an error

  @config.command(name='reset')
  async def configReset(self, ctx, property: str):
    if isinstance(ctx.channel, discord.channel.DMChannel):
      await ctx.send("Sorry, config in DMs is not supported.")
      return
    result = config.reset(ctx.guild.id, property)
    if result != None: await ctx.send(result)
    else: await ctx.send(f"Succesfully reset config option {property}")

  @config.command(name='append', aliases=['add', 'push'])
  async def configAppend(self, ctx, arr: str, value):
    if isinstance(ctx.channel, discord.channel.DMChannel):
      await ctx.send("Sorry, config in DMs is not supported.")
      return
    try:
      value = int(value)
    except (TypeError, ValueError):
      pass
    result = config.append(ctx.guild.id, arr, value)
    if result != None:
      await ctx.send(result)
      return
    await ctx.send(f"Appended config value `{value}` to `{arr}`.")

  @config.command(name='remove', aliases=['splice'])
  async def configRemove(self, ctx, arr: str, value: str):
    if isinstance(ctx.channel, discord.channel.DMChannel):
      await ctx.send("Sorry, config in DMs is not supported.")
      return
    result = config.remove(ctx.guild.id, arr, value)
    if result != None:
      await ctx.send(result)
      return
    await ctx.send(f"Removed config value `{value}` from `{arr}`.")

  @commands.group(name='link',aliases=['info','about'], invoke_without_command=True) # %link
  async def link(self, ctx, ):
    link = config.read(ctx.guild.id, "link").replace(
      "{prefix}", ctx.prefix
    ) # read the link message for this server, and replace the text {prefix} with the bot's prefix.
    if link.replace(" ", "") != "":
      await ctx.send(link)

  @link.command(name='set') # %link set
  async def setLink(
    self,
    ctx, *,
    arg=""
  ):
    config.write(ctx.guild.id, "link", arg)
    await ctx.send(f"Set link to {arg}")

  @commands.command(name='meesedetect') # %meesedetect
  async def meesedetect(self, ctx, toggle: bool):
    result = config.write(ctx.guild.id, "nomees", str(toggle).lower())
    if result == None:
      await ctx.send(f"Set config value `nomees` to `{toggle}`.")
    else:
      await ctx.send(result)

def setup(bot):
  bot.add_cog(ConfigCommand(bot))