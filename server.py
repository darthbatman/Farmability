import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from src.soil_color import find_closest_soil_match_by_color
from src.monthly_rainfall import weather
import sys
import cv2

sys.path.insert(0, './src/')
import map_to_image

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
                lat = google[google.find('@')+1:]
                lat = lat[:22]
                lon = lat[lat.find(',')+1:]
                lat = lat[:lat.find(',')]
                avg_rain = weather(float(lat),float(lon))

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
            lat = coordinates
            lon = lat[lat.find(',')+1:]
            lat = lat[:lat.find(',')]
            avg_rain = weather(float(lat),float(lon))

            filename = secure_filename(file.filename)
            print(request.form['coordinates'])
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
        print(rgb)
        soil_color = [None] * 3
        soil_color[0] = rgb['R']
        soil_color[1] = rgb['G']
        soil_color[2] = rgb['B']
        soil_match = find_closest_soil_match_by_color(soil_color, 'data/soil.json')
        print(soil_match)

    filename = app.config['UPLOAD_FOLDER'] + '/' + filename
    return render_template('uploaded_image.html', filename=filename)

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
    app.run(host="0.0.0.0",debug=True)

