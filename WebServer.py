import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = 'assets'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return render_template('index.html')


@app.route('/<filename>', methods=['GET', 'POST', 'OPTIONS'])
def uploaded_file(filename):
    if request.method == 'POST':
        rgb = request.get_json()

    filename = app.config['UPLOAD_FOLDER'] + '/' + filename
    return render_template('uploaded_image.html', filename=filename)


@app.route('/assets/<filename>')
def send_assets(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


if __name__ == '__main__':
    app.run(debug=True)
