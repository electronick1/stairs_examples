import csv

from stairs import producer_signals

from core.app_config import app
from core.pipelines import prepare_image_for_nn


@app.producer(prepare_image_for_nn,
              repeat_on_signal=producer_signals.on_all_components_empty,
              repeat_times=app.config.num_epoch)
def read_image():
    with open('data/train.csv') as csv_file:
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
