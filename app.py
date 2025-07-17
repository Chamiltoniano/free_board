from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

app = Flask(__name__)

# Carpeta donde se subirán las imágenes
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint para subir imágenes
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'archivo' not in request.files:
        return 'No file part', 400
    file = request.files['archivo']
    if file.filename == '':
        return 'No selected file', 400
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return f'Imagen subida correctamente: <a href="/static/uploads/{file.filename}">{file.filename}</a>'

# Endpoint para listar las imágenes subidas
@app.route('/list_uploads')
def list_uploads():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            files.append(url_for('static', filename=f'uploads/{filename}'))
    return jsonify(files)

if __name__ == '__main__':
    app.run(debug=True)
