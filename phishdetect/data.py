import csv
import re

LABELS = ("legit", "phishing")

URL_PATTERN = re.compile(r"(https?://\S+|www\.\S+)", re.IGNORECASE)
NUMBER_PATTERN = re.compile(r"\d[\d,.]*")


def normalize(text):
    """Make messages comparable.

    Links and numbers are replaced with placeholders. The model then learns
    from the wording of a message and not from one specific link or number.
    This also keeps private numbers out of the training features.
    """
    text = text.lower()
    text = URL_PATTERN.sub(" url ", text)
    text = NUMBER_PATTERN.sub(" num ", text)
    return " ".join(text.split())


def load_messages(path):
    """Read a CSV file with the columns text and label.

    Returns a list of texts and a list of labels.
    """
    texts, labels = [], []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None or not {"text", "label"} <= set(reader.fieldnames):
            raise ValueError("The CSV file needs the columns: text, label")
        for line_number, row in enumerate(reader, start=2):
            text = (row["text"] or "").strip()
            label = (row["label"] or "").strip().lower()
            if not text:
                continue
            if label not in LABELS:
                raise ValueError(f"Line {line_number}: label must be one of {LABELS}, got '{label}'")
            texts.append(text)
            labels.append(label)
    if not texts:
        raise ValueError("The CSV file has no messages")
    return texts, labels
