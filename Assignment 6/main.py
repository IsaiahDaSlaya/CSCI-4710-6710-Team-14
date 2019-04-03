import os
from flask import Flask, request, render_template
import json
import util


app = Flask(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = dir_path + '/data/'
app.config['DATA_FILE'] = UPLOAD_FOLDER + 'NRDC_data.csv'
app.config['COL_NAME'] = 'Temperature'

@app.route('/')
def index():
    # this is your index page
    log = 'Index.'
    return render_template('index.html', log_index = log)

@app.route('/config')
def config():
    # this is your index page
    return render_template('config.html')

@app.route('/api/process_csv/<lower_threshold>/<upper_threshold>')
def process_csv(lower_threshold= '', upper_threshold= ''):
	qualified, outlier = util.threshold_process_method(app.config['DATA_FILE'], app.config['COL_NAME'], float(lower_threshold), float(upper_threshold))
	return qualified

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
