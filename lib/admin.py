import config.config as config
import discord
from discord.ext import commands

# Admin commands
RESTRICTED_COMMANDS = ("meesedetect", "admin", "link set", "prefix", "messages", "config", "secrets") # Only admins can run these

# Message to send when no permissions
NO_PERMS_MESSAGE = lambda ctx: f"You have insufficient permissions to run the command `{ctx.prefix}{ctx.command.name}`!"

# All JCWYT Team members always have admin
JCWYT_TEAM = (437404651818582017, 797282028344573992, 738843304057372702)

# Does this user have admin perms?
def perms(ctx):
  if type(ctx) == discord.Member:
    user = ctx
  elif type(ctx) == discord.ext.commands.Context:
    if isinstance(ctx.channel, discord.channel.DMChannel):
      return False
    user = ctx.author
  else:
    raise TypeError(f'ctx requires a discord.Member, or a discord.ext.commands.Context object. It got passed a {str(type(ctx))}')
    return False
  # All admins are, well, admins
  if user.guild_permissions.administrator: return True
  #All JCWYT team members admin by default
  elif user.id in JCWYT_TEAM: return True
  #Specifically mentioned as an admin user
  elif user.id in config.fetch(ctx.guild.id, "admin users"): return True
  else:
    # Loop through each role the user has, and check if it's an admin role
    for i in user.roles:
      if i.id in config.fetch(ctx.guild.id, "admin roles"):
        return True
  return False

def jcwytTeam(): # Is this user on the JCWYT team?
  def predicate(ctx):
    if ctx.author.id in JCWYT_TEAM:
      return True
    if ctx.command == 'eval' and ctx.author.id == 397191449894060045:
      return True
    return False
  return commands.check(predicate)