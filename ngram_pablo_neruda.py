#!/usr/bin/env python3

"""
This file has the PabloNeruda class.
"""

import re
import pickle
import json
import argparse
import numpy as np
from os.path import join
from ngram import NGram


class PabloNeruda():
    def __init__(self, ngram, vocab, probs):
        self.n = ngram
        self.vocab = vocab
        self.ngram_probs = probs

        self.max_words_per_line = np.random.randint(1, 5) + self.n
        self.lines_per_poem = np.random.randint(1, 10)
        self.words_per_title = np.random.randint(1, 3) + self.n

    def kick_off(self):
        # randomly chooses the first ngram of the line
        first_word = '<s>'
        while first_word == '<s>':
            first_ngram = np.random.choice(list(self.ngram_probs.keys()))
            first_word = first_ngram.split('-')[0]

        return first_ngram.split('-')

    def next_word(self, previous_ngram):
        if self.n == 1:
            words = list(self.ngram_probs.keys())
            probs = list(self.ngram_probs.values())
        else:
            words = list(self.ngram_probs[previous_ngram].keys())
            probs = list(self.ngram_probs[previous_ngram].values())

        chosen_word = np.random.choice(a=words, p=np.exp(probs))

        return chosen_word

    def write_line(self):
        number_of_words = self.max_words_per_line
        line = []
        line.extend(self.kick_off())
        added = 1

        while added < number_of_words:
            previous_ngram = '-'.join(line[-(self.n - 1):])
            next_word = self.next_word(previous_ngram)
            if next_word == '</s>':
                return ' '.join(line)
            else:
                line.append(next_word)
                added += 1

        return ' '.join(line)

    def write_poem(self):
        number_of_lines = self.lines_per_poem
        added = 0
        poem = []

        while added < number_of_lines:
            poem.append(self.write_line())
            added += 1

        return poem

    def write_title(self, poem):
        number_of_words = self.words_per_title
        words = [word for line in poem for word in line.split()]

        try:
            title = np.random.choice(a=words, size=number_of_words, replace=False)
        except ValueError:
            # larger amount of samples than population
            title = np.random.choice(a=words, size=number_of_words, replace=True)

        return ' '.join(title)

def generate_from_pkl(ngram, mwpl, lpp, wpt):
    with open(join('ngrams_probs', args.ngram + '.pkl'), 'rb') as handle:
        ngram = pickle.load(handle)

    pablo_neruda = PabloNeruda(ngram)
    pablo_neruda.max_words_per_line = mwpl
    pablo_neruda.lines_per_poem = lpp
    pablo_neruda.words_per_title = wpt

    poem = pablo_neruda.write_poem()
    title = pablo_neruda.write_title(poem)

    print('\n\t', title, '\n')
    for line in poem:
        print('\t', line)
    print()

    return (title, poem)

def generate_from_json(ngram, mwpl, lpp, wpt):
    with open(join('ngrams_probs', args.ngram + '.json')) as jfile:
        jobject = json.load(jfile)
        jfile.close()

    pablo_neruda = PabloNeruda(jobject['NGRAM'], jobject['VOCAB'], jobject['PROBS'])
    pablo_neruda.max_words_per_line = mwpl
    pablo_neruda.lines_per_poem = lpp
    pablo_neruda.words_per_title = wpt

    poem = pablo_neruda.write_poem()
    title = pablo_neruda.write_title(poem)

    print('\n\t', title, '\n')
    for line in poem:
        print('\t', line)
    print()

    return (title, poem)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('-n', '--ngram', action='store', type=str, default=False)
    parser.add_argument('-l', '--max_words_per_line', action='store', type=int, default=False)
    parser.add_argument('-p', '--lines_per_poem', action='store', type=int, default=False)
    parser.add_argument('-t', '--words_per_title', action='store', type=int, default=False)
    args = parser.parse_args()

    title, poem = generate_from_json(args.ngram, args.max_words_per_line, args.lines_per_poem, args.words_per_title)
