import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import json
import util

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = dir_path + '/data/'

# Upload a CSV File
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['DATA_FILE'] = UPLOAD_FOLDER + 'NRDC_data.csv'
app.config['COL_NAME'] = 'Temperature'
app.config['json_obj'] = util.read_data(app.config['DATA_FILE'])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# request.file <class 'werkzeug.datastructures.FileStorage'>
		# request.url is http://127.0.0.1:5000/
		# check if the post request has the file part
		if 'file' not in request.files:
			log = 'no file field in request.'
			return render_template('fail.html', log = log)
		# print(request.files['file'])
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			# This part should use flash to output information
			log = 'Empty filename.'
			return render_template('fail.html', log = log)
		if file and util.allowed_file(file.filename):
			# get filename in a safe way
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			column_names, data_part = util.preview_csv(app.config['UPLOAD_FOLDER']+filename)
			return render_template('success.html',column_names=column_names, data_part=data_part)
	elif request.method == 'GET':
		return render_template('index.html')



@app.route('/read_data')
def read_data():
    return app.config['json_obj']

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
