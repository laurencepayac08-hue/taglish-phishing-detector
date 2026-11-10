# Data

`sample_messages.csv` holds synthetic messages written for this demo. No message comes from a real person, and every link uses the reserved `.example` domain.

## Format

A CSV file with two columns:

| column | value |
|--------|-------|
| text   | the message |
| label  | `phishing` or `legit` |

## Using your own messages

1. Save your messages in `data/private/messages.csv`. This folder is ignored by Git, so the file never reaches GitHub.
2. Remove names, phone numbers, account numbers, and real links before you save a message.
3. Train with your file:

```
python -m phishdetect.train --data data/private/messages.csv
```

Only publish data that is synthetic or fully anonymous, and only with the permission of the people who wrote the messages.
