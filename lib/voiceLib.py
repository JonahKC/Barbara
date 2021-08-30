from discord import PCMVolumeTransformer, FFmpegPCMAudio
from time import sleep

def play(ctx, query, blockUntilDone=False): # Play an audio file in a vc
  source = PCMVolumeTransformer(FFmpegPCMAudio(query))
  ctx.voice_client.play(source)
  if blockUntilDone:
    while not ctx.voice_client.is_done():
      sleep(1)

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