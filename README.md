# Taglish Phishing Detector

A machine learning project that checks if a text message looks like phishing. It works with Taglish, the mix of Tagalog and English used in many scam messages in the Philippines.

## How it works

1. **Clean the text.** Links and numbers become placeholders, so the model learns from the wording of a message and not from one link or one amount.
2. **Turn text into numbers.** TF-IDF on character n-grams handles Taglish spelling variations such as `ma-verify` and `maverify`.
3. **Classify.** Logistic regression returns the probability that a message is phishing.

## Setup

You need Python 3.10 or newer.

```
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

On macOS or Linux, use `source .venv/bin/activate` for the second line.

## Usage

Train the model and see the results on messages it has not seen:

```
python -m phishdetect.train
```

Check a message:

```
python -m phishdetect.predict "GCash: Naka-lock ang account mo. I-verify dito http://x.example at ilagay ang OTP"
```

Output:

```
PHISHING (phishing probability: 66%)
```

Run the tests:

```
python -m pytest
```

## Data and privacy

The included `data/sample_messages.csv` has 63 synthetic messages written for this demo. No message comes from a real person, and every link uses the reserved `.example` domain.

To train on real messages, put them in `data/private/messages.csv`. Git ignores this folder, so private messages never reach GitHub. Remove names, phone numbers, account numbers, and real links first. See `data/README.md` for the format.

## Results

Training on the sample data and testing on 16 held-out messages gives 88% accuracy, with one mistake in each class. This number only shows that the pipeline works. The dataset is small and synthetic, so the score does not predict how the model performs on real messages.

## Limitations

- The model learns only from the messages it is given. Scam wording changes often, so it needs fresh data.
- A short or unusual message gives an unreliable score.
- The tool supports a person who checks a message. It does not replace careful judgment.

## Project structure

```
phishdetect/   data loading, model, training, and prediction code
tests/         pytest tests
data/          sample data and instructions for private data
models/        trained model (not uploaded to GitHub)
```

## Roadmap

- [x] Baseline model with character n-grams
- [x] Automated tests
- [ ] Collect at least 200 anonymized messages per class
- [ ] Cross-validation and more metrics
- [ ] Show which words drive each prediction
- [ ] Web demo
