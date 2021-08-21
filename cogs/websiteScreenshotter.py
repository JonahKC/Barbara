from discord.ext import commands
from pyppeteer import launch

class WebsiteScreenshotter(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def screenshot(self, ctx, website: str):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(website)
    image = await page.screenshot({'path': './temp/websites/website.png'})
    await browser.close()
    await ctx.send(image)
  
def setup(bot):
  bot.add_cog(WebsiteScreenshotter(bot))