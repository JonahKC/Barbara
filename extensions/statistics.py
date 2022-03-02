import os
import json
import nextcord
from nextcord.ext import commands

class Statistics(commands.Cog):
  '''
	Record anonymous statistics about the bot
	'''
  def __init__(self, bot):
    self.bot = bot

    # If the file doesn't exist or it's empty
    if not os.path.exists('./stats.json') or os.stat('./stats.json').st_size == 0:
      
      # Write the default stats to it
      with open('./stats.json', 'w') as stats_json:
        json.dump({
          'commands_executed': 0,
          'meeses_censored': 0
        }, stats_json)
    
    with open('./stats.json', 'r') as stats_json:
      
      # Load stats.json into an object
      self.bot.stats = json.load(stats_json)

  def cog_unload(self):
    self.update_file()

  @commands.Cog.listener()
  async def on_interaction(self, interaction: nextcord.Interaction):
    self.bot.stats['commands_executed'] += 1
    self.update_file()

  def update_file(self):
    with open('./stats.json', 'w') as stats_json:
      json.dump(self.bot.stats, stats_json)

def setup(bot):
  bot.add_cog(Statistics(bot))