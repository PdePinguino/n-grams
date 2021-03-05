#!/usr/bin/env python3

"""
This files has the Ngram class.
"""
import pickle
import pandas as pd
import numpy as np


class NGram():
    def __init__(self, poems, n):
        self.n = n
        self.poems = poems
        self.all_lines = self.append_tag(self.get_lines())
        self.vocab = []  # stores unique ngrams
        self.ngram = {}  # counts of ngrams occurrences
        self.count_ngram_in_poems()
        self.vocab = set(self.vocab)
        self.ngram_probs = self.compute_ngram_probs()

    def compute_ngram_probs2(self):
        if self.n == 1:
            df = pd.DataFrame.from_dict(self.ngram, columns=['counts'],orient='index')
            df.drop('<s>', axis='index', inplace=True)
            #df.drop('</s>', axis='index', inplace=True)
            total_counts = df.sum(axis='index')
            self.add_probs(df, total_counts)

        else:
            w2i = self.words2index()
            data = self.counts2df(w2i)
            df = pd.DataFrame(data=data, columns=w2i, index=w2i)
            # to access a specific cell --> df.loc['word_from','word_to']

            df.drop('<s>', axis='columns', inplace=True)
            #df.drop('</s>', axis='index', inplace=True)
            self.counts2probs(df, w2i)

    def compute_ngram_probs(self):
        if self.n == 1:
            df = pd.DataFrame.from_dict(self.ngram, columns=['counts'],orient='index')
            df.drop('<s>', axis='index', inplace=True)
            #df.drop('</s>', axis='index', inplace=True)
            total_counts = df.sum(axis='index')
            df = self.add_probs(df, total_counts)

            return df

        else:
            w2i = self.words2index()
            i2w = self.index2words()
            count_matrix = self.count_matrix(w2i)
            probs_matrix = self.counts2probs(count_matrix, w2i, i2w)

            return probs_matrix

    def counts2probs2(self, df, w2i):
        for word_from in w2i:
            try:
                word_from_occurrences = sum(df[word_from])
                for word_to in w2i:
                    ngram_ocurrences = df[word_from][word_to]
                    #print(df[w2i[word_from]],w2i[[word_to]])
                    df.loc[word_from, word_to] = ngram_ocurrences / word_from_occurrences
                    #print(df[w2i[word_from]],w2i[[word_to]])
            except KeyError:  # KeyError: '<s>' --> it has been dropped
                pass
        print(df)

    def counts2probs(self, matrix, w2i, i2w):
        indexes, columns = matrix.shape
        for word_from in range(indexes):
            word_from_occurrences = sum(matrix[word_from])
            for word_to in range(columns):
                ngram_ocurrences = matrix[word_from][word_to]
                try:
                    matrix[word_from, word_to] = ngram_ocurrences / word_from_occurrences
                except RuntimeWarning:  # division by 0 --> </s> does not go to any other word
                    pass

        return matrix

    def counts2df(self, w2i):
        matrix = np.zeros(shape=(len(w2i), len(w2i)))

        for word, count in self.ngram.items():
            word_from, word_to = word.split('-')
            matrix[w2i[word_from], w2i[word_to]] = count

        return matrix

    def count_matrix(self, w2i):
        matrix = np.zeros(shape=(len(w2i), len(w2i)))

        for word, count in self.ngram.items():
            word_from, word_to = word.split('-')
            matrix[w2i[word_from], w2i[word_to]] = count

        return matrix

    def words2index(self):
        w2i = {word: index for index, word in enumerate(self.vocab)}

        return w2i

    def index2words(self):
        i2w = {index: word for index, word in enumerate(self.vocab)}

        return i2w

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
            self.vocab.append(word)
            try:
                self.ngram[word] += 1
            except KeyError:
                self.ngram[word] = 1

        return

    def n_gram(self, line):
        words = line.split()
        self.vocab.extend(words)
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

    bigram = NGram(poems, n=2)
    #print(bigram.ngram)
    print(bigram.ngram_probs)
    print(bigram.ngram_probs[np.nonzero(bigram.ngram_probs)])

    #trigram = NGram(poems, n=3)
    #print(trigram.ngram)
