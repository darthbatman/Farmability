import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from src.soil_color import find_closest_soil_match_by_color
from src.monthly_rainfall import weather
from src.dominant_image_color import dominant_color

import sys
import cv2
import numpy

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

avg_rain = 0.0


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
                lat = lat.split(',')
                lon = lat[1]
                lat = lat[0]
                global avg_rain
                print(lat)
                print(lon)
                # avg_rain = weather(float(lat),float(lon))
                print(avg_rain)

                filename = 'google-maps1.png'
                filepath = app.config['UPLOAD_FOLDER'] + '/' + filename
                filename = secure_filename(filename)
                map_to_image.save_image_for_google_maps_url(filepath, google)
                process_image(filepath)
                if 'favicon.ico' not in filename:
                    most_dominant_color = dominant_color(filepath)
                    print(most_dominant_color)
                    soil_match = find_closest_soil_match_by_color(most_dominant_color, 'data/soil.json')
                    print(soil_match)
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
            # avg_rain = weather(float(lat),float(lon))

            filename = secure_filename(file.filename)
            print(request.form['coordinates'])
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            process_image(filepath)

            if 'favicon.ico' not in filename:
                most_dominant_color = dominant_color(filepath)
                soil_match = find_closest_soil_match_by_color(most_dominant_color, 'data/soil.json')
                print(soil_match)
            
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return render_template('home.html')


@app.route('/<filename>', methods=['GET', 'POST', 'OPTIONS'])
def uploaded_file(filename):
    filepath = app.config['UPLOAD_FOLDER'] + '/' + request.url[20:]
    if request.method == 'POST':
        rgb = request.get_json()
        rgb = numpy.uint8([[[rgb['B'],rgb['G'],rgb['R']]]])
        hls = cv2.cvtColor(rgb,cv2.COLOR_BGR2HLS)
        process_image(filepath, hls[0][0][0], hls[0][0][2], hls[0][0][1])

    filename = app.config['UPLOAD_FOLDER'] + '/' + filename

    if 'favicon.ico' not in filename:
        most_dominant_color = dominant_image_color.dominant_color(filename)
        soil_match = find_closest_soil_match_by_color(most_dominant_color, 'data/soil.json')

    return render_template('info.html',
        filename=filename,
        soil_color_r=most_dominant_color[0],
        soil_color_g=most_dominant_color[1],
        soil_color_b=most_dominant_color[2],
        soil_munsell_fine=soil_match['munsell_fine'],
        soil_munsell_color=soil_match['munsell_color'],
        soil_water_content=soil_match['water_content'],
        soil_indicates=soil_match['indicates'][0],
        precipitation=str(avg_rain))

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
