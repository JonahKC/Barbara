# Deprecated web server for bot. If you're looking to do frontend stuff, use the Barbara-frontent repl.
from flask import Flask, render_template
from threading import Thread
app = Flask('')
@app.route('/')
def main():
  return render_template('index.html')
def run():
    app.run(debug=False, host="0.0.0.0", port=3000)
def keep_alive():
		server = Thread(target=run)
		server.start()