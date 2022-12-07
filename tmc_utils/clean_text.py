"""Procedures for pre-processing Czech text.

This module cleans Czech text following these steps: remove numbers, convert to
lowercase (except for names), remove punctuation, remove double spaces, remove
stopwords, tokenize, lemmatize, and filter out 1 letter words.

The module contains the following functions:

- `text_cleaner_cz(text_string)` - Prepares the SOCKS proxy for TOR
"""

import re
import string
import nltk
# from sumy.nlp.stemmers import czech
from stop_words import get_stop_words
import simplemma as sl


# Lemmatization needs help with some words
lemma_helper = {
  "koronavirus": [
    "koronavir",
    "koronaviru",
    "koronavire",
    "koronavirem",
    "koronaviry",
    "koronavirů",
    "koronavirům",
    "koronavirech"
  ],
  "covid": [
    "covid",
    "covidu",
    "covide",
    "covidem",
    "covidy",
    "covidů",
    "covidům",
    "covidech"
  ]
}



def sentence_cleaner_cz(text_string: str):
    """Pre-process Czech text for text mining

    Args:
        text_string (str): Text to be pre-processed

    Returns:
        list: List of lowercase words (no numbers, punctuation, or symbols)
    """
    # Download tokenizer and define stopwords
    nltk.download("punkt", quiet=True)
    stop_words = get_stop_words("czech")
    punct_and_symbols = string.punctuation + "„“"

    # Remove: numbers, symbols, punctuation, double whitespaces, stopwords
    text_nonum = re.sub(r"\d+", "", text_string).lower()
    text_nopunct = text_nonum.translate(
        str.maketrans("", "", punct_and_symbols)
    )
    text_nodbl = re.sub(" +", " ", text_nopunct).strip()
    text_cleaned = " ".join(
        [word for word in text_nodbl.split() if word not in stop_words]
    )

    # Tokenize words and sort alphabetically to break up meaning
    token_words = sorted(nltk.tokenize.word_tokenize(text_cleaned))

    # Lemmatize instead of stemming, note that lemmatization can introduce
    # uppercase words, e.g., germany -> Germany. We omit this feature.
    token_words_lm = [
        sl.lemmatize(t, lang="cs").lower() for t in token_words if len(t) > 1
    ]

    return token_words_lm
