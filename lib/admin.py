import config.config as config
import discord

RESTRICTED_COMMANDS = ("admin", "link set", "prefix", "message", "config") # Only admins can run these
NO_PERMS_MESSAGE = lambda ctx: f"You have insufficient permissions to run the command `{ctx.prefix}{ctx.command.name}`!"

def perms(ctx): # Does this user have admin perms?
  if type(ctx) == discord.User:
    raise TypeError('ctx requires a discord.Member, or a discord.ext.commands.Context object. You passed it a discord.User')
  elif type(ctx) == discord.Member:
    #if guild_id == -1:
    #  raise TypeError('guild_id must be set to the ID of the discord guild when passing a User as ctx')
    #  return False
    user = ctx
  else:
    if isinstance(ctx.channel, discord.channel.DMChannel):
      return False
    user = ctx.author

  if f'<@!{user.id}>' in config.fetch(ctx.guild.id, "admin users"):
    return True
  else:
    for i in user.roles:
      if f'<@&{i.id}>' in config.fetch(ctx.guild.id, "admin roles"):
        return True
  return False

def jcwytTeam(ctx): # Is this user on the JCWYT team?
  if ctx.author.id in (437404651818582017, 797282028344573992, 738843304057372702):
    return True
  else:
    return False