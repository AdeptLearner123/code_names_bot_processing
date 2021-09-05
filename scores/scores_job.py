from utils.term_synonyms import get_synonyms
from tqdm import tqdm
import time

from utils import wiki_database
from page_extraction import page_extracts_database
from utils.title_utils import extract_title_words
from scores import scores_database
from utils import term_utils


def output_scores(term, id_to_title):
    print("Counting: " + term)
    paths = {}
    scores = {}

    get_synonym_scores(term, paths, scores)
    get_link_page_scores(term, paths, scores, id_to_title)
    get_source_page_scores(term, paths, scores, id_to_title)

    print("Inserting: {0}".format(len(scores)))
    with tqdm(total=len(scores)) as pbar:
        for clue in scores:
            if term not in clue:
                scores_database.insert_term_clue(term, clue, scores[clue], paths[clue])
            pbar.update(1)
    scores_database.commit()


def get_synonym_scores(term, paths, scores):
    for synonym in get_synonyms(term):
        if term not in synonym:
            words = synonym.split('_')
            score = 1 / len(words)
            for word in words:
                scores[word] = score
                paths[word] = ""


def get_link_page_scores(term, paths, scores, id_to_title):
    term_page_counts = page_extracts_database.get_term_page_counts(term, False)
    page_counts = {}
    for word, page_id, count in term_page_counts:
        if count is None:
            continue
        if page_id not in page_counts or page_counts[page_id] < count:
            page_counts[page_id] = count
    
    print("Count: {0}".format(len(page_counts)))
    for page_id in page_counts:
        term_count = page_counts[page_id]
        if term_count == 0:
            continue

        title = id_to_title[page_id]
        title_words = extract_title_words(title)
        if len(title_words) != 1:
            continue

        score = 1 - 0.7 ** term_count
        clue = title_words[0]
        scores[clue] = score
        paths[clue] = title


def get_source_page_scores(term, paths, scores, id_to_title):
    term_page_counts = page_extracts_database.get_term_page_counts(term, True)
    word_counts = {}
    word_page = {}
    with tqdm(total=len(term_page_counts)) as pbar:
        for word, page_id, count in term_page_counts:
            if word not in word_counts or word_counts[word] < count:
                word_counts[word] = count
                word_page[word] = page_id
            pbar.update(1)

    for word in word_counts:
        score = 1 - 0.7 ** word_counts[word]
        if word not in scores or scores[word] < score:
            scores[word] = score
            paths[word] = id_to_title[word_page[word]]


def output_scores_job():
    start_time = time.time()

    print("Get all id to title")
    id_to_title = wiki_database.get_all_titles_dict()

    for term in term_utils.get_terms():
        output_scores(term, id_to_title)
    
    print("--- %s seconds ---" % (time.time() - start_time))