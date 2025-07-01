from flask import Flask, send_from_directory, request, redirect, url_for
from flask import jsonify
import os

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'archivo' not in request.files:
        return 'No file part', 400
    file = request.files['archivo']
    if file.filename == '':
        return 'No selected file', 400
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return f'Imagen subida correctamente: <a href="/{filepath}">{file.filename}</a>'

@app.route('/list_uploads')
def list_uploads():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            files.append(f'/static/uploads/{filename}')
    return jsonify(files)

if __name__ == '__main__':
    app.run()
