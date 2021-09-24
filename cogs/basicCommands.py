import config.config as config
import lib.admin as admin
import lib.help as libHelp
import lib.graph as graph
from discord.ext import commands
from random import choice
from asyncio import sleep, TimeoutError
from discord.channel import DMChannel
from discord_components import Button, ButtonStyle, InteractionType

# Quick command explanation and syntax:
# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
# Cog explanation and syntax:
# https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html
# https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
# Subcommands syntax:
# https://github.com/Snaptraks/discord.py/blob/examples/examples/subcommands.py
# CommandError docs (used to check perms among other things)
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.CommandError

# Examples:
# https://github.com/AlexFlipnote/discord_bot.py

class BasicCommands(commands.Cog):
  def __init__(self, bot): # Allows us to access bot later on with self.bot
    self.bot = bot

  @commands.Cog.listener
  async def on_message(self, message):
      if self.bot.user.mention in message.content.split():
          await message.channel.send(f'Hi, {message.author.display_name}! Run `{config.read(message.guild.id, "prefix")}help` for help accessing my commands.')

  @commands.group(name='help',aliases=['h'], invoke_without_command=True)
  async def helpCommand(self, ctx, DM: str=""): # %help
    helpPages = libHelp.splitIntoPages(libHelp.helpText(ctx))
    helpPages = [i for i in helpPages if i]
    currentPage = 0
    if not DM:
      thingToSendMessageTo = ctx.channel
    else:
      thingToSendMessageTo = ctx.author
    #Totally original code not yoinked from https://github.com/SkullCrusher0003/paginator/blob/main/pagination.py
    helpMsg = await thingToSendMessageTo.send(
    	content = helpPages[currentPage],
      components = [
            [
              Button(
                label = "Prev",
                id = "back",
                style = ButtonStyle.green
              ),
              Button(
                label = f"Page {str(currentPage + 1)}/{str(len(helpPages))}",
                id = "cur",
                style = ButtonStyle.grey,
                disabled = True
              ),
              Button(
                label = "Next",
                id = "front",
                style = ButtonStyle.green
              )
            ]
          ]
    )
    while True:
      #Try and except blocks to catch timeout and break
      try:
        interaction = await self.bot.wait_for(
          "button_click",
          check = lambda i: i.component.id in ["back", "front"],
          timeout = 30.0
        )
        #Getting the right list index
        if interaction.component.id == "back":
          currentPage -= 1
        elif interaction.component.id == "front":
          currentPage += 1
        #If its out of index, go back to start / end
        if currentPage == len(helpPages):
          currentPage = 0
        elif currentPage < 0:
          currentPage = len(helpPages) - 1

        #Edit to new page + the center counter changes
        await interaction.respond(
          type = InteractionType.UpdateMessage,
          content = helpPages[currentPage],
          components = [ 
            [
              Button(
                label = "Prev",
                id = "back",
                style = ButtonStyle.green
              ),
              Button(
                label = f"Page {str(currentPage + 1)}/{str(len(helpPages))}",
                id = "cur",
                style = ButtonStyle.grey,
                disabled = True
              ),
              Button(
                label = "Next",
                id = "front",
                style = ButtonStyle.green
              )
            ]
          ]
        )
      except TimeoutError:
          #Disable and get outta here
          await helpMsg.edit(helpPages[currentPage]+"\nButtons disabled to stop Discord API rate limiting.", components=[])
          break

  @helpCommand.command(name='admin') # %help admin
  async def helpAdmin(self, ctx, DM: str=""):
    with open('./resources/helpAdmin.txt') as helpText:
      helpPages = libHelp.splitIntoPages(helpText.read().replace("{prefix}", ctx.prefix))
    helpPages = [i for i in helpPages if i]
    currentPage = 0
    if not DM:
      thingToSendMessageTo = ctx.channel
    else:
      thingToSendMessageTo = ctx.author
    helpMsg = await thingToSendMessageTo.send(
    	content = helpPages[currentPage],
      components = [
            [
              Button(
                label = "Prev",
                id = "back",
                style = ButtonStyle.green
              ),
              Button(
                label = f"Page {str(currentPage + 1)}/{str(len(helpPages))}",
                id = "cur",
                style = ButtonStyle.grey,
                disabled = True
              ),
              Button(
                label = "Next",
                id = "front",
                style = ButtonStyle.green
              )
            ]
          ]
    )
    while True:
      #Try and except blocks to catch timeout and break
      try:
        interaction = await self.bot.wait_for(
          "button_click",
          check = lambda i: i.component.id in ["back", "front"],
          timeout = 30.0
        )
        #Getting the right list index
        if interaction.component.id == "back":
          currentPage -= 1
        elif interaction.component.id == "front":
          currentPage += 1
        #If its out of index, go back to start / end
        if currentPage == len(helpPages):
          currentPage = 0
        elif currentPage < 0:
          currentPage = len(helpPages) - 1

        #Edit to new page + the center counter changes
        await interaction.respond(
          type = InteractionType.UpdateMessage,
          content = helpPages[currentPage],
          components = [ 
            [
              Button(
                label = "Prev",
                id = "back",
                style = ButtonStyle.green
              ),
              Button(
                label = f"Page {str(currentPage + 1)}/{str(len(helpPages))}",
                id = "cur",
                style = ButtonStyle.grey,
                disabled = True
              ),
              Button(
                label = "Next",
                id = "front",
                style = ButtonStyle.green
              )
            ]
          ]
        )
      except TimeoutError:
          #Disable and get outta here
          await helpMsg.edit(helpPages[currentPage]+"\nButtons disabled to stop Discord API rate limiting.", components=[])
          break

  @commands.command(name='invite') # %invite
  async def invite(self, ctx):
    await ctx.send(
      "**Invite Me to Your Other Discord Servers!**\n<https://barbara.jcwyt.com/invite>"
    )

  @commands.command(name='emily')
  async def emily(self, ctx):
    await ctx.send(choice(("hi Emily", "@emi1ypeng", "I wonder what Emily's listening to today... Nevermind, it's Taylor Swift")))

  @commands.group(name='link',aliases=['info','about'], invoke_without_command=True) # %link
  async def link(self, ctx, ):
    link = config.read(ctx.guild.id, "link").replace(
      "{prefix}", ctx.prefix
    ) # read the link message for this server, and replace the text {prefix} with the bot's prefix.
    if link.replace(" ", "") != "":
      await ctx.send(link)

  @link.command(name='set') # %link set
  async def setLink(
    self,
    ctx, *,
    arg=""
  ):
    config.write(ctx.guild.id, "link", arg)
    await ctx.send(f"Set link to {arg}")

  @commands.command(name='bazzi', aliases=['ifly'])
  async def perfectlyNormalFunction(self, ctx):
    for lyric in (("I guess what I'm sayin'", 0.6), (" I guess what I'm sayin'", 0.5), ("I guess what I'm sayin' is, I", 2), ("I f||uckin'|| love yooouuuuuuu", 0)):
      await ctx.send(lyric[0])
      await sleep(lyric[1])

  @commands.command(name='prefix') # %prefix !
  async def prefix(self, ctx, newPrefix: str):
    config.write(ctx.guild.id, "prefix", newPrefix)
    await ctx.send(f'My prefix is now \"{newPrefix}\"')

  @commands.command(name='reload',aliases=['cog','rld']) # %reload cogs.basicCommands
  @commands.check(admin.jcwytTeam)
  async def reloadCog(self, ctx, *, nameOfCog: str, stealthy="false"): # Reloads a Cog
    if stealthy == "true":
      await ctx.message.delete()
    try:
      self.bot.unload_extension(nameOfCog)
      self.bot.load_extension(nameOfCog)
    except Exception as e:
      await ctx.send(f'**ERROR:** `{type(e).__name__} - {e}`')
    else:
      await ctx.send(f'**SUCCESSFULLY RELOADED COG: **`{nameOfCog}`')
  @commands.command()
  async def ping(self, ctx):
   await ctx.send(f'Pong! 🏓\nPing: `{self.bot.latency} milliseconds`')

  @commands.command(name='restart')
  @commands.check(admin.jcwytTeam)
  async def restartRepl(self, ctx): # Restarts the entire repl.
    shutdownMessage = await ctx.send("Restarting bot...")
    sdRaw = open('./temp/shutdown-message.txt', 'w') # We want a "bot online again" message, so let's write the place that message should be in a file.
    if isinstance(ctx.channel, DMChannel):
      sdRaw.write(str(ctx.author.id) + "DM")
    else:
      sdRaw.write(str(shutdownMessage.channel.id))
    sdRaw.close()
    graph.flush()
    raise SystemExit

  @commands.Cog.listener()
  async def on_ready(self):
    try:
      sdRaw = open('./temp/shutdown-message.txt', 'r+') # Let's see if we need to send a message
      shutdownMessageData = sdRaw.read()
      sdRaw.truncate(0) # Delete contents so it doesn't send message next restart
      sdRaw.close()
      if shutdownMessageData[-2:] == "DM":
        channel = self.bot.get_user(int(shutdownMessageData[:-2]))
      else:
        channel = self.bot.get_channel(int(shutdownMessageData))
      await channel.send("Bot succesfully restarted!")
    except ValueError: # Repl didn't shutdown because of %restart
      pass

def setup(bot): # Builtin discord function
  bot.add_cog(BasicCommands(bot))
