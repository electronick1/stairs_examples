import csv

from stairs import producer_signals

from core.app_config import app
from core.pipelines import prepare_image_for_nn


@app.producer(prepare_image_for_nn,
              repeat_on_signal=producer_signals.on_all_components_empty,
              repeat_times=app.config.num_epoch)
def read_image():
    """
    Reads data from a file and forward each image and label to
    `prepare_image_for_nn` pipeline through streaming service.

    Also `read_image` producer allows you to split data on 'training' and
    'validation' datasets.

    When all data in pipelines where consumed by neural network - producer
    will repeat itself until amount of epochs specified in app config.
    """
    with open(app.config.train_data_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # skip first line
        next(csv_reader)

        for i, row in enumerate(csv_reader):
            is_train_data = i > app.config.num_validation_images

            yield dict(
                label=int(row[0]),
                image=list(map(int, row[1:])),
                is_train_data=is_train_data
            )
