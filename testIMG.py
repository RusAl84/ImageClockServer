import os
from stylize import render
from PIL import Image
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
# from scipy.misc import imread, imsave
# # pip install scipy==1.1.0
import imageio
from PIL import Image

UPLOAD_FOLDER = './upload'

if __name__ == '__main__':
    # image = cv2.imread(UPLOAD_FOLDER + '/image.jpg')
    image = imageio.imread(UPLOAD_FOLDER + '/image.jpg')
    # file.save(os.path.join('./static/image.jpg'))
    # cv2.imwrite('./static/image.jpg',image)
    # imageio.imwrite('./static/image.jpg', image)
    abstract = render(image, depth=6, verbose=True)
    # # smoother = render(image, iterations=35, verbose=True)
    # # aa = render(image, anti_aliasing=True, verbose=True)
    # # less_detail = render(image, ratio=0.001, verbose=True)
    # # more_detail = render(image, ratio=0.00005, verbose=True)
    # # landmarks = render(image, features='landmarks', verbose=True)
    # # defaults = render(image, verbose=True)
    # imageio.imwrite('./static/image.jpg', abstract)
    # imsave('./static/image.jpg', landmarks)
    # abstract = abstract.save('./static/image.jpg')
    # imsave(r'./static/image.jpg', abstract)
    # show_img(abstract, "A depth of 4 results in an abstract representation")
    imageio.imwrite('./static/image.jpg', abstract)
    image = Image.open('./static/image.jpg')
    image.save('./static/image.png')

    image = Image.open('./static/image.png')
    fimage = Image.open('./static/foreground.png')
    image.paste(image, (1920, 1440), fimage)

    image.save('./static/image.jpg')
    image = Image.open('./static/image.jpg')
    image.show()
