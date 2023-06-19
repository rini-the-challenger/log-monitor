import string

import nltk
import pathlib
from yml_admin import YmlAdmin
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier

import pandas as pa

"""
Responsible for doing the search
"""

training_data = [
    ("Error: Disk full", "error"),
    ("Warning: Connection lost", "warning"),
    ("Error: Invalid input", "error"),
    # Add more labeled log entries
]


def classify_log_entry(entry):
    preprocessed_data = [(preprocess_text(entry), label) for entry, label in training_data]
    classifier = NaiveBayesClassifier.train(preprocessed_data)

    preprocessed_entry = preprocess_text(entry)

    return classifier.classify(dict([(token, True) for token in preprocessed_entry]))


def preprocess_text(text):
    """ Preprocess training data Before training the classifier, preprocess the training data by tokenizing the log
        entries, removing stop words and punctuation, and converting the text to lowercase
    """

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove punctuation
    tokens = [token for token in tokens if token not in string.punctuation]

    # Remove stop words
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token.lower() not in stop_words]

    # Convert to lowercase
    tokens = [token.lower() for token in tokens]

    return tokens


def read_log():
    yml = YmlAdmin()
    yml.read_yaml()
    root = yml.settings['APP']['ROOT-DIR']
    root_path = pathlib.Path(root)

    # root_path.iterdir()

    # Iterate and check for log files
    for item in root_path.rglob("*"):
        print(f"{item} - {'dir' if item.is_dir() else 'file'}")
        if item.is_file():
            # Read log file and classify each entry
            with open(item) as file:

                for line in file:
                    classification = classify_log_entry(line)
                    if classification == "error":
                        print(f"Error: {line.strip()}")
                    elif classification == "warning":
                        print(f"Warning: {line.strip()}")
