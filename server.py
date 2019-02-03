import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import sys
import cv2

sys.path.insert(0, './src/')
import map_to_image

sys.path.insert(0, './src/vision/')
from hslpipline import *

app = Flask(__name__, template_folder='web')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = 'assets/uploaded'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])


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
        # check if the post request has the file part
        if 'file' not in request.files:
            google = request.form['google']
            if google != '':
                filename = 'google-maps1.png'
                filepath = 'assets/' + filename
                if (os.path.isfile(filepath)):
                    os.remove(filepath)

                filename = secure_filename(filename)
                map_to_image.save_image_for_google_maps_url(filepath, google)
                process_image(filepath)
                return redirect(url_for('uploaded_file', filename=filename))

            return render_template('home.html')

        file = request.files['file']
        coordinates = request.form['coordinates']
        
        # if user does not select file, browser also
        # submit an empty part without filename
        if file and allowed_file(file.filename) and coordinates != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
            file.save(filepath)
            process_image(filepath)

            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return render_template('home.html')


@app.route('/<filename>', methods=['GET', 'POST', 'OPTIONS'])
def uploaded_file(filename):
    if request.method == 'POST':
        rgb = request.get_json()

    filename = app.config['UPLOAD_FOLDER'] + '/' + filename
    return render_template('uploaded_image.html', filename=filename)

@app.route('/assets/<filename>')
def send_assets(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/css/<filename>')
def send_css(filename):
    return send_from_directory('web/css', filename)

@app.route('/fonts/<filename>')
def send_fonts(filename):
    return send_from_directory('web/fonts', filename)

@app.route('/img/<filename>')
def send_img(filename):
    return send_from_directory('web/img', filename)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
