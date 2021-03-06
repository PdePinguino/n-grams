#!/usr/bin/env python3

"""
This files has the Ngram class.
"""
import pickle
import pandas as pd
import numpy as np
from tqdm import tqdm


class NGram():
    def __init__(self, poems, n):
        self.n = n
        self.poems = poems
        self.all_lines = self.append_tag(self.get_lines())
        self.vocab = self.get_vocab()  # stores unique words without <s> and </s>
        self.n2i = self.ngram2index()
        self.i2n = self.index2ngram()
        #self.ngram = {}  # counts of ngrams occurrences
        #self.count_ngram_in_poems()
        #self.ngram_probs = self.compute_ngram_probs()

    def get_vocab(self):
        words = []
        for line in self.all_lines:
            words.extend(line.split()[1:-1])

        return list(set(words))

    def compute_ngram_probs(self):
        wf2i, wt2i = self.words2index()
        i2wf, i2wt = self.index2words(wf2i, wt2i)

        if self.n == 1:
            df = pd.DataFrame.from_dict(self.ngram, columns=['counts'],orient='index')
            df.drop('<s>', axis='index', inplace=True)
            #df.drop('</s>', axis='index', inplace=True)
            total_counts = df.sum(axis='index')
            df = self.add_probs(df, total_counts)

            return df

        else:
            matrix = self.probs_matrix(wf2i, wt2i, i2wf, i2wt)

            return matrix

    def probs_matrix(self, wf2i, wt2i, i2wf, i2wt):
        matrix = np.zeros(shape=(len(wf2i), len(wt2i)))
        ngram_occurrences = {i2wf[index]: []}

        for index in tqdm(range(matrix.shape[0])):
            for column in range(matrix.shape[1]):
                ngram_occurrences = sum(matrix[index])
                # assigning occurrences count of this particular ngram
                ngram = '-'.join([i2wf[index], i2wt[column]])
                try:
                    matrix[index, column] = self.ngram[ngram] / ngram_occurrences
                except KeyError:
                    matrix[index, column] = 0.0  # assigning 0.0 to non-seeing ngrams

        return matrix

    def words2index(self):
        if self.n == 1:
            wf2i = {word: index for index, word in enumerate([voc for voc in self.ngram])}
            wt2i = {word: index for index, word in enumerate([voc for voc in self.ngram])}
        else:
            words = [word.rpartition('-') for word in self.ngram]
            words_from = list(set([word[0] for word in words]))
            words_to = list(set([word[2] for word in words]))

            wf2i = {word: index for index, word in enumerate(words_from)}
            wt2i = {word: index for index, word in enumerate(words_to)}

        return wf2i, wt2i

    def index2words(self, wf2i, wt2i):
        i2wf = {index: word for word, index in wf2i.items()}
        i2wt = {index: word for word, index in wt2i.items()}

        return i2wf, i2wt

    def add_probs(self, df, total_counts):
        probs = []
        for word in df.index:
            prob = df['counts'][word] / total_counts
            probs.append(prob.item())
        df['probs'] = probs

        return df

    def get_lines(self):
        lines = [line for book in self.poems
                      for file in self.poems[book]
                      for line in self.poems[book][file][1]]

        return lines

    def count_ngram_in_poems(self):
        for line in self.all_lines:
            self.count_ngram_in_line(line)

        return

    def count_ngram_in_line(self, line):
        if self.n == 1:
            self.uni_gram(line)
        else:
            self.n_gram(line)

        return

    def uni_gram(self, line):
        for word in line.split():
            try:
                self.ngram[word] += 1
            except KeyError:
                self.ngram[word] = 1

        return

    def n_gram(self, line):
        words = line.split()
        for index in range(len(words) - (self.n - 1)):
            nword = '-'.join(words[index: index + self.n])
            try:
                self.ngram[nword] += 1
            except KeyError:
                self.ngram[nword] = 1

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
    with open('poems.pkl', 'rb') as handle:
        poems = pickle.load(handle)

    #unigram = NGram(poems, n=1)
    #print(unigram.ngram)
    #print(unigram.ngram_table)

    #bigram = NGram(poems, n=2)
    #print(bigram.ngram)
    #print(bigram.ngram_probs)
    #print(bigram.ngram_probs[np.nonzero(bigram.ngram_probs)])

    trigram = NGram(poems, n=3)
    print(trigram.ngram)
    print(trigram.ngram_probs)
    print(trigram.ngram_probs[np.nonzero(trigram.ngram_probs)])
