import pickle
from stairs import App
from word2vec.app_config import app as word2vec_app

app = App("bag_of_words")


@app.on_app_created()
def init_centroids_data(app):
    data_path = word2vec_app.config.word_centroid_map_path
    app.config.centroids = pickle.load(data_path)
