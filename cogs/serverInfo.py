import json
from discord.ext import commands

class ServerInfo(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    serverDict = {}
    for i in self.bot.guilds:
      inviteList = []
      invites = await i.invites()
      for j in invites:
        try:
          inviteList.append(j.url)
        except AttributeError:
          print(j)
      if len(inviteList) == 0:
        invite = await i.text_channels[0].create_invite()
        inviteList.append(invite.url)
      serverDict[i.name] = inviteList
    with open("servers.json", "w") as fp:
      json.dump(serverDict,fp,indent=2,sort_keys=True)
    return
  
def setup(bot):
  bot.add_cog(ServerInfo(bot))