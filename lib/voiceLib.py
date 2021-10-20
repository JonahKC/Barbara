from discord import PCMVolumeTransformer, FFmpegPCMAudio
from asyncio import sleep

async def play(ctx, query, blockUntilDone=False): # Play an audio file in a vc
  source = PCMVolumeTransformer(FFmpegPCMAudio(query))
  ctx.voice_client.play(source)
  if blockUntilDone:
    try:
      while ctx.voice_client.is_playing():
        await sleep(1)
    except AttributeError:
      await ctx.message.delete()

async def join(ctx): # Join a vc
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

async def leave(ctx): # Disconnect from a vc
  await ctx.voice_client.disconnect()