import numpy as np
import matplotlib.pyplot as plt

from page_extraction import page_extracts_setup

def link_scores_histogram():
    page_scores, _ = page_extracts_setup.get_term_links()
    #page_scores = { 'a': 1, 'b': 0.5, 'c': 1, 'd': 2 }
    a = np.array(list(map(lambda item:item[1], page_scores.items())))
    bins = np.arange(0, 10, 0.5)
    plt.hist(a, bins=bins)
    plt.show()