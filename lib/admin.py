import config.config as config

RESTRICTED_COMMANDS = ("admin", "link set", "prefix") # Only admins can run these
NO_PERMS_MESSAGE = lambda ctx: f"You have insufficient permissions to run the command `{ctx.prefix}{ctx.command.name}`!"

def perms(ctx): # Does this user have admin perms?
	if f'<@!{ctx.author.id}>' in config.fetch(ctx.guild.id, "admin users") or ctx.message.author.server_permissions.administrator:
		return True
	else:
		for i in ctx.user.roles:
			if f'<@&{i.id}>' in config.fetch(ctx.guild.id, "admin roles"):
				return True
	return False

def jcwytTeam(ctx): # Is this user on the JCWYT team?
  if ctx.author.id in (437404651818582017, 797282028344573992, 738843304057372702):
    return True
  else:
    return False