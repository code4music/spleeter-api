import os
from spleeter.separator import Separator
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'upload'
OUTPUT_FOLDER = 'output'
MAX_CONTENT_LENGTH = 16 * 1000 * 1000 # 16MB
ALLOWED_EXTENSIONS = {'mp3', 'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            separator = Separator('spleeter:2stems')
            separator.separate_to_file(os.path.join(app.config["UPLOAD_FOLDER"], filename), app.config["OUTPUT_FOLDER"])
            return redirect(url_for('done', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/done/<name>', methods=['GET'])
def done(name):
    return f'''
    <!doctype html>
    <title>Upload completed</title>
    <h1>Upload completed!</h1>
    <a href="/outputs/{name}/vocals.wav">Download vocals</a><br>
    <a href="/outputs/{name}/accompaniment.wav">Download accompaniment</a>
    '''

@app.route('/outputs/<name>/<part>')
def download_file(name, part):
    destination = os.path.join(app.config["OUTPUT_FOLDER"], name.split('.')[0])
    return send_from_directory(destination, part)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT', '3000'))
