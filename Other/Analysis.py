"""
Copyright 2016 Thomas Woodside

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Creates a csv relating loan uses to whether or not the loan should receive #Animals. This is useful for the Bag of Words
approach.
"""
import pandas as pd
import re
from nltk.corpus import stopwords
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier


def modify(description):
    """
    Takes in a text description and removes punctuation, numbers, and stopwords for use in Bag of Words.
    :param description:
    :return cleaned description:
    """
    try:
        everyword = re.sub("[^a-zA-Z]", " ", description).lower().split()
        cleaned = [w for w in everyword if not w in stopwords.words("english")]
        return " ".join(cleaned)
    except:
        return None

def initialize(filename):
    """
    Reads a csv file with text descriptions and information about whether that loan deserved the tag, puts the
    description through the modify function, and returns a vectorizer and a random forest classifier for use in making
    predictions about new loans.
    :param filename:
    :return forest1:
    :return vectorizer:
    """
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








