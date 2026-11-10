from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from phishdetect.data import normalize


def build_model():
    """Character n-grams handle Taglish spelling variations such as 'ma-verify' and 'maverify'."""
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            preprocessor=normalize,
            analyzer="char_wb",
            ngram_range=(2, 5),
            sublinear_tf=True,
        )),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])
