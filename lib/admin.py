import config.config as config
import discord

RESTRICTED_COMMANDS = ("admin", "link set", "prefix", "message", "config") # Only admins can run these
NO_PERMS_MESSAGE = lambda ctx: f"You have insufficient permissions to run the command `{ctx.prefix}{ctx.command.name}`!"

JCWYT_TEAM = (437404651818582017, 797282028344573992, 738843304057372702)

def perms(ctx): # Does this user have admin perms?
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
  elif jcwytTeam(user.id): return True
  #Specifically mentioned as an admin user
  elif user.id in config.fetch(ctx.guild.id, "admin users"): return True
  else:
    # Loop through each role the user has, and check if it's an admin role
    for i in user.roles:
      if i.id in config.fetch(ctx.guild.id, "admin roles"):
        return True
  return False

def jcwytTeam(ctx): # Is this user on the JCWYT team?
  if type(ctx) == int:
    id = ctx
  elif type(ctx) == discord.ext.commands.Context:
    id = ctx.author.id
  else:
    raise TypeError(f'ctx requires a discord.Member, or a discord.ext.commands.Context object. It got passed a {str(type(ctx))}')
    return False
  if id in JCWYT_TEAM:
    return True
  return False