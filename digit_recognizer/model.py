import pickle
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.optimizers import RMSprop
from keras.callbacks import ReduceLROnPlateau

from stairs import StairsProject
StairsProject('config.py', data_pickeler=pickle)

from core.app_config import app as core_app
from core.consumers import deliver_train_data_to_model, deliver_validation_data_to_model


def get_model():
    model = Sequential()

    model.add(Conv2D(filters=32, kernel_size=(5, 5), padding='Same',
                     activation='relu', input_shape=(28, 28, 1)))
    model.add(Conv2D(filters=32, kernel_size=(5, 5), padding='Same',
                     activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='Same',
                     activation='relu'))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='Same',
                     activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(256, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation="softmax"))

    # Define the optimizer
    optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
    # Compile the model
    model.compile(optimizer=optimizer, loss="categorical_crossentropy",
                  metrics=["accuracy"])

    return model


def train(model):
    learning_rate_reduction = ReduceLROnPlateau(monitor='val_acc',
                                                patience=3,
                                                verbose=1,
                                                factor=0.5,
                                                min_lr=0.00001)

    model.fit_generator(
        deliver_train_data_to_model.iter(),
        epochs=core_app.config.num_epoch,
        validation_data=deliver_validation_data_to_model.iter(),
        verbose=1,
        steps_per_epoch=core_app.config.steps_per_epoch,
        validation_steps=core_app.config.num_validation_images,
        callbacks=[learning_rate_reduction]
    )


if __name__ == "__main__":
    train(get_model())