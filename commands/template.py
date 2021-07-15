import config.config as config
#IF ADMIN ONLY: import commands.admin as admin

async def main(message, prefix, client):
	if message.content.startswith(f"{prefix}[COMMAND NAME]"):
		#IF ADMIN ONLY: if admin.perms(message.guild.id,message.author):
			"CODE GOES HERE"