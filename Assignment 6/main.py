import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import json
import util
import tablib
import os

app = Flask(__name__)

dataset = tablib.Dataset()
with open(os.path.join(os.path.dirname(__file__),'NRDC_data.csv')) as f:
    dataset.csv = f.read()

dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = dir_path + '/data/'

# Upload a CSV File
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATA_FILE'] = UPLOAD_FOLDER + 'NRDC_data.csv'
app.config['META_FILE'] = UPLOAD_FOLDER + 'meta_data.txt'
app.config['COL_NAME'] = 'Temperature'
json_obj = util.read_data(app.config['DATA_FILE'])
outlier = json_obj
lowerthreshold= ''
upperthreshold= ''


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

@app.route('/api/post_csv', methods=['POST'])
def post_csv():
	# request.file <class 'werkzeug.datastructures.FileStorage'>
	# request.url is http://127.0.0.1:5000/api/post_csv
	# check if the post request has the file part
	if 'file' not in request.files:
		log = 'no file field in request.'
		return render_template('fail.html', log = log)
	# print(request.files['file'])
	file = request.files['file']
	# if user does not select file, browser also
	# submit an empty part without filename
	if file.filename == '':
		log = 'Empty filename.'
		return render_template('fail.html', log = log)
	if file and util.allowed_file(file.filename):
		# get filename in a safe way
		filename = secure_filename(file.filename)
		# check if the data folder exists, if not create one
		if os.path.exists(app.config['UPLOAD_FOLDER']) == False:
			os.makedirs(app.config['UPLOAD_FOLDER'])
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return render_template('success.html',filename=filename)
		
@app.route('/read_data')
def read_data():
    return json_obj

@app.route('/config')
def config():
    # this is your index page
	
    return render_template('config.html', json_obj= json_obj)
	

@app.route('/save_data', methods=['GET','POST'])
def save_data():
	data = outlier
	text_file = open(app.config['META_FILE'], "w")
	text_file.write(data)
	text_file.close()
	return 'Success'
	
@app.route('/api/process_csv/<lower_threshold>/<upper_threshold>')
def process_csv(lower_threshold= '', upper_threshold= ''):
	qualified, outlier = util.threshold_process_method(app.config['DATA_FILE'], app.config['COL_NAME'], float(lower_threshold), float(upper_threshold))
	return qualified 

@app.route('/verify')
def verify():
    data = dataset.html
    return render_template('verify.html', data=data) 

@app.route('/runtests')
def runtests():
    
    log = 'runtests.'
    return render_template('Runtests.html', log_config = log)

@app.route('/review')
def review():
    log = 'review.'
    return render_template('review.html', log_config = log)

if __name__ == '__main__':
    app.debug = True
    ip = '127.0.0.1'
    app.run(host=ip)
