import argparse
import os

import joblib
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from phishdetect.data import LABELS, load_messages
from phishdetect.model import build_model


def main():
    parser = argparse.ArgumentParser(description="Train the phishing detector.")
    parser.add_argument("--data", default="data/sample_messages.csv", help="CSV file with text and label columns")
    parser.add_argument("--model-out", default="models/model.joblib", help="where to save the trained model")
    parser.add_argument("--test-size", type=float, default=0.25)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    texts, labels = load_messages(args.data)
    print(f"Loaded {len(texts)} messages from {args.data}")

    x_train, x_test, y_train, y_test = train_test_split(
        texts, labels, test_size=args.test_size, random_state=args.seed, stratify=labels
    )

    model = build_model()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    print(f"\nResults on {len(x_test)} messages the model has not seen:\n")
    print(classification_report(y_test, predictions, labels=list(LABELS), zero_division=0))
    print("Confusion matrix (rows = real label, columns = prediction):")
    print(f"labels: {list(LABELS)}")
    print(confusion_matrix(y_test, predictions, labels=list(LABELS)))

    # Train again on every message before saving, so the final model uses all the data.
    model.fit(texts, labels)
    os.makedirs(os.path.dirname(args.model_out) or ".", exist_ok=True)
    joblib.dump(model, args.model_out)
    print(f"\nSaved the model to {args.model_out}")


if __name__ == "__main__":
    main()
