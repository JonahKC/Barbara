from discord.ext import commands
import mediawiki
import aiohttp
import os

QA_URL = "https://api-inference.huggingface.co/models/bert-large-uncased-whole-word-masking-finetuned-squad"
GPT_NEO_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"

headers = {"Authorization": f"Bearer {os.getenv('API_TOKEN')}"}

async def query(payload, url=QA_URL, parameters={}, options={}):
  body = {"inputs":payload,'parameters':parameters,'options':options}
  async with aiohttp.ClientSession() as cs:
    async with cs.post(url, headers=headers, json=body) as response:
      answer = await response.json()
      return answer

class HuggingfaceAI(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.wikipedia = mediawiki.MediaWiki()

  @commands.command(name='textgen', aliases=['prompt'])
  async def textGen(self, ctx, length: int=-1, *, prompt: str):
    answer = await ctx.send("Waiting for GPT-NEO")
    if length == -1:
      length = max(250, len(prompt))
    answerText = prompt + (await query(prompt, GPT_NEO_URL, {"repetition_penalty": 1.3, "temperature": 2.5, "return_full_text": False, "max_length": length}))[0]['generated_text']
    await answer.edit(answerText)

  @commands.command(name='igotaquestion', aliases=['plzihavequestion', 'readthisandanswermyquestion', 'aiqa', 'ask'])
  async def aiqa(self, ctx, wikipediaPageTitle: str=None, *, quesion: str):
    answer = await ctx.send("Waiting for Wikipedia...")
    try:
      summary = self.wikipedia.page(wikipediaPageTitle).summarize(10)
    except mediawiki.exceptions.DisambiguationError as e:
      await answer.edit(f"Sorry, there's multiple Wikipedia articles going by similar names to what you requested I look at. Look at this list and see which one you want: {str(e)[:30] + (str(e)[30:] and '...')}")
      return
    except mediawiki.exceptions.PageError:
      await answer.edit("Sorry, no Wikipedia page by the requested title was found.")
      return
    except mediawiki.exceptions.HTTPTimeoutError:
      await answer.edit("Sorry, the Mediawiki servers timed out. Maybe try again later idk")
      return
    except mediawiki.exceptions.RedirectError:
      await answer.edit("Sorry, the Wikipedia page unexpectedly resolved to a redirect.")
      return
    await answer.edit("Waiting for bert-large-uncased-whole-word-masking-finetuned-squad...")
    answerText = (await query({
      "inputs": {
        "question": quesion,
        "context": summary,
      },
    }))['answer']
    await answer.edit(answerText)

def setup(bot):
  bot.add_cog(HuggingfaceAI(bot))