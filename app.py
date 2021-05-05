import os
from stylize import render
from PIL import Image
from flask import Flask,flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
# from scipy.misc import imread, imsave
# # pip install scipy==1.1.0
import imageio



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
        # image = Image.open(UPLOAD_FOLDER + '/image.jpg').convert('RGB')
        image = cv2.imread(UPLOAD_FOLDER + '/image.jpg')
        #file.save(os.path.join('./static/image.jpg'))
        #abstract = render(image, depth=4, verbose=True)
        smoother = render(image, iterations=25, verbose=True)
        # aa = render(image, anti_aliasing=True, verbose=True)
        #less_detail = render(image, ratio=0.001, verbose=True)
        # more_detail = render(image, ratio=0.00005, verbose=True)
        #landmarks = render(image, features='landmarks', verbose=True)
        # defaults = render(image, verbose=True)
        imageio.imwrite('./static/image.jpg', smoother)
        # imsave('./static/image.jpg', landmarks)
        # abstract = abstract.save('./static/image.jpg')
        # imsave(r'./static/image.jpg', abstract)
        # show_img(abstract, "A depth of 4 results in an abstract representation")
        image = Image.open('./static/image.jpg')
        image.show()
        return {"id":1,"Username":"admin","Level":"Administrator"} , 200
    return "http://10.0.2.2:5000/upload/image.jpg" , 200



if __name__ == '__main__':
    app.run(host='0.0.0.0')

