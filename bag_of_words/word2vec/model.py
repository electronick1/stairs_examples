import pickle
from gensim.models import Word2Vec

from word2vec.app_config import app
from word2vec.consumers import fit_to_word2vec

from sklearn.cluster import KMeans


def train_word2vec():
    print("Training Word2Vec model...")
    config = app.config

    sentences = []
    for s in fit_to_word2vec():
        sentences.append(s)
        if len(sentences) > 20000:
            break

    model = Word2Vec(sentences,
                     workers=config.num_workers,
                     size=config.num_features,
                     min_count=config.min_word_count,
                     window=config.context,
                     sample=config.downsampling,
                     seed=1)

    # If you don't plan to train the model any further, calling
    # init_sims will make the model much more memory-efficient.
    model.init_sims(replace=True)

    # It can be helpful to create a meaningful model name and
    # save the model for later use. You can load it later using Word2Vec.load()
    model.save(config.model_path)


def train_kmean():
    model = Word2Vec.load(app.config.model_path)

    word_vectors = model.wv.syn0
    num_clusters = word_vectors.shape[0] / 5

    kmeans_clustering = KMeans(n_clusters=num_clusters)
    idx = kmeans_clustering.fit_predict(word_vectors)
    word_centroid_map = dict(zip(model.wv.index2word, idx))

    pickle.dump(word_centroid_map, app.config.word_centroid_map_path)


if __name__ == "__main__":
    pass
    #train_word2vec()
    #train_kmean()