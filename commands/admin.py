import nextcord
import config
import util
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class AdminCommand(commands.Cog):
  """
  Commands for managing admin users of the bot.
  """
  def __init__(self, bot):
    self.bot = bot

  @util.admin()
  @nextcord.slash_command(
    name="admin",
    description="Manage bot administrators.",
    guild_ids=TESTING_GUILD_ID,
    force_global=SLASH_COMMANDS_GLOBAL,
  )
  async def admin_command(self, interaction: nextcord.Interaction):
    """
    Admin commands for managing admin users of the bot.
    """
    pass

  @admin_command.subcommand(
    name="add",
    description="Add users or roles to the list of admins."
  )
  async def admin_add_command(self, interaction: nextcord.Interaction):
    """
    Add users, or roles to the list of admins
    """
    pass

  @admin_add_command.subcommand(
    name="user",
    description="Add a user to the list of admins."
  )
  async def admin_add_user_command(self, interaction: nextcord.Interaction, member: nextcord.Member):
    """
    Add a user to the list of admins
    """

    # Appent the member ID to the list of admins for the guild
    config.append(interaction.guild_id, "admin users", member.id)

    # Send a success message
    await interaction.send(f"Promoted user {member.display_name} to admin.")

  @admin_add_command.subcommand(
    name="role",
    description="Add a role to admin roles."
  )
  async def admin_add_role_command(self, interaction: nextcord.Interaction, role: nextcord.Role):
    """
    Add a role to admin roles
    """

    # Appent the member ID to the list of admins for the guild
    config.append(interaction.guild_id, "admin roles", role.id)

    # Send a success message
    await interaction.send(f"Promoted role {role.name} to admin.")

  @admin_command.subcommand(
    name="remove",
    description="Remove users or roles from the list of admins.",
  )
  async def admin_remove_command(self, interaction: nextcord.Interaction):
    """
    Remove users, or roles from the list of admins
    """
    pass

  @admin_remove_command.subcommand(
    name="user",
    description="Remove a user to the list of admins."
  )
  async def admin_remove_user_command(self, interaction: nextcord.Interaction, member: nextcord.Member):
    """
    Remove an individual user from the list of admins
    """

    # Remove the member ID from the list of admins for the guild
    config.remove(interaction.guild_id, "admin users", member.id)

    # Send a success message
    await interaction.send(f"Demoted user {member.display_name} from admin.")

  @admin_remove_command.subcommand(
    name="role",
    description="Remove a role from the list of admin."
  )
  async def admin_remove_role_command(self, interaction: nextcord.Interaction, role: nextcord.Role):
    """
    Remove a role from the list of admin roles
    """

    # Remove the member ID from the list of admins for the guild
    config.remove(interaction.guild_id, "admin roles", role.id)

    # Send a success message
    await interaction.send(f"Demoted role {role.name} from admin.")

  @admin_command.subcommand(
    name="list",
    description="List admin users and roles."
  )
  async def admin_list_command(self, interaction: nextcord.Interaction):
    """
    List admin users/roles
    """
    pass

  @admin_list_command.subcommand(
    name="roles",
    description="List manually set admin roles."
  )
  async def admin_list_roles_command(self, interaction: nextcord.Interaction):
    """
    List admin roles
    """

    # Read all admin roles
    roles = config.read(interaction.guild_id, "admin roles")
    roles_temp = []

    # Loop through them all
    for i in roles:

      # If it's @everyone
    	if i == '@everyone':

        # Add a space to prevent pinging
    		roles_temp.append('@ everyone')
    	else:

        # Otherwise append the role's name to the array
    		roles_temp.append(interaction.guild.get_role(i).name)

    # Send a message with the list 
    await interaction.send('**ADMIN ROLES:**\n'+'\n'.join(roles_temp))

  @admin_list_command.subcommand(
    name="users",
    description="List manually set admin users."
  )
  async def admin_list_users_command(self, interaction: nextcord.Interaction):
    """
    List manually promoted admin users
    """

    # Read the admin users array
    users = config.read(interaction.guild_id, "admin users")
    users_temp = []

    # Loop through all of the users
    for i in users:

      # Fetch the User object
      user = await self.bot.fetch_user(i)

      # Append the name, and backslash underscores etc.
      users_temp.append(user.display_name.replace('_', '\_').replace('*', '\*'))
    
    # Send a message with the list
    await interaction.send('**ADMIN USERS:**\n'+'\n'.join(users_temp))

  @admin_list_command.subcommand(
    name="all",
    description="List every user with admin."
  )
  async def admin_list_all_command(self, interaction: nextcord.Interaction):
    """
    List every user with admin
    """

    # Read the admin users config array
    users = config.read(interaction.guild_id, "admin users")
    users_temp = []

    # Loop through all of the users
    for i in users:

      # Fetch the User object
      user = await self.bot.fetch_user(i)

      # Append the name, and backslash underscores etc.
      users_temp.append(user.display_name.replace('_', '\_').replace('*', '\*'))

    # Read the admin roles config array
    roles = config.read(interaction.guild_id, "admin roles")
    roles_temp = []

    # Loop through every role
    for i in roles:

      # If it's @everyone
      if i == '@everyone':

        # Send a custom message
        await interaction.send('Everyone on this server is an admin! The more the merrier!')

        # And cancel the rest of the function
        return
      else:
        
        # Otherwise just appent the Role object to the array
        roles_temp.append(interaction.guild.get_role(i))

    # Make a new array for all of the admin users
    members = []

    # Loop through every admin role
    for i in roles_temp:

      # Add each member with the role to an array
      members += i.members
    
    # Remove duplicates
    members = list(set(members))

    # Set a variable to the users manually promoted to admin
    manually_promoted_users_temp = users_temp

    # Loop through every member with an admin role
    for i in members:

      # Append their name to the array
      users_temp.append(i.display_name)

    # Remove duplicates (again)
    users_temp = list(set(users_temp))

    # Finally, send a message with every admin user,
    # manually promoted admin user, and admin role.

    await interaction.send(
			"**Users with admin:**\n  "
		  f"{', '.join(users_temp)}"
			"\n**Defined admin users:**\n  "
			f"{', '.join(manually_promoted_users_temp)}"
			"\n**Defined admin roles:**\n  "
			f"{', '.join(map(lambda x: x.name, roles_temp))}"
		)

def setup(bot):
  bot.add_cog(AdminCommand(bot))