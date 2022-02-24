import click
import logging
from flask import Flask
from flask_cors import CORS
from threading import Thread
from nextcord.ext import commands

class API(commands.Cog):
  """
	API to get data about Barbara
	"""
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    # Start a flask server so that you can ping her to see if she's alive
    web_app = Flask('')

    # use flask-cors to set Access-Control-Allow-Origin to "*"
    CORS(web_app)

    # Because we need to run this inside a thread
    def _run_webserver():
      web_app.run(host="0.0.0.0", port=8080)

    # Flask we don't care about your spam
    # These are overrides to the logging functions
    def secho(text, file=None, nl=None, err=None, color=None, **styles):
      pass
    def echo(text, file=None, nl=None, err=None, color=None, **styles):
      pass

    # Code injection hacker cia override function
    click.echo = echo
    click.secho = secho

    # Please Flask I don't care what you have to say
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @web_app.route('/')
    def webserver_index():
      return f"Barbara {self.bot.__version__}"

    @web_app.route('/guilds')
    def webserver_guilds():
      return str(len(self.bot.guilds))

    @web_app.route('/commands')
    def command_stats():
      return str(self.bot.stats['commands_executed'])

    @web_app.route('/m*eses')
    def meese_stats():
      return str(self.bot.stats['meeses_censored'])

    @web_app.route('/members')
    def total_members():
      return str(sum([guild.member_count for guild in self.bot.guilds]))

    # Start the server in a thread
    server = Thread(target=_run_webserver)
    server.start()

def setup(bot):
  bot.add_cog(API(bot))