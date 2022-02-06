import config.config as config
import discord
from discord.ext import commands

class BasicCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name='admin', aliases=['sudo', 'owo'], invoke_without_subcommand=False)
  async def admin(self, ctx):
    pass

  @admin.group(name='add', aliases=['+'],invoke_without_subcommand=False)
  async def adminAdd(self, ctx):
    pass

  @adminAdd.command(name='role')
  async def adminAddRole(self, ctx, role: discord.Role):
    config.append(ctx.guild.id, "admin roles", role.id)
    await ctx.send(f"Promoted role {role.name} to admin.")

  @adminAdd.command(name='user')
  async def adminAddUser(self, ctx, user: discord.User):
    config.append(ctx.guild.id, "admin users", user.id)
    await ctx.send(f"Promoted user {user.name} to admin.")

  @admin.group(name='list', aliases=['='],invoke_without_subcommand=False)
  async def adminList(self, ctx):
    pass

  @adminList.command(name='roles')
  async def adminListRoles(self, ctx):
    roles = config.read(ctx.guild.id, "admin roles")
    roles_temp = []
    for i in roles:
    	if i == '@everyone':
    		roles_temp.append('@ everyone')
    	else:
    		roles_temp.append(ctx.guild.get_role(i).name)
    await ctx.send('**ADMIN ROLES:**\n'+'\n'.join(roles_temp))

  @adminList.command(name='users')
  async def adminListUsers(self, ctx):
    users = config.read(ctx.guild.id, "admin users")
    users_temp = []
    for i in users:
      user = await self.bot.fetch_user(i)
      users_temp.append(user.display_name.replace('_', '\_').replace('*', '\*'))
    await ctx.send('\n'.join(users_temp))

  @adminList.command(name='all',aliases=['*'])
  async def adminListAll(self, ctx):
    users = config.read(ctx.guild.id, "admin users")
    users_temp = []
    for i in users:
      user = await self.bot.fetch_user(i)
      users_temp.append(user.display_name)
    roles = config.read(ctx.guild.id, "admin roles")
    roles_temp = []
    for i in roles:
    	if i == '@everyone':
    		await ctx.send('Everyone on this server is an admin! The more the merrier!')
    		return
    	else:
    		roles_temp.append(ctx.guild.get_role(i))
    members = []
    for i in roles_temp:
      members += i.members
    members = list(set(members))
    for i in members:
      users_temp.append(i.display_name)
    users_temp = list(set(users_temp))
    await ctx.send('**All Admin Users:**\n'+'\n'.join(users_temp))
  
  @admin.group(name='remove', aliases=['-','delete','demote','rm', '0w0'],invoke_without_subcommand=False) # %admin remove
  async def adminRemove(self, ctx):
    pass

  @adminRemove.command(name='role',aliases=['r'])
  async def adminRemoveRole(self, ctx, role: discord.Role):
    config.remove(ctx.guild.id, "admin roles", role.id)

  @adminRemove.command(name='user',aliases=['u'])
  async def adminRemoveUser(self, ctx, user: discord.User):
    config.remove(ctx.guild.id, "admin users", user.id)

  @adminRemove.command(name='message', aliases=['uwu'])
  async def adminRemoveMessage(self, ctx, message: discord.Message):
    await message.delete()
    await ctx.message.delete()

def setup(bot):
    bot.add_cog(BasicCommands(bot))