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
        from keras.backend import image_data_format
        from keras.datasets import mnist
        from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
        from keras.models import Sequential
        from keras.utils import to_categorical
        from keras.losses import categorical_crossentropy
        from keras.optimizers import Adadelta
        from pickle import dump
        import numpy as np
        import time

        print('Generating model')

        print('Data preprocessing')
        (X_train, y_train), (X_test, y_test) = mnist.load_data()
        if image_data_format() == 'channels_first':
            X_train = X_train.reshape(X_train.shape[0], 1, params.img_rows,
                                      params.img_cols)
            X_test = X_test.reshape(X_test.shape[0], 1, params.img_rows,
                                    params.img_cols)
            input_shape = (1, params.img_rows, params.img_cols)
        else:
            X_train = X_train.reshape(X_train.shape[0], params.img_rows,
                                      params.img_cols, 1)
            X_test = X_test.reshape(X_test.shape[0], params.img_rows,
                                    params.img_cols, 1)
            input_shape = (params.img_rows, params.img_cols, 1)

        X_train = X_train.astype('float32')
        X_test = X_test.astype('float32')
        X_train /= 255
        X_test /= 255

        print('X_train[0] shape', X_train[0].shape)
        print('X_train shape:', X_train.shape)
        print(X_train.shape[0], 'train_samples')
        print(X_test.shape[0], 'test samples')

        print(np.unique(y_train, return_counts=True))
        num_category = len(np.unique(y_train))

        y_train = to_categorical(y_train, num_category)
        y_test = to_categorical(y_test, num_category)

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
            num_category,
            activation='softmax'
        ))
        model.compile(
            loss=categorical_crossentropy,
            optimizer=Adadelta(),
            metrics=['accuracy'],
        )

        print('Model training')
        start = time.time()
        model_hist = model.fit(
            X_train,
            y_train,
            batch_size=params.batch_size,
            epochs=params.num_epoch,
            verbose=1,
            validation_data=(X_test, y_test)
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
    from keras.datasets import mnist
    from keras.utils import to_categorical
    from os import remove

    parser = ArgumentParser(description='Execute [and train] a CNN model')
    parser.add_argument('-t', action='store_true',
                        help='Delete saved model, retrain')
    parser.add_argument('-m', action='store', nargs='?', default='model',
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
    X_test = mnist.load_data()[1][0].reshape(10000, 28, 28, 1)
    y_test = to_categorical(mnist.load_data()[1][1])
    model_results = model.evaluate(X_test, y_test)
    for idx, label in enumerate(model.metrics_names):
        print('{}: {}'.format(label, model_results[idx]))
