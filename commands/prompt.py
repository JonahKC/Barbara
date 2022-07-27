import nextcord
from nextcord.ext import commands
import lib.huggingface as huggingface
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL


class PromptCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name='prompt',
        description=
        'Generate text using BLOOM, the model made by the volunteers during the BigScience 1-year AI workshop',
        guild_ids=TESTING_GUILD_ID,
        force_global=SLASH_COMMANDS_GLOBAL)
    async def prompt_command(
        self,
        interaction: nextcord.Interaction,
        prompt: str = nextcord.SlashOption(
            description=
            'The AI tries to "continue" this text. Try and keep under 3 sentences.'
        ),
        temperature: float = nextcord.SlashOption(
            description='Creativity/Chaos of the output.',
            choices={
                'Factual': 0.0000001,
                'Insightive': 0.5,
                'Creative': 0.7,
                'Very Creative': 1.0,
                'Insane': 100.0
            }),
        length: int = nextcord.SlashOption(
            description='Rough estimate of output length.',
            choices={
                'One-Word': 1,
                'Sentence': 16,
                'Paragraph': 38,
                'Essay': 250
            }),
        repetition_penalty: float = nextcord.SlashOption(
            description=
            'Encourage the AI to talk about new things -- or at least to not repeat words it\'s used a lot',
            required=False,
            default=2.0,
            choices={
                "Repetetive": 0.0,
                "Normal": 2.0,
                "Unique": 15.0,
                "Quirky": 50.0,
                "ADHD": 100.0
            }),
        return_sequences: int = nextcord.SlashOption(
            description=
            'How many times should you enslave the AI to complete your prompt?',
            required=False,
            default=1,
            min_value=1,
            max_value=3)):

        # If there, remove extra leading/trailing whitespace
        prompt = prompt.strip('\n ')

        # Bot is thinking
        await interaction.response.defer()

        # Get the output from GPT-J
        raw_ai_output = await huggingface.query(
            prompt, huggingface.Model.BLOOM, {
                'repetition_penalty': repetition_penalty,
                'num_return_sequences': return_sequences,
                'temperature': temperature,
                'max_new_tokens': length,
                'return_full_text': False
            }, {'wait_for_model': True})

        # Loop through all of the outputs
        for output in raw_ai_output:

            # Add the prompt to the beginning
            if type(output) == str:
                complete_text = "**" + prompt + "**" + output
            else:
                complete_text = "**" + prompt + "**" + output[
                    'generated_text'][len(prompt) - 1:]

            # Cut it off at 2000 characters so Discord doesn't scream at us
            complete_text = complete_text[:1996] + (complete_text[1996:]
                                                    and '...')

            # Send a message with the prompt test as well as
            # the AI-generated text
            await interaction.send(complete_text)


def setup(bot):
    bot.add_cog(PromptCommand(bot))
