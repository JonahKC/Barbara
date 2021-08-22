from discord.ext import commands
from discord import File
from pyppeteer import launch
import lib.directoryVars as paths

class WebsiteScreenshotter(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def screenshot(self, ctx, website: str):
    progress = await ctx.send("Screenshotting... Awaiting `browser.launch()`")
    browser = await launch()
    await progress.edit("Screenshotting... Awaiting `browser.newPage()`")
    page = await browser.newPage()
    await progress.edit("Screenshotting... Awaiting `page.goto()`")
    await page.goto(website)
    await progress.edit("Screenshotting... Taking Screenshot")
    await page.screenshot({'path': paths.ABS_WORKING_DIR + '/temp/website.jpg', 'fullpage': True, 'quality': 80})
    await progress.edit("Screenshotting... Awaiting `browser.close()`")
    await browser.close()
    await progress.edit("Screenshotting Complete. Sending Image.")
    await progress.edit(file=File(paths.ABS_WORKING_DIR + '/temp/website.jpg'))

def setup(bot):
  bot.add_cog(WebsiteScreenshotter(bot))