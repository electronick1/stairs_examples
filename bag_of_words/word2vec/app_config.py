from stairs import App

app = App('word2vec')


train_word2vec_config = dict(
    num_features=300,    # Word vector dimensionality
    min_word_count=40,   # Minimum word count
    num_workers=4,       # Number of threads to run in parallel
    context=10,          # Context window size
    downsampling=1e-3,   # Downsample setting for frequent words
    model_path='300features_40minwords_10context',
    word_centroid_map_path='word_centroid_map.pickle',
)
