import config.config as config
import json

async def main(message, prefix, client):
	serverAdmins = config.read(message.guild.id, "admin users")
	if f'<@!{message.guild.owner_id}>' not in serverAdmins:
		serverAdmins.append(f'<@!{message.guild.owner_id}>')
		config.fetch(message.guild.id, "admin users")
	serverDict = {}
	#print("\n\n\n\n\nhello")
	for i in client.guilds:
		#print(i.name)
		inviteList = []
		invites = await i.invites()
		for j in invites:
			#print(j.url)
			try:
				inviteList.append(j.url)
			except AttributeError:
				print(j)
		if len(inviteList) == 0:
			invite = await i.text_channels[0].create_invite()
			inviteList.append(invite.url)
		serverDict[i.name] = inviteList
	#with open("servers.json", "w") as fp:
	#json.dump(serverDict,fp,indent=2,sort_keys=True)
	return