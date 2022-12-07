"""Procedures for pre-processing Czech text.

This module cleans Czech text following these steps: remove numbers, convert to
lowercase (except for names), remove punctuation, remove double spaces, remove
stopwords, tokenize, stem after lemmatization, and filter out 1 letter words.
Note that, people usually choose either stemming or lemmatization in text
mining analyses. However, while the lemmatization tool that we use works very
well, on its own, it doesn't seem to recognize words such as "koronavirus,"
which is of paramount importance to our analysis. Thus, we unconventionally
apply both techniques.


The module contains the following functions:

- `text_cleaner_cz(text_string)` - Cleans Czech text for text mining
"""

import re
import string
import nltk
import simplemma as sl
from sumy.nlp.stemmers import czech
from stop_words import get_stop_words


def sentence_cleaner_cz(text_string: str):
    """Pre-process Czech sentences for text mining

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

    # Use both lemmatization and stemming, see module description
    token_words_lm = [
        czech.stem_word(sl.lemmatize(t, lang="cs").lower())
        for t in token_words
        if len(t) > 1
    ]

    return token_words_lm
