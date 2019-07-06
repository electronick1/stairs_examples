import numpy as np
import imgaug.augmenters as iaa
from keras.utils.np_utils import to_categorical

from core.app_config import app


def apply_normalization(image):
    image = np.asarray(image)
    image = image / 255.0

    return dict(image=image)


def apply_reshape(image):
    image = image.reshape(28, 28, 1)

    return dict(image=image)


def apply_augmentation(image):
    data_aug: iaa.Sequential = app.config.data_augmentation

    image = data_aug(image=image)
    return dict(image=image)


def encode_image(image):
    return dict(image=np.asarray([image]))


def encode_labels(label):
    label = to_categorical(label, num_classes=app.config.num_classes)
    return dict(label=np.asarray([label]))