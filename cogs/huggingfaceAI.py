from discord.ext import commands
import lib.admin as admin
import mediawiki
import aiohttp
import os
from typing import Optional

QA_URL = "https://api-inference.huggingface.co/models/bert-large-uncased-whole-word-masking-finetuned-squad"
GPT_NEO_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"

headers = {"Authorization": f"Bearer {os.getenv('API_TOKEN')}"}

async def query(payload, url=QA_URL, parameters={}, options={}):
  body = {"inputs":payload,'parameters':parameters,'options':options}
  async with aiohttp.ClientSession() as cs:
    async with cs.post(url, headers=headers, json=body) as response:
      answer = await response.json()
      return answer
#%prompt 4 I'm an engineer constructing cutting edge transportation
class HuggingfaceAI(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.wikipedia = mediawiki.MediaWiki()

  @commands.command(name='textgen', aliases=['prompt'])
  async def textGen(self, ctx, length: Optional[int]=-1, temperature: Optional[float]=1.0, *, prompt: str):
    answer = await ctx.send("Waiting for GPT-NEO")
    if length == -1:
      length = min(round(len(prompt) / 4.4) + 45, 500)
    else:
      length = int(length)
    minimumTokenLength = 6
    if admin.perms(ctx):
      minimumTokenLength = 1
    if length > 500 or length < minimumTokenLength:
      await ctx.send(f"Sorry, token length of {length} is invalid. Either it's too big, or too small. Please try a different length. My personal favorite is 40, which will output one or two sentences.")
      return
    answerText = prompt + (await query(prompt, GPT_NEO_URL, {"repetition_penalty": 3.2, "temperature": temperature, "return_full_text": False, "max_length": length, 'end_sequence': "###"}))[0]['generated_text']
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