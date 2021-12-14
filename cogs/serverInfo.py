from discord.ext import commands

class ServerInfo(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Function to write server names bot is currently in to a txt file
  def write_serverlist(self):
    servers = []
    for i in self.bot.guilds:
      servers.append(i.name+'\n')
    with open("./servers.txt", "w") as serverlist:
      serverlist.writelines(servers)
  
  # Every time the bot starts, update the serverlist
  @commands.Cog.listener()
  async def on_ready(self):
    self.write_serverlist()

  # We joined a new server, update servers.txt
  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    self.write_serverlist()
  
def setup(bot):
  bot.add_cog(ServerInfo(bot))
