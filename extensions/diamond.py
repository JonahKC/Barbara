import nextcord
from re import match
from asyncio import sleep
from nextcord.ext import commands
from nextcord import PCMVolumeTransformer, FFmpegPCMAudio

class Diamond(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def play(ctx, query, blockUntilDone=False):
    """
    Play a .mp3 in the vc the user is in, optionally blocking the code until it's done playing
    """

    # Convert the audio file path into a playable audio object
    source = PCMVolumeTransformer(FFmpegPCMAudio(query))

    # Play it!
    ctx.voice_client.play(source)

    # Sleep until it's done
    if blockUntilDone:
      try:
        while ctx.voice_client.is_playing():
          await sleep(1)
      except AttributeError:
        await ctx.message.delete()

  async def join(ctx):
    """
    Join the VC the user is in
    """
    try:
      channel = ctx.author.voice.channel
      vc = ctx.voice_client
      if vc:
        await vc.move_to(channel)
      else:
        vc = await channel.connect()
      return vc
    except Exception as e:
        print(repr(e))

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.content.lower() == "hey barbara, can you play me a song?":
      ctx = await self.bot.get_context(message)
      print(message.content)
      try:

        # Join the vc
        await self.join(ctx)

        # Wait a second
        await sleep(1)

        # Play sweet caroline
        await self.play(ctx, './resources/neil-diamond-sweet-caroline.mp3')

        # Send a wink emoji
        msg = await ctx.send("😉")

        # Wait for Neil Diamond to start singing
        await sleep(14)

        # Go through all the lyrics
        with open('./resources/sweet_caroline.txt') as file:
          for line in file:

            # Get the amount of time to wait after each lyric
            # and the actual lyric
            lineMatch = match(r"(?P<lyric>.*):(?P<time>\d*.\d*)",line)
            lyric = lineMatch.group("lyric")
            dur = lineMatch.group("time")

            # Edit the original message to the current lyric
            await msg.edit(content=lyric.replace(r'\n', '\n'))

            # Wait the specified amount of time
            await sleep(float(dur))

        # Leave the vc
        await ctx.voice_client.disconnect()

        # Delete the command
        await message.delete()

      # If the user is not in a call or the bot is already in a call
      except Exception as e:

        # Send an error message
        if e.__class__ == AttributeError:
          await ctx.send("Try again in a voice call 😉")
        elif e.__class__ == nextcord.ClientException:
          await ctx.send(f"Sorry, I'm already in a vc ({ctx.voice_client.channel.name}).")

def setup(bot):
  bot.add_cog(Diamond(bot))