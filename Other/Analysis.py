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

Provides tools for machine learning new autotags.
"""
import pandas as pd
import nltk
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_selection import SelectPercentile, f_classif
import re
from sklearn.grid_search import GridSearchCV

stemmer = SnowballStemmer("english")  # This is done in the main body to avoid redundancy


def modify(description):
    """
    Takes in a text description and returns the description in a format that is readily interpretable by a Vectorizer.
    Also stems words in the description.
    :param description:
    :return cleaned description:
"""
    words = ""
    description = nltk.wordpunct_tokenize(description)
    for word in description:
        word = word.replace(" ", "")
        word = re.sub("[0-9]", "#", word)
        words += stemmer.stem(word) + " "
    words = words[:-1]
    return words


def convert(filename):
    """
    Converts a file containing features and labels into two pandas dataframes.
    :param filename:
    :return features:
    :return labels:
    """
    data = pd.read_csv(filename)
    data = data[data.description.notnull()]
    features = data["description"]
    labels = data["value"]
    for index in tqdm(range(0, len(features))):
        try:
            features[index] = modify(features[index])
        except:
            print(features[index-1])
    return features, labels

def initialize(name, params = None):
    """
    Reads a csv file with text descriptions and information about whether that loan deserved the tag, puts the
    description through the modify function, and returns a vectorizer, random forest classifier, and selector for use
    in making predictions about new loans.
    :param name: The tag's identifier. All relevant files should begin with this identifier.
    :return forest: A fitted random forest classifier for this tag.
    :return vectorizer: A fitted TFIDF vectorizer for this tag.
    :return selector: A fitted selector for this tag.
    """
    features_train, labels_train = convert("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/BagOfWords/" + name + "BagOfWords.csv")
    print("Creating Vectorizer")
    vectorizer = TfidfVectorizer(stop_words = "english",
                                 max_df = .5,
                                 ngram_range = (1,3))
    print("Fitting Vectorizer")
    features_train_transformed = vectorizer.fit_transform(features_train)
    print("Creating Selector")
    selector = SelectPercentile(f_classif,
                                percentile=10)
    print("Fitting Selector")
    selector.fit(features_train_transformed,
                 labels_train)
    print("Transforming data")
    features_train_transformed_selected = selector.transform(features_train_transformed).toarray()
    print("Creating Forest")
    if not params:
        forest = RandomForestClassifier()
        parameters = {
            "n_estimators" : [50, 150, 250],
            "min_samples_leaf" : [2, 5, 7, 10]
        }
        forest = GridSearchCV(forest,
                              parameters)
    else:
        forest = RandomForestClassifier(n_estimators=params[0],
                                        min_samples_leaf=params[1])
    print("Fitting Forest")
    forest.fit(features_train_transformed_selected,
                        labels_train)
    return forest, vectorizer, selector









