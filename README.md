# Pyhton Text Analyzer 
`text-analyzer-alaa`
#spaCy Text Analyzer

A simple, efficient Python script for analyzing text files using **spaCy**.

This tool performs:

* Word count
* Sentence count
* Top 10 most frequent words
  
It uses **linguistic tokenization and lemmatization**, not naive string splitting, making the results more meaningful for NLP analysis.

## Features

* Uses spaCy’s tokenizer and sentence segmenter
* Lemmatizes words and normalizes case
* Preserves numbers, symbols, hashtags, and mentions
* Filters punctuation safely
* Robust file reading with error handling

## Project Structure

```
.
├── main.py
├── sample_text.txt
├── requirements.txt
└── README.md
```

## Requirements

Contents of `requirements.txt`:

```
spacy
nltk
contractions
emoji
regex
en_core_web_sm
```

## Environment Setup

### 1. Creating a virtual environment

**macOS / Linux**

```bash
python -m venv venv
```

### 2. Activating the environment

**macOS / Linux**

```bash
source venv/bin/activate
```

You should now see `(venv)` in your terminal.

### 3. Installing dependencies

```bash
pip install -r requirements.txt
```

### 4. Downloading the spaCy language model

```bash
python -m spacy download en_core_web_sm
```

This step is required — the script will not run without the model.

## 5. Running the Program

1. Place your text inside `sample_text.txt`
2. Run the script:

```bash
python main.py
```

##  Example Output

```
====== STARTING READING THE FILE ======
FILE: sample_text.txt
=======================================


========== ANALYSIS STARTING ==========
File sample_text.txt is being analyzed.

========== ANALYSIS RESULTS ===========
Word Count: 289
Sentence Count: 34

Top 10 Frequent Words:
1. ai (7)
2. and (7)
3. we (4)
4. are (4)
5. repeat (4)
...
```

## How It Works (High Level)

* Text is processed once using `nlp(text)`
* Sentences are extracted via `doc.sents`
* Words are counted after:

  * removing punctuation
  * lemmatizing
  * lowercasing
* Frequencies are computed using `collections.Counter`

This ensures **consistent, linguistically grounded statistics**.


## License

This project is for educational and research use, and it's a part of AbdoKomar mentorship.
Feel free to adapt, extend, and experiment.



This is solid groundwork.
