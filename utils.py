import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_vocabulary(full_text):
    cleaned_text = clean_text(full_text)
    words = cleaned_text.split()
    return set(words)


def count_occurrences(full_text):
    cleaned_text = clean_text(full_text)
    words = cleaned_text.split()
    frequency_table = {}

    for word in words:
        if word in frequency_table:
            frequency_table[word] += 1
        else:
            frequency_table[word] = 1

    return frequency_table


def count_document_frequency(documents):
    document_frequency = {}

    for document in documents:
        cleaned_text = clean_text(document)
        words = set(cleaned_text.split())

        for word in words:
            if word in document_frequency:
                document_frequency[word] += 1
            else:
                document_frequency[word] = 1

    return document_frequency