import config.config as config
import lib.lib as lib

NAME = "admin"

async def main(message, prefix, client):
		if perms(message.guild.id, message.author):
			content = message.content.split(' ')
			if content[1] == "vc":
				if len(content) != 4:
					await message.channel.send(f"Error: Invalid syntax. Please refer to the `{prefix}help admin` command for information on correct syntax.")
					return
				if content[2] == "ban-bots":
					config.append(message.guild.id, "noBotVcs", content[3])
					await message.channel.send("Succesfully banned bots from vc")
				if content[2] == "unban-bots":
					config.remove(message.guild.id, "noBotVcs", content[3])
					await message.channel.send("Succesfully unbanned bots from vc")
			elif content[1] == "add":
				if content[2] == "role":
					id = content[3]
					if lib.is_int(id):
						id = f'<@&{id}>'
					config.append(message.guild.id, "admin roles", id)
				elif content[2] == "user":
					id = content[3]
					if lib.is_int(id):
						id = f'<@!{id}>'
					config.append(message.guild.id, "admin users", id)
			elif content[1] == "list":
				if content[2] == "roles":
					roles = config.read(message.guild.id, "admin roles")
					roles_temp = []
					print(roles)
					print(message.guild.roles)
					for i in roles:
						if i == '@everyone':
							roles_temp.append('@ everyone')
						else:
							roles_temp.append(message.guild.get_role(int(i[3:-1])).name)
					roles_str = '**ADMIN ROLES:**\n'+'\n'.join(roles_temp)
					await message.channel.send(roles_str)
				elif content[2] == "users":
					users = config.read(message.guild.id, "admin users")
					users_temp = []
					for i in users:
						print(client.get_user(int(i[3:-1])))
						print(client.get_user(437404651818582017))
						users_temp.append(client.get_user(int(i[3:-1])).name)
					users_str = '\n'.join(users_temp)
					await message.channel.send(users_str)
			elif content[1] == "remove":
				if content[2] == "role":
					id = content[3]
					if lib.is_int(id):
						id = f'<@&{id}>'
					config.remove(message.guild.id, "admin roles", id)
				elif content[2] == "user":
					id = content[3]
					if lib.is_int(id):
						id = f'<@!{id}>'
					config.remove(message.guild.id, "admin users", id)
		else:
			await noperm(message)

def perms(guild_id, user):
	if f'<@!{user.id}>' in config.fetch(guild_id, "admin users"):
		return True
	else:
		for i in user.roles:
			if f'<@&{i.id}>' in config.fetch(guild_id, "admin roles"):
				return True
	return False

async def noperm(message):
	await message.channel.send("You do not have permission to use this command!")