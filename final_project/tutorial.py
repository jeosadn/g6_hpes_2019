#!/bin/env python3


def create_model():
    try:
        from keras.models import load_model
        return load_model('mnist_model.h5')
    except OSError:
        from keras.datasets import mnist
        from keras.layers import Dense, Conv2D, Flatten
        from keras.models import Sequential
        from keras.utils import to_categorical

        (X_train, y_train), (X_test, y_test) = mnist.load_data()
        X_train = X_train.reshape(60000, 28, 28, 1)
        X_test = X_test.reshape(10000, 28, 28, 1)
        y_train = to_categorical(y_train)
        y_test = to_categorical(y_test)
        model = Sequential()
        model.add(Conv2D(64, kernel_size=3, activation='relu'))
        model.add(Flatten())
        model.add(Dense(10, activation='softmax'))
        model.compile(optimizer='adam', loss='categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3)
        model.save('mnist_model.h5')
        return model


if __name__ == '__main__':
    from argparse import ArgumentParser
    from keras.datasets import mnist
    from os import remove

    parser = ArgumentParser(description='Execute [and train] a CNN model')
    parser.add_argument('-t', action='store_true',
                        help='Delete saved model, retrain')
    args = parser.parse_args()

    if args.t:
        try:
            remove('mnist_model.h5')
        except OSError:
            print('No model to delete')

    model = create_model()

    test = mnist.load_data()[1][0].reshape(10000, 28, 28, 1)

    print(model.predict(test[:3]))
