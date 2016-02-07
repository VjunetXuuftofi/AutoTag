import pandas as pd
import re
from nltk.corpus import stopwords
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.ensemble import RandomForestClassifier


def modify (description):
    try:
        everyword = re.sub("[^a-zA-Z]", " ", description).lower().split()
        cleaned = [w for w in everyword if not w in stopwords.words("english")]
        return " ".join(cleaned)
    except:
        return None

def initialize(filename):
    data = pd.read_csv(filename)
    for index in tqdm(range(0, len(data))):
        data["description"][index] = modify(data["description"][index])
    olddata = data[data.description.notnull()]
    vectorizer = CountVectorizer(analyzer = "word",
                                 tokenizer = None,
                                 preprocessor = None,
                                 stop_words = None,
                                 max_features = 10000,
                                 ngram_range = (1,3))
    data = vectorizer.fit_transform(olddata["description"])
    data = data.toarray()
    forest1 = RandomForestClassifier(n_estimators = 100)
    forest1 = forest1.fit(data, olddata["value"])
    return forest1, vectorizer








