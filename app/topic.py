import pickle

import numpy as np
import pandas as pd

from preprocess import Preprocess
from twitter import Twitter


def topic_run(data, lang):
    # preprocess data
    processor = Preprocess()
    processor.fit(data, lang)
    clean_data = processor.data

    # prepare X
    X = clean_data.text.apply(lambda x: np.str_(x))

    # vectorize data
    address = "app/vectorizer/topic/tfidf_fa.sav"
    loaded_vectorizer = pickle.load(open(address, "rb"))
    X_vector = loaded_vectorizer.transform(X)

    # rf model
    address = "app/models/topic/random_forest/rf_fa.sav"
    loaded_rf_model = pickle.load(open(address, "rb"))
    prediction = loaded_rf_model.predict(X_vector)

    # add prediction to data
    y = pd.DataFrame(prediction, columns=["topic"])
    data = pd.concat([data, y], axis=1, join="inner")

    return data

