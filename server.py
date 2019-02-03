import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import sys
import cv2

sys.path.insert(0, './src/')
import map_to_image
import dominant_image_color

sys.path.insert(0, './src/vision/')
from hslpipline import *

app = Flask(__name__, template_folder='web')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = 'assets'
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
                filepath = app.config['UPLOAD_FOLDER'] + '/' + filename
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

    if 'favicon.ico' not in filename:
        most_dominant_color = dominant_image_color.dominant_color(filename)
        print(most_dominant_color)

    return render_template('info.html',
        filename=filename,
        soil_color_r=most_dominant_color[0],
        soil_color_g=most_dominant_color[1],
        soil_color_b=most_dominant_color[2])

@app.route('/assets/<filename>')
def send_assets(filename):
    print("assests accesesd")
    return send_from_directory('assets', filename)

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
    return send_from_directory('web/js', path)

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

