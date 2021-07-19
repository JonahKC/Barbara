async def main(message, prefix, client):
	content = message.content.split(" ")
	if message.content.startswith(f"{prefix}help"):
		if len(content) == 1:
			await message.channel.send(f"""**Hey there sweetie! I'm Barbara! Here's some things you can ask me:**

`{prefix}secret` - I'll tell you a secret!
`{prefix}pickup` - My husband fell for me after I told him a pickup line I got from this command.
`{prefix}link` - Check out some server-specific links.
`{prefix}invite` - Invite barbara to your Discord! (Also available at <https://barbara.jcwyt.com/>)
`{prefix}help admin` - View admin commands.

**For a list of all commands, go to <https://barbara.jcwyt.com/commands>.**""")
		elif content[1] == "admin":
			await message.channel.send(f"""**Here's a list of admin commands:**
*Remember, you need to be an admin to use these commands. I see you being sneaky...*

`{prefix}admin list roles` - Lists roles that can use admin commands.
`{prefix}admin list users` - Lists users that can use admin commands.
`{prefix}admin add role [@role]` - Adds role to admin command whitelist.
`{prefix}admin add user [@user]` - Adds user to admin command whitelist.
`{prefix}admin remove role [@role]` - Removes role from admin command whitelist.
`{prefix}admin remove user [@user]` - Removes user from admin command whitelist.
`{prefix}link set [message or link]` - Customizes the link in %link. Add as many as you want.
`{prefix}prefix [new prefix]` - Customize the prefix for all commands from % to whatever you want.

**If you would like to edit other config, use these commands:**

`{prefix}config read` - read the entire config as json (what the kids are coding in nowadays).
`{prefix}config read [option]` - read a specific option from config.
`{prefix}config set [option] [value]` - set option to value in config.

**Go to <https://barbara.jcwyt.com/adminhelp> for more info.**""")
