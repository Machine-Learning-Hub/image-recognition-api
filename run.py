from flask import Flask, jsonify, request, render_template
from service import run_inference_on_image, training_data_set
from werkzeug import secure_filename

import os
import sys
import zipfile

app = Flask(__name__)

_upload_image_path = 'images/upload'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')


'''
    params:
        @img : image for recognize  type: file
'''


@app.route('/recognize', methods=['POST'])
def recognition():
    results = []
    if request.method == 'POST':
        # Get Image 
        img = request.files['img']
        # Upload
        file_path = upload_file_temp(img)
        # Start Recognition
        results = run_inference_on_image(file_path)
        # Delete temp file
        os.system('rm %s' % file_path)
    return jsonify({'results': results})


'''
    params:
        @zip_file       : zip file contains set of images type: file
        @training_name  : name of image to traint    type: text
'''


@app.route('/upload/zip', methods=['POST'])
def upload_zip():
    if request.method == 'POST':
        zip_file = request.files['zip_file']
        training_name = request.form['training_name']
        # Path upload for each user
        path = os.path.join(_upload_image_path, training_name)
        if not os.path.exists(path):
            os.system('mkdir -pv %s' % path)
        # Extract file
        extract_file(path, zip_file)
    return 'Upload Complete'


@app.route('/train', methods=['POST'])
def training():
    training_data_set()
    return 'Training Completed...'


'''
    params:
        @dir    :   path to image folder
        @file   :   zip file
'''


def extract_file(dir, file):
    f_name = secure_filename(file.filename)
    f_path = os.path.join(dir, f_name)
    file.save(f_path)
    # Extract
    with zipfile.ZipFile(f_path, "r") as zip_ref:
        zip_ref.extractall(dir)
    # Remove old file
    os.system('rm -rf %s' % f_path)
    os.system('rm -rf %s/__MACOSX' % dir)


'''
    params:
        @file : temp file to recognize
'''


def upload_file_temp(file):
    file_name = secure_filename(file.filename)
    file_path = ('tmp/%s' % file_name)
    file.save(file_path)
    return file_path


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
