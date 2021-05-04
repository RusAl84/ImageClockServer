import os

from PIL import Image
from flask import Flask,flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './upload'

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/api/upload", methods=['POST'])
def SendMessage():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url), 200
        if file:
            filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = Image.open(UPLOAD_FOLDER + '/image.jpg')
        image.show()
        return redirect(url_for('read_uploaded_file',
                                filename=filename)) , 200
    return "" , 500



if __name__ == '__main__':
    app.run(host='0.0.0.0')

