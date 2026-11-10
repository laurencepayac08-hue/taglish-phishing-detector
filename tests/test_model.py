import pytest

from phishdetect.data import load_messages
from phishdetect.model import build_model


@pytest.fixture(scope="module")
def trained():
    texts, labels = load_messages("data/sample_messages.csv")
    model = build_model()
    model.fit(texts, labels)
    return model, texts, labels


def phishing_probability(model, message):
    classes = list(model.classes_)
    return model.predict_proba([message])[0][classes.index("phishing")]


def test_model_fits_the_training_data(trained):
    model, texts, labels = trained
    predictions = model.predict(texts)
    accuracy = sum(p == t for p, t in zip(predictions, labels)) / len(labels)
    assert accuracy >= 0.9


def test_probabilities_are_between_zero_and_one(trained):
    model, _, _ = trained
    probability = phishing_probability(model, "kumusta ka na?")
    assert 0.0 <= probability <= 1.0


def test_obvious_phishing_message_is_flagged(trained):
    model, _, _ = trained
    message = "URGENT: Naka-lock ang account mo. I-verify agad sa http://secure-login.example at ilagay ang OTP mo."
    assert phishing_probability(model, message) > 0.5


def test_everyday_message_is_not_flagged(trained):
    model, _, _ = trained
    message = "Tara kain tayo mamaya after class, libre ko kape."
    assert phishing_probability(model, message) < 0.5


def test_different_links_give_the_same_score(trained):
    model, _, _ = trained
    first = phishing_probability(model, "Verify your account at http://one.example now")
    second = phishing_probability(model, "Verify your account at http://another-site.example/x now")
    assert first == pytest.approx(second)
