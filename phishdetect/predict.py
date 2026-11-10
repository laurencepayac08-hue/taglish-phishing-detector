import argparse
import sys

import joblib


def main():
    parser = argparse.ArgumentParser(description="Check if a message looks like phishing.")
    parser.add_argument("message", help="the message text, in quotation marks")
    parser.add_argument("--model", default="models/model.joblib")
    args = parser.parse_args()

    try:
        model = joblib.load(args.model)
    except FileNotFoundError:
        print("No trained model found. Run this first: python -m phishdetect.train")
        sys.exit(1)

    classes = list(model.classes_)
    probability = model.predict_proba([args.message])[0][classes.index("phishing")]
    label = "PHISHING" if probability >= 0.5 else "LEGIT"
    print(f"{label} (phishing probability: {probability:.0%})")


if __name__ == "__main__":
    main()
