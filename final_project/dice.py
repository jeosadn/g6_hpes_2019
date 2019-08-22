#!/bin/env python3

# Requirements:
#  conda install tensorflow keras pillow


# Hide TF warnings
import logging
from os import environ
logging.disable(logging.WARNING)  # Suppress deprecation warnings
environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Suppress tensorflow messages
environ["KMP_WARNINGS"] = "0"  # Suppress OpenMP messages
# End of Hide TF warnings


class ModelParams(object):
    """ Simple object used to store parameters used in model """

    def __init__(self, img_rows, img_cols, batch_size, num_epoch,
                 classes=None, directory=None, datagen=None):
        """ Store arguments directly """
        self.img_rows = img_rows
        self.img_cols = img_cols
        self.batch_size = batch_size
        self.num_epoch = num_epoch
        self.classes = classes
        self.directory = directory
        self.datagen = datagen

    def __eq__(self, other):
        """ Compares fields except for datagen """
        return (
            self.img_rows == other.img_rows
            and self.img_cols == other.img_cols
            and self.batch_size == other.batch_size
            and self.num_epoch == other.num_epoch
            and self.directory == other.directory
            and self.classes == other.classes
        )


def create_model(filename, params):
    """ Attempts to load model from memory. On failure, generate one """
    try:
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

    except (OSError, FileNotFoundError):
        from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
        from keras.models import Sequential
        from keras.losses import categorical_crossentropy
        from keras.optimizers import Adadelta
        from pickle import dump
        import numpy as np
        import time

        print('Generating model')

        print('Data preprocessing')
        input_shape = (params.img_rows, params.img_cols, 1)
        train_generator = params.datagen.flow_from_directory(
            directory=params.directory + './train/',
            target_size=(params.img_rows, params.img_cols),
            classes=params.classes,
            color_mode='grayscale',
            batch_size=params.batch_size,
        )
        valid_generator = params.datagen.flow_from_directory(
            directory=params.directory + './valid/',
            target_size=(params.img_rows, params.img_cols),
            classes=params.classes,
            color_mode='grayscale',
            batch_size=params.batch_size,
        )

        print('Model design')
        model = Sequential()
        model.add(Conv2D(
            32,
            kernel_size=(3, 3),
            activation='relu',
            input_shape=input_shape,
        ))
        model.add(Conv2D(
            64,
            kernel_size=(3, 3),
            activation='relu',
            input_shape=input_shape,
        ))
        model.add(MaxPooling2D(
            pool_size=(2, 2),
        ))
        model.add(Dropout(
            0.25,
        ))
        model.add(Flatten(
        ))
        model.add(Dense(
            128,
            activation='relu',
        ))
        model.add(Dropout(
            0.5,
        ))
        model.add(Dense(
            len(params.classes),
            activation='softmax',
        ))
        model.compile(
            loss=categorical_crossentropy,
            optimizer=Adadelta(),
            metrics=['accuracy'],
        )

        print('Model training')
        start = time.time()
        model_hist = model.fit_generator(
            train_generator,
            steps_per_epoch=len(train_generator),
            epochs=params.num_epoch,
            verbose=1,
            validation_data=valid_generator,
            validation_steps=len(valid_generator),
        )
        end = time.time()
        print("Training time: {:.0f}s".format(end-start))

        print('Saving model generation results')
        model.save(filename + '.h5')
        with open(filename + '.hist', 'wb') as hist_file:
            dump(model_hist, hist_file)
        with open(filename + '.params', 'wb') as params_file:
            dump(params, params_file)

        print('Returning model')
        return model, model_hist


if __name__ == '__main__':
    from argparse import ArgumentParser
    from keras.preprocessing.image import ImageDataGenerator
    from os import remove

    parser = ArgumentParser(description='Execute [and train] a CNN model')
    parser.add_argument('-t', action='store_true',
                        help='Delete saved model, retrain')
    parser.add_argument('-m', action='store', nargs='?', default='dice',
                        help='Filename for storing the model and history')
    args = parser.parse_args()

    if args.t:
        try:
            remove(args.m + '.h5')
            remove(args.m + '.hist')
            remove(args.m + '.params')
        except OSError:
            print('No model to delete')

    print('Define model params')
    params = ModelParams(
        img_rows=28,
        img_cols=28,
        batch_size=10,
        num_epoch=1,
        classes=['d4', 'd6', 'd8', 'd10', 'd12', 'd20'],
        directory='./dice/',
        datagen=ImageDataGenerator(rescale=1./255),
    )

    print('Create model')
    model, model_hist = create_model(args.m, params)

    print('Model summary:')
    print(model.summary())
    print()

    print('Model generation history:')
    for x in model_hist.history.keys():
        print('{}: {}'.format(x, model_hist.history[x]))
    print()

    print('Model results on the ./test dataset:')
    test_generator = params.datagen.flow_from_directory(
        directory='./test/',
        target_size=(params.img_rows, params.img_cols),
        classes=params.classes,
        color_mode='grayscale',
        batch_size=params.batch_size,
    )
    model_results = model.evaluate_generator(test_generator,
                                             steps=len(test_generator))
    for idx, label in enumerate(model.metrics_names):
        print('{}: {}'.format(label, model_results[idx]))
