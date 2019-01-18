import csv
from .app_config import app
from . import pipelines


@app.producer(pipelines.train_word2vec)
def read_unlabeled_train_data():
    with open(app.config.unlabeled_data_path, 'r') as f:
        for row in csv.reader(f, header=0,  delimiter="\t", quoting=3):
            yield dict(
                review=row[1]
            )
