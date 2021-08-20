import config.config as config
import discord # Two different imports are needed, because discord.ext.commands is like a different module or something
from discord.ext import commands

class BasicCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.group(name='admin', invoke_without_subcommand=False)
  async def admin(self, ctx): # This command doesn't exist, you need to reference a subcommand.
    pass

  @admin.group(name='add') # %admin add
  async def adminAdd(self, ctx):
    pass

  @adminAdd.command(name='role') # %admin add role
  async def adminAddRole(self, ctx, role: discord.Role):
    config.append(ctx.guild.id, "admin roles", role.id)

  @adminAdd.command(name='user') # %admin add user
  async def adminAddUser(self, ctx, user: discord.User):
    config.append(ctx.guild.id, "admin roles", user.id)

  @admin.group(name='list') # %admin list
  async def adminList(self, ctx):
    pass

  @adminList.command(name='roles') # %admin list roles
  async def adminListRoles(self, ctx):
    roles = config.read(ctx.guild.id, "admin roles")
    roles_temp = []
    print(roles)
    print(ctx.guild.roles)
    for i in roles:
    	if i == '@everyone':
    		roles_temp.append('@ everyone')
    	else:
    		roles_temp.append(ctx.guild.get_role(int(i[3:-1])).name)
    await ctx.send('**ADMIN ROLES:**\n'+'\n'.join(roles_temp))

  @adminList.command(name='users') # %admin list users
  async def adminListUsers(self, ctx):
    users = config.read(ctx.guild.id, "admin users")
    users_temp = []
    for i in users:
      print(int(i[3:-1]))
      print(self.bot.get_user(int(i[3:-1])))
      print(self.bot.get_user(437404651818582017))
      users_temp.append(self.bot.get_user(int(i[3:-1])).name)
    await ctx.send('\n'.join(users_temp))
  
  @admin.group(name='remove') # %admin remove
  async def adminRemove(self, ctx):
    pass

  @adminRemove.command(name='role') # %admin remove role
  async def adminRemoveRole(self, ctx, role: discord.Role):
    config.remove(ctx.guild.id, "admin roles", role.id)

  @adminRemove.command(name='user') # %admin remove user
  async def adminRemoveUser(self, ctx, user: discord.User):
    config.remove(ctx.guild.id, "admin users", user.id)

def setup(bot):
    bot.add_cog(BasicCommands(bot))