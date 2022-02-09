import nextcord
from nextcord.ext import commands
import lib.huggingface as huggingface
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL

class PromptCommand(commands.Cog):
  """
	Generate text with GPT-J, the autoregressive natural language transformer by Eleuther AI.
	"""
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(
		name='prompt',
		description='Generate text using the AI GPT-J',
		guild_ids=TESTING_GUILD_ID,
		force_global=SLASH_COMMANDS_GLOBAL
	)
  async def prompt_command(
    self,
    interaction: nextcord.Interaction,
    prompt: str,
    length: int=nextcord.SlashOption(
      required=True,
      default=32,
      min_value=8,
      max_value=256
    ),
    temperature: float=nextcord.SlashOption(
      required=True,
      default=0.5,
      min_value=0.0,
      max_value=2.0
    )
  ):

    # If there, remove extra leading/trailing whitespace
    prompt = prompt.strip('\n ')

    # Huggingface doesn't like 0 temperature
    # so change it to nigh zero
    temperature = min(temperature, 0.0000001)
    
    # Bot is thinking
    await interaction.response.defer()

    # Get the output from GPT-J
    raw_ai_output = (await huggingface.query(
      prompt,
      huggingface.Model.GPT_J_6B,
      {
        "repetition_penalty": 1.0,
        "temperature": temperature,
        "return_full_text": False,
        "top_p": 0.6
      },
      {'wait_for_model': True}
    ))[0]['generated_text']

    # Send a message with the prompt test as well as 
    # the AI-generated text
    await interaction.send(prompt + raw_ai_output)

def setup(bot):
  bot.add_cog(PromptCommand(bot))