from nltk.corpus import stopwords
from nltk.stem.porter import *

stop_words = set(stopwords.words('english'))
stop_words.update(set(["list", "de"]))

def has_suffix(title):
    return '_(' in title


def get_suffix(title):
    if '_(' in title:
        index = title.index('_(')
        return title[index + 2:-1]
    return ''

def trim_suffix(clue_title):
    if '_(' in clue_title:
        index = clue_title.index('_(')
        return clue_title[:index]
    return clue_title


def extract_clue_word(clue_title, term):
    clue_title = trim_suffix(clue_title)
    if '_' in clue_title:
        clue_title = clue_title.split('_')[-1]
    if clue_title.lower() == term.lower():
        return None
    return clue_title.upper()


def count_title_words(clue_title):
    clue_title = trim_suffix(clue_title)
    return clue_title.count('_') + 1


def extract_title_words(title):
    title = trim_suffix(title)
    title_words = title.split('_')

    cleaned_title_words = []
    for word in title_words:
        # Clean out &, "Mirmo!", "St."
        alphanumeric = [c for c in word if c.isalnum() or c == '-']
        cleaned_word = "".join(alphanumeric)
        if len(cleaned_word) > 0 and cleaned_word.lower() not in stop_words:
            cleaned_title_words.append(cleaned_word)

    return list(map(lambda x:x.upper(), cleaned_title_words))