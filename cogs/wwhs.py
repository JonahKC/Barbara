from discord.ext import commands
from discord.utils import find
import discord

class WWHS(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    self.INTRODUCTIONS = (await (await self.bot.fetch_channel(854961975292854283)).history(limit=250).flatten())[::-1]
    self.KEYWORDS = ("lincoln", "hale", "roosevelt", "holy name", "lakeside", "ingraham", "ida b")
    self.TRIM = (':', 'name')

  def is_wwhs():
    def predicate(ctx):
      return ctx.guild.id == "838269717566718002"
    return commands.check(predicate)
  def has_keywords(self, msg):
    for k in self.KEYWORDS:
      if k in msg.lower():
        return True
    return False
  def extract_name_from_intro(self, intro: str):
    trimmed = intro.lower()
    for t in self.TRIM:
      trimmed = trimmed.replace(t, '')
    return " ".join([name.capitalize() for name in trimmed.split('\n')[0].split(' ')[0:3]]).strip()
  def find_name(self, id: int):
    try:
      intro = find(lambda x: x.author.id==id and self.has_keywords(x.content), self.INTRODUCTIONS).content
      return self.extract_name_from_intro(intro)
    except AttributeError:
      return f"No introduction found for user"

  @commands.command(name='whois')
  @is_wwhs()
  async def realname(self, ctx, person: discord.User):
    await ctx.send(f"{person.display_name} is {self.find_name(person.id)}")

def setup(bot):
  bot.add_cog(WWHS(bot))
