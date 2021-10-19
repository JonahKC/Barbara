from discord.ext import commands
from discord.errors import HTTPException

class ReactionCommand(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name='reaction', aliases=['reactions'], invoke_without_subcommand=False)
  async def reaction(self, ctx):
    pass

  @reaction.command(name='add')
  async def reactionAdd(self, ctx, *, reactions: str):
    reactions = reactions.replace(' ', '').split(',')
    messageToReact = (await ctx.channel.history(limit=2).flatten())[1]
    for reaction in reactions:
      try:
        await messageToReact.add_reaction(reaction)
      except HTTPException:
        await ctx.send(f"Invalid Reaction: {reaction}", delete_after=3.0)
    await ctx.message.delete()

  @reaction.command(name='remove')
  async def reactionRemove(self, ctx, *, reactions: str):
    reactions = reactions.replace(' ', '').split(',')
    messageToReact = (await ctx.channel.history(limit=2).flatten())[1]
    for reaction in reactions:
      try:
        await messageToReact.remove_reaction(reaction, self.bot.user)
      except HTTPException:
        await ctx.send(f"Invalid Reaction: {reaction}", delete_after=3.0)    
    await ctx.message.delete()

def setup(bot):
  bot.add_cog(ReactionCommand(bot))