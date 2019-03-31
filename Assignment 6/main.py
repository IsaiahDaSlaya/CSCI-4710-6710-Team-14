from flask import Flask, render_template, jsonify, json
import util


app = Flask(__name__)


@app.route('/')
def index():
    # this is your index page
    log = 'Index.'
    return render_template('index.html', log_index = log)

@app.route('/config')
def config():
    # this is your index page
    return render_template('config.html')

@app.route('/verify')
def verify():
    # this is your index page
    return render_template('verify.html')	

@app.route('/runtests')
def runtests():
    # this is your index page
    log = 'runtests.'
    return render_template('Runtests.html', log_config = log)

@app.route('/review')
def review():
    # this is your index page
    log = 'review.'
    return render_template('review.html', log_config = log)

if __name__ == '__main__':
    app.debug = True
    ip = '127.0.0.1'
    app.run(host=ip)

