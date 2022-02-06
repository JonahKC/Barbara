from discord.ext import commands
from discord import File
from pyppeteer import launch
from pyppeteer.errors import TimeoutError
from pyppeteer_stealth import stealth
from asyncio import sleep
import lib.admin as admin

class WebsiteScreenshotter(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  def is_nsfw_or_jcwyt(ctx):
    return ctx.channel.is_nsfw() or admin.jcwytTeam(ctx)

  @commands.check(is_nsfw_or_jcwyt)
  @commands.command(name='screenshot', aliases=['website', 'snapshot', 'takeapictureof', 'snap'])
  @commands.cooldown(1, 14, commands.BucketType.user)
  async def screenshot(self, ctx, website: str, fullPageArg=True, scrollBy: int=0, pageWidth: int=1280, pageHeight: int=720):
    if not hasattr(self.bot, 'browser'):
      progress = await ctx.send("Screenshotting... Awaiting `browser.launch()`")
      self.bot.browser = await launch(options={'args': ['--no-sandbox']})
    else:
      progress = await ctx.send("Screenshotting... Awaiting `browser.newPage()`")
    page = await self.bot.browser.newPage()
    await stealth(page)
    page.setDefaultNavigationTimeout(8000)
    await progress.edit("Screenshotting... Awaiting `page.setViewport()`")
    await page.setViewport({"width": 1280, "height": 720})
    await progress.edit("Screenshotting... Awaiting `page.goto()`")
    try:
      await page.goto(website)
    except TimeoutError:
      await progress.edit("Error: The website timed out.")
      await page.close()
      return
    await page.evaluate(f"window.scrollBy(0, {scrollBy});")
    await progress.edit("Waiting for page to fully load...")
    await sleep(1)
    await progress.edit("Screenshotting... Awaiting `page.screenshot()`")
    await page.screenshot({'path': './temp/SPOILER_website.png', 'fullPage': fullPageArg, })
    await progress.edit("Screenshotting... Awaiting `page.close()`")
    await page.close()
    await progress.edit("Screenshotting Complete. Sending Image.")
    await progress.delete()
    await ctx.send(f"Command Sender: {ctx.author.mention}. Command: `{ctx.message.content}`. Image:", file=File('./temp/SPOILER_website.png'))

def setup(bot):
  bot.add_cog(WebsiteScreenshotter(bot))