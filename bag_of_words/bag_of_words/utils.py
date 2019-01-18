import numpy as np
from bag_of_words.app_config import app


def words_to_centroids(words):
    word_centroid_map = app.config.centroids

    num_centroids = max(word_centroid_map.values()) + 1
    #
    # Pre-allocate the bag of centroids vector (for speed)
    bag_of_centroids = np.zeros(num_centroids, dtype="float32")

    for word in words:
        if word in word_centroid_map:
            index = word_centroid_map[word]
            bag_of_centroids[index] += 1
        #
        # Return the "bag of centroids"
    return bag_of_centroids
