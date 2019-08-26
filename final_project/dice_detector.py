#!/bin/env python3

# Hide TF warnings
import logging
from os import environ
logging.disable(logging.WARNING)  # Suppress deprecation warnings
environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Suppress tensorflow messages
environ["KMP_WARNINGS"] = "0"  # Suppress OpenMP messages
# End of Hide TF warnings

def gstreamer_pipeline (capture_width=480, capture_height=480, display_width=480, display_height=480, framerate=60, flip_method=0) :
    return ('nvarguscamerasrc ! '
    'video/x-raw(memory:NVMM), '
    'width=(int)%d, height=(int)%d, '
    'format=(string)NV12, framerate=(fraction)%d/1 ! '
    'nvvidconv flip-method=%d ! '
    'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
    'videoconvert ! '
    'video/x-raw, format=(string)BGR ! appsink'  % (capture_width,capture_height,framerate,flip_method,display_width,display_height))

def capture_camera():
    print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    ret,frame = cap.read()
    cv2.imwrite('Img/dice.png',frame)

class ModelParams(object):
    """ Simple object used to store parameters used in model """

    def __init__(self, img_rows, img_cols, rescale, batch_size, num_epoch,
                 classes=None, directory=None):
        """ Store arguments directly """
        self.img_rows = img_rows
        self.img_cols = img_cols
        self.rescale = rescale
        self.batch_size = batch_size
        self.num_epoch = num_epoch
        self.classes = classes
        self.directory = directory

    def __eq__(self, other):
        """ Compares fields """
        return (
            self.img_rows == other.img_rows
            and self.img_cols == other.img_cols
            and self.rescale == other.rescale
            and self.batch_size == other.batch_size
            and self.num_epoch == other.num_epoch
            and self.directory == other.directory
            and self.classes == other.classes
        )


def load_model(filename, params):
    from keras.models import load_model
    from pickle import load

    with open(filename + '.params', 'rb') as params_file:
        model_params = load(params_file)

    if model_params != params:
        print('Current params differ from saved params. Aborting load')
        raise FileNotFoundError

    with open(filename + '.hist', 'rb') as hist_file:
        model_hist = load(hist_file)
    model = load_model(filename + '.h5')

    print('Loading model from disk')
    return model, model_hist


if __name__ == '__main__':
    from argparse import ArgumentParser
    from keras.preprocessing.image import ImageDataGenerator
    from PIL import Image
    import keras
    import numpy
    #import cv2
    import time
    start = time.time()

    parser = ArgumentParser(description='Execute [and train] a CNN model')
    parser.add_argument('-m', action='store', nargs='?', default='model',
                        help='Filename for storing the model and history')
    args = parser.parse_args()

    params = ModelParams(
        img_rows=80,  # Training data size is 480
        img_cols=80,  # Training data size is 480
        rescale=1./255,
        batch_size=10,
        num_epoch=10,
        classes=['d4', 'd6', 'd8', 'd10', 'd12', 'd20'],
        directory='./dice/',
    )

    model, model_hist = load_model(args.m, params)
    #capture_camera()

    img = numpy.array(keras.preprocessing.image.load_img('Img/dice.png', target_size=(params.img_rows,params.img_cols), color_mode="grayscale"))
    img = numpy.expand_dims(img, axis=3)
    img = numpy.array([img,])
    prd = model.predict_classes(img, batch_size=params.batch_size)

    if prd == 1:
        print('Dice: d4')
    elif prd == 2:
        print('Dice: d6')
    elif prd == 3:
        print('Dice: d8')
    elif prd == 4:
        print('Dice: d10')
    elif prd == 5:
        print('Dice: d12')
    elif prd == 6:
        print('Dice: d20')

    end = time.time()
    print("Exc Time: ",end - start)
