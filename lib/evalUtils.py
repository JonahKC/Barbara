from discord.ext import commands
import discord
from discord.utils import find
from typing import Callable, Union
import inspect

async def in_each_channel(check: Union[Callable[[discord.TextChannel], bool], str], callback, bot: commands.Bot):
  noChannelsFound = True
  for guild in bot.guilds:
    for channel in guild.text_channels:
      if (type(check) == str and channel.name == check) or (inspect.isfunction(check) and check(channel)):
        noChannelsFound = False
        if inspect.iscoroutinefunction(callback):
          await callback(channel)
        else:
          callback(channel)
  if noChannelsFound:
    print(f"No channels found")

async def send(guild: str, channel: str, message: str, bot: commands.Bot):
  await find(lambda x: channel.lower() in x.name.lower(), find(lambda x: guild.lower() in x.name.lower(), bot.guilds).text_channels).send(message)

async def reply(channelID: int, messageID: int, message: str, bot: commands.Bot):
  await (await (bot.get_channel(channelID)).fetch_message(messageID)).reply(message)

async def dm(userID: int, message: str, bot: commands.Bot):
  await (await bot.fetch_user(userID)).send(message)