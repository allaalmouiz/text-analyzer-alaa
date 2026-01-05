import spacy
from collections import Counter
import string

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")


def analyze_text_spacy(text):
    """
    spaCy-based text analysis:
    - Word count
    - Sentence count
    - Top 10 frequent words
    - Top 10 frequent sentences
    """

    doc = nlp(text)

    # ---------- SENTENCES ----------
    sentences = [
        sent.text.strip()
        for sent in doc.sents
        if sent.text.strip()
    ]

    sentence_count = len(sentences)
    top_sentences = Counter(sentences).most_common(10)

    # ---------- WORDS ----------
    words = []
    for token in doc:
        if token.is_space or token.is_punct:
            continue

        # Keep numbers
        if token.like_num:
            words.append(token.text)
            continue

        # Keep hashtags / mentions / symbols
        if token.text.startswith(("#", "@", "$")):
            words.append(token.text)
            continue

        # Lemmatize + lowercase
        lemma = token.lemma_.lower()

        # Skip pure punctuation or empty lemmas
        if lemma and not all(ch in string.punctuation for ch in lemma):
            words.append(lemma)

    word_count = len(words)
    top_words = Counter(words).most_common(10)

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "top_words": top_words,
        "top_sentences": top_sentences,
    }

# ---------- File reader ----------
def read_text_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("File not found.")
        return None


# ---------- Main ----------
def main():
    text = read_text_file("sample_text.txt")
    if not text:
        return

    result = analyze_text_spacy(text)

    print("\n========== ANALYSIS STARTING ==========")
    print(f"File %s is being analyzed." % "sample_text.txt")

    print("\n========== ANALYSIS RESULTS ==========")
    print("Word Count:", result["word_count"])
    print("Sentence Count:", result["sentence_count"])

    print("\nTop 10 Frequent Words:")
    for i, (word, freq) in enumerate(result["top_words"], 1):
        print(f"{i}. {word} ({freq})")


if __name__ == "__main__":
    main()
