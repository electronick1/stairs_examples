from core.app_config import app


@app.pipeline()
def prepare_image_for_nn(pipeline, image):
    return (image
            .subscribe_func(apply_normalization)
            .subscrube_func(apply_reshape)
            .subscribe_func(encode_labels)
            .subscribe_consumer(deliver_to_model))
