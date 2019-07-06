from stairs import concatenate

from core.app_config import app
from core.data_utils import (apply_normalization,
                             apply_reshape,
                             apply_augmentation,
                             encode_image,
                             encode_labels)

from core.consumers import (deliver_train_data_to_model, 
                            deliver_validation_data_to_model)


@app.pipeline()
def prepare_image_for_nn(pipeline, image, label, is_train_data):
    return (concatenate(image=image, label=label, is_train_data=is_train_data)

            .subscribe_func(apply_normalization)
            .subscribe_func(apply_reshape)
            .subscribe_func(apply_augmentation)
            .subscribe_func(encode_image)
            .subscribe_func(encode_labels)

            .subscribe_consumer(deliver_train_data_to_model, 
                                when=lambda is_train_data: is_train_data)

            .subscribe_consumer(deliver_validation_data_to_model,
                                when=lambda is_train_data: not is_train_data))
