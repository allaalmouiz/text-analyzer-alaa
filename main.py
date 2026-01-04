# main.py
import re
from collections import Counter
import spacy
import contractions

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Optional: add custom MixedCase / technical terms
CUSTOM_ENTITIES = ["OpenAI", "README", "LangChain", "FastAPI", "GitHub"]

def read_text_file(filepath):
    """
    Reads a text file safely with error handling
    """
    print("\nStarting to read the file...")
    print(f"Reading file: {filepath}")
    print("==========="*5)
    print("")

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            return content

    except FileNotFoundError:
        print("Error: File not found.")
    except PermissionError:
        print("Error: Permission denied.")
    except UnicodeDecodeError:
        print("Error: Encoding issue.")
    except OSError as e:
        print(f"Error: OS error: {e}")



def normalize_text_robust(text):
    """
    Robust text normalization:
    - Expand contractions
    - Replace emails, URLs, tickets with placeholders
    - Normalize whitespace
    - Normalize punctuation
    - Preserve numbers, hyphenated words, MixedCase, symbols
    - Collapse repeated words
    """
    
    # --- Expand contractions ---
    text = contractions.fix(text)
    
    # --- Replace placeholders ---
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', 'EMAIL_TOKEN', text)
    text = re.sub(r'https?://\S+', 'URL_TOKEN', text)
    text = re.sub(r'\b[A-Z]{2,}-\d{4,}-\d+\b', 'TICKET_TOKEN', text)
    
    # --- Normalize whitespace ---
    text = re.sub(r'\s*\n\s*', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # --- Normalize repeated punctuation ---
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'!{2,}', '!', text)
    text = re.sub(r'\?{2,}', '?', text)
    
    # Remove unwanted punctuation except .!?-$#@ and hyphens
    text = re.sub(r'[\"\'():,;]', '', text)
    
    # --- Protect hyphenated words temporarily ---
    text = re.sub(r'\b(\w+(?:-\w+)+)\b', lambda m: m.group(0).replace("-", "~"), text)
    
    # --- spaCy processing ---
    doc = nlp(text)
    
    # --- Process words ---
    words = []
    for token in doc:
        # Preserve MixedCase / entities / numbers / hyphenated / symbols
        if token.ent_type_ in ['PERSON', 'ORG', 'GPE', 'PRODUCT'] or token.text in CUSTOM_ENTITIES:
            words.append(token.text)
        elif token.like_num:
            words.append(token.text)
        elif re.match(r'^[#@$]\w+', token.text):  # hashtags, mentions, symbols
            words.append(token.text)
        elif token.is_punct or token.is_space:
            continue  # skip punctuation entirely
        else:
            words.append(token.text.lower())
    
    # Collapse repeated words and restore hyphens
    collapsed_words = []
    prev_word = None
    for w in words:
        w = w.replace("~", "-")
        if w != prev_word:
            collapsed_words.append(w)
        prev_word = w
    
    normalized_text = ' '.join(collapsed_words)
    
    # --- Sentences ---
    sentences = [sent.text.strip().replace("~", "-") for sent in doc.sents]

    
    # --- Word & sentence counts ---
    word_count = len(collapsed_words)
    sentence_count = len(sentences)
    
    # --- Frequent words ---
    import string

    freq_words = Counter(
        w for w in collapsed_words
        if not all(ch in string.punctuation for ch in w) ).most_common(10)

    
    return {
        'normalized_text': normalized_text,
        'sentences': sentences,
        'words': collapsed_words,
        'word_count': word_count,
        'sentence_count': sentence_count,
        'frequent_words': freq_words
    }


# --- Helper functions ---

def list_words(text):
    """Return a list of normalized words (punctuation removed)"""
    result = normalize_text_robust(text)
    return result['words']

def list_sentences(text):
    """Return a list of sentences"""
    result = normalize_text_robust(text)
    return result['sentences']


# --- Main function ---
def main():
    file = read_text_file("sample_text.txt")
    if not file:
        return
    
    print("File snippet:\n", file[:200])
    
    result = normalize_text_robust(file)
    
    print("\n========== Normalized Results ==========")
    print("Normalized Text:\n", result['normalized_text'])
    print("\nSentence Count:", result['sentence_count'])
    print("Word Count:", result['word_count'])
    print("Top Frequent Words:", result['frequent_words'])
    
    print("\nAll Sentences:")
    for i, sentence in enumerate(result['sentences'], 1):
        print(f"{i}: {sentence}")
    
    print("\nAll Words:")
    print(result['words'])


if __name__ == "__main__":
    main()
