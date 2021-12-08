from discord.ext import commands
import discord
from random import choice#, uniform
import lib.admin as admin
import aiohttp
import os
from typing import Optional

GPT_NEO_URL ="https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
GPT_J_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"

headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_TOKEN')}"}

async def query(payload, url=GPT_NEO_URL, parameters={}, options={}):
  body = {"inputs":payload,'parameters':parameters,'options':options}
  async with aiohttp.ClientSession() as cs:
    async with cs.post(url, headers=headers, json=body) as response:
      try:
        return (await response.json())
      except aiohttp.client_exceptions.ContentTypeError:
        return (await response.text())

class HuggingfaceAI(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='textgen', aliases=['prompt'])
  async def textGen(self, ctx, length: Optional[int]=-1, temperature: Optional[float]=-1, *, prompt: str):
    if prompt.startswith('\n'): prompt = prompt.replace('\n', '', 1)
    if temperature == -1: temperature = 0.02
    temperature = max(temperature, 0.0001)
    answer = await ctx.send("Waiting for GPT-J-6B")
    minimumTokenLength = 4
    if admin.perms(ctx): minimumTokenLength = 1
    if (length > 500 or length < minimumTokenLength) and length != -1:
      await answer.edit(f"Sorry, token length of {length} is invalid. Either it's too big, or too small. Please try a different length. My personal favorite is 40, which will output one or two sentences.")
      return
    try:
      reqJSON = {"repetition_penalty": 90.0, "temperature": temperature, "return_full_text": False, "top_p": 0.6}
      if length != -1:
        reqJSON["max_new_tokens"] = length
      rawAnswer = await query(prompt, GPT_J_URL, reqJSON, {'wait_for_model': True})
      answerText = rawAnswer[0]['generated_text']
    except Exception:
      jsonStuff = str(rawAnswer).replace("\'", "\"")
      await answer.edit(f"Sorry, an unexpected `KeyError` was encountered talking to the API. Please report bugs in the JCWYT Discord, or by contacting bugs@jcwyt.com. When you report the error, give us this: ```json\n{jsonStuff[:1500] + ('...' and jsonStuff[:1500])}\n```")
      return
    await answer.edit(answerText[1980:] + ('...' and answerText[:1980]))

  @commands.command(name='josh', aliases=['yosh'])
  async def hiJosh(self, ctx):
    await ctx.send(choice(("tuple", "Java is shorthand for JavaScript", str(discord.utils.get(self.bot.emojis, name='Susstew')))))

def setup(bot):
  bot.add_cog(HuggingfaceAI(bot))