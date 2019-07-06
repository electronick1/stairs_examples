from stairs import producer_signals

from core.app_config import app
from core.pipelines import prepare_image_for_nn


@app.producer(prepare_image_for_nn)
def read_image():
    pass


@app.batch_producer(read_image,
                    repeat_on_signal=producer_signals.on_pipeline_empty,
                    repeat_times=app.config.num_epoch)
def read_batch_of_images():
    pass
