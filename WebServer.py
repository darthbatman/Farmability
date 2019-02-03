import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import sys
import cv2
sys.path.insert(0, './vision/')
from hslpipline import *

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = 'assets/uploaded'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_image(filename="assets/fields/generated_fields/field0.png", h=24, s=17, l=41):
    image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

    pipeline = HSLPipline(h, s, l, filename)
    pipeline.process(image)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
            file.save(filepath)

            process_image(filepath)

            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return render_template('index.html')


@app.route('/<filename>')
def uploaded_file(filename):
    filename = app.config['UPLOAD_FOLDER'] + '/' + filename
    return render_template('uploaded_image.html', filename=filename)


@app.route('/assets/<filename>')
def send_assets(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
