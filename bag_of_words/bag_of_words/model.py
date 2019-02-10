
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def train_random_forest():
    # ****** Fit a random forest and extract predictions
    #
    forest = RandomForestClassifier(n_estimators = 100)

    # Fitting the forest may take a few minutes
    print("Fitting a random forest to labeled training data...")
    forest = forest.fit(train_centroids, train["sentiment"])
    result = forest.predict(test_centroids)

    # Write the test results
    output = pd.DataFrame(data={"id": test["id"], "sentiment":result})
    output.to_csv("BagOfCentroids.csv", index=False, quoting=3)
    print("Wrote BagOfCentroids.csv")

