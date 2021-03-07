#!/usr/bin/env python3

"""
This files has the Generator class.
"""

import pickle
import numpy as np
import re
from tqdm import tqdm
import sys
from ngram import NGram

class NGramGenerator():
    def __init__(self, ngram):
        self.n = ngram.n
        self.vocab = ngram.vocab
        self.ngram_probs = ngram.ngram_probs

    def kick_off(self):
        return np.random.choice(list(self.ngram_probs.keys()))

    def next_word(self, previous_gram):
        words = self.ngram_probs[previous_gram]
        print(words)
        probs = [self.ngram_probs[word] for word in words]

        chosen_word = np.random.choice(a=words, p=probs)
        print(chosen_word)
        return chosen_word

    def write_line(self):
        added = 0
        number_of_words = np.random.randint(1, 10)
        print(number_of_words)

        line = []
        line.append(self.kick_off())
        while added < number_of_words:
            line.append(self.next_word(line[-1]))

        return ' '.join(line)

if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as handle:
        ngram = pickle.load(handle)

    generator = NGramGenerator(ngram)
    print(generator.write_line())
