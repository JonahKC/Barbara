from discord import PCMVolumeTransformer, FFmpegPCMAudio

def play(ctx, query): # Play an audio file in a vc
  source = PCMVolumeTransformer(FFmpegPCMAudio(query))
  ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

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