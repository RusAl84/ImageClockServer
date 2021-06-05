import os
from stylize import render
from PIL import Image
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
# from scipy.misc import imread, imsave
# # pip install scipy==1.1.0
import imageio

UPLOAD_FOLDER = './upload'

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
import imageio
from PIL import Image
import numpy as np
import cv2

def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/api/upload", methods=['POST'])
def uploadAndConvert():
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
        # image = cv2.imread(UPLOAD_FOLDER + '/image.jpg')
        image = imageio.imread(UPLOAD_FOLDER + '/image.jpg')
        # file.save(os.path.join('./static/image.jpg'))
        abstract = render(image, depth=6, verbose=True)
        # smoother = render(image, iterations=35, verbose=True)
        # aa = render(image, anti_aliasing=True, verbose=True)
        # less_detail = render(image, ratio=0.001, verbose=True)
        # more_detail = render(image, ratio=0.00005, verbose=True)
        # landmarks = render(image, features='landmarks', verbose=True)
        # defaults = render(image, verbose=True)
        # imageio.imwrite('./static/image.jpg', smoother)
        imageio.imwrite('./static/image.jpg', abstract)
        # imsave('./static/image.jpg', landmarks)
        # abstract = abstract.save('./static/image.jpg')
        # imsave(r'./static/image.jpg', abstract)
        # show_img(abstract, "A depth of 4 results in an abstract representation")

        background = cv2.imread('./static/image.jpg')
        overlay = cv2.imread('./static/foreground.png', -1)  # Load with transparency
        result = blend_transparent(background, overlay)
        cv2.imwrite('./static/image.jpg', result)

        image = Image.open('./static/image.jpg')
        image.show()
        return {"id": 1, "Username": "admin", "Level": "Administrator"}, 200
    return "http://10.0.2.2:5000/upload/image.jpg", 200


@app.route("/api/enc", methods=['GET'])
def smoother():
    image = cv2.imread(UPLOAD_FOLDER + '/image.jpg')
    enc = render(image, iterations=25, verbose=True)  #сюда вставляется эффект
    imageio.imwrite('./static/image.jpg', enc)
    image = Image.open('./static/image.jpg')
    image.show()
    return "Complite encoding", 200
if __name__ == '__main__':
    app.run(host='0.0.0.0')
