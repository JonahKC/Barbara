import json
from discord.ext import commands

class ServerInfo(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    servers = []
    for i in self.bot.guilds:
      servers.append(i.name)
    with open("servers.json", "w") as fp:
      json.dump(servers,fp,indent=2,sort_keys=True)
    return
  
def setup(bot):
  bot.add_cog(ServerInfo(bot))

