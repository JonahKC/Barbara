import config.config as config

async def main(message, prefix, client):
	serverAdmins = config.read(message.guild.id, "admin users")
	if f'<@!{message.guild.owner_id}>' not in serverAdmins:
		serverAdmins.append(f'<@!{message.guild.owner_id}>')
		config.fetch(message.guild.id, "admin users")
	return