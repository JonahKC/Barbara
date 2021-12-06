from discord.ext import commands
import discord
import lib.introductions as intros

class WWHS(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    await intros.index(self.bot)

  @commands.command(name='whois')
  @intros.is_wwhs()
  async def realname(self, ctx, person: discord.User):
    await ctx.send(f"{person.display_name} is {intros.find_name(person)}")

def setup(bot):
  bot.add_cog(WWHS(bot))