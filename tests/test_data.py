import pytest

from phishdetect.data import load_messages, normalize


def test_normalize_replaces_links_and_numbers():
    assert normalize("Claim P50,000 at http://promo.example/win now") == "claim p num at url now"


def test_normalize_lowercases_and_trims_spaces():
    assert normalize("  HELLO   World ") == "hello world"


def test_load_messages_reads_text_and_labels(tmp_path):
    file = tmp_path / "messages.csv"
    file.write_text('text,label\n"Hello, kumusta?",legit\nVerify now,PHISHING\n', encoding="utf-8")
    texts, labels = load_messages(file)
    assert texts == ["Hello, kumusta?", "Verify now"]
    assert labels == ["legit", "phishing"]


def test_load_messages_rejects_unknown_label(tmp_path):
    file = tmp_path / "messages.csv"
    file.write_text("text,label\nHello,spam\n", encoding="utf-8")
    with pytest.raises(ValueError, match="label"):
        load_messages(file)


def test_load_messages_rejects_missing_columns(tmp_path):
    file = tmp_path / "messages.csv"
    file.write_text("message,tag\nHello,legit\n", encoding="utf-8")
    with pytest.raises(ValueError, match="columns"):
        load_messages(file)


def test_load_messages_skips_blank_rows(tmp_path):
    file = tmp_path / "messages.csv"
    file.write_text("text,label\n,legit\nHello,legit\n", encoding="utf-8")
    texts, _ = load_messages(file)
    assert texts == ["Hello"]


def test_sample_dataset_is_balanced():
    _, labels = load_messages("data/sample_messages.csv")
    assert abs(labels.count("phishing") - labels.count("legit")) <= 5
