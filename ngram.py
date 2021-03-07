#!/usr/bin/env python3

"""
This files has the NGram class.
"""

import pickle
from os.path import join
import numpy as np
import re
from tqdm import tqdm


class NGram():
    def __init__(self, poems, n, reduced=False):
        self.n = n
        self.poems = poems
        self.tagged_lines = self.append_tag(self.get_lines())
        if reduced:
            print('using reduced corpus')
            self.tagged_lines = self.tagged_lines[:10]
        self.vocab = self.get_vocab()  # stores unique words without <s> and </s>

        self.index = 0
        self.n2i = {}  # ngram to index
        self.i2n = {}  # index to ngram
        self.ngram_counts = {}  # counts of ngrams occurrences
        self.count_ngram_in_poems()  # it populates n2i, i2n, ngram_counts dictionaries

        # key is an ngram-1, value is the log of next-seen-word occurrence probability
        # example for bigram case:
        # self.ngram_probs['en'] = {'el': -0.40546510810816444, 'mi': -1.0986122886681098}
        self.ngram_probs = {}
        self.compute_probs()

    def compute_probs(self):
        if self.n == 1:
            self.compute_unigram_probs()
        else:
            self.compute_ngram_probs()

        return

    def compute_ngram_probs(self):
        print('computing ngram probs. this might take a while...')
        for ngram in tqdm(self.ngram_counts):
            words_from = ngram.rpartition('-')[0]
            pattern = re.compile(f'{words_from}-.*')
            seen_ngrams = [ngram for ngram in self.ngram_counts if re.match(pattern, ngram)]
            total_counts = sum([self.ngram_counts[ngram] for ngram in seen_ngrams])

            self.ngram_probs[words_from] = {}
            for seen_ngram in seen_ngrams:
                word_to = seen_ngram.rpartition('-')[2]
                ngram_counts = self.ngram_counts[seen_ngram]
                self.ngram_probs[words_from][word_to] = np.log(ngram_counts / total_counts)

        return

    def compute_unigram_probs(self):
        total_counts = sum([self.ngram_counts[word] for word in self.ngram_counts])
        for word in tqdm(self.ngram_counts):
            word_counts = self.ngram_counts[word]
            self.ngram_probs[word] = np.log(word_counts / total_counts)

        return

    def get_vocab(self):
        words = []
        for line in self.tagged_lines:
            words.extend(line.split()[1:-1])

        return list(set(words))

    def get_lines(self):
        lines = [line for book in self.poems
                      for file in self.poems[book]
                      for line in self.poems[book][file][1]]

        return lines

    def count_ngram_in_poems(self):
        for line in self.tagged_lines:
            self.count_ngram_in_line(line)

        return

    def count_ngram_in_line(self, line):
        if self.n == 1:
            self.count_unigram(line)
        else:
            self.count_ngram(line)

        return

    def count_unigram(self, line):
        for unigram in line.split()[1:]:  # skipping first token <s>
            try:
                self.ngram_counts[unigram] += 1
            except KeyError:
                self.ngram_counts[unigram] = 1
                self.n2i[unigram] = self.index
                self.i2n[self.index] = unigram
                self.index += 1

        return

    def count_ngram(self, line):
        words = line.split()
        for index in range(len(words) - (self.n - 1)):
            ngram = '-'.join(words[index: index + self.n])
            try:
                self.ngram_counts[ngram] += 1
            except KeyError:
                self.ngram_counts[ngram] = 1
                self.n2i[ngram] = self.index
                self.i2n[self.index] = ngram
                self.index += 1

        return

    def append_tag(self, lines):
        lines_tag = []
        for line in lines:
            line = line.split()
            line.insert(0, '<s>')
            line.append('</s>')
            line = ' '.join(line)
            lines_tag.append(line)

        return lines_tag


if __name__ == '__main__':
    with open(join('corpus', 'poems.pkl'), 'rb') as handle:
        poems = pickle.load(handle)

    unigram = NGram(poems, n=1)
    #bigram = NGram(poems, n=2)
    #trigram = NGram(poems, n=3)
    #fourthgram = NGram(poems, n=4)

    # save to pkl file
    with open('unigram.pkl', 'wb') as handle:
        pickle.dump(unigram, handle)
