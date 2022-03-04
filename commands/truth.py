import config
import nextcord
import util
from lib.LCG import LCG
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL, DEVELOPMENT_FEATURES

class TruthCommand(commands.Cog):
  """
  Get a pickup line from a hand-curated list of 400+
  """
  def __init__(self, bot):
    self.bot = bot
  
  @nextcord.slash_command(
    name='truth',
    description='Truth or dare... with out the \'or dare\' part.',
    guild_ids=TESTING_GUILD_ID,
    force_global=SLASH_COMMANDS_GLOBAL,
  )
  async def truth_command(self, interaction: nextcord.Interaction, juice=nextcord.SlashOption(
    name='juice',
    description='The type of question to ask.',
    choices=('Friends', 'Partners')
  )):

    guild_id = interaction.guild_id

    with open('./resources/truths.txt','r') as fp:
      file_raw = fp.read()
      categories = file_raw.split('CATEGORY:')
      categories.pop(0)

      categories = [x.split('\n') for x in categories]
      cat_dict = {}
      
      for i in categories:
        cat = [x for x in i if x.strip() != '']
        cat_dict[cat[0].lower()] = cat[1:]

      truths = cat_dict[juice.lower()]
      if juice == 'Partners':
        truths += cat_dict['friends']
      
      lcg_data = config.read(guild_id,f'_truth_{juice.lower()}_lcg')
      
      try:
        lcg_data.pop('last_num')
      except KeyError:
        pass
      try:
        lcg = LCG(len(truths),**lcg_data)
      except ValueError:
        await interaction.send(util.get_message("truth.category_not_implemented"), ephemeral=True)
        return
			
      # Get the truth, and replace {author} with the command author's name
      last_num = config.read(guild_id,f'_truth_{juice.lower()}_lcg').get('last_num')
      truth = truths[lcg.gen(last_num)].format(
        author=interaction.user.display_name
      )

			# Update stored lcg data
      lcg_data = {
        'seed': lcg.seed,
        'additive': lcg.additive,
        'coefficient': lcg.coefficient,
        'last_num': lcg.last_num
      }
      config.write(guild_id,f'_truth_{juice.lower()}_lcg',lcg_data)

      # Send the truth
      await interaction.send(truth)

def setup(bot):
  bot.add_cog(TruthCommand(bot))