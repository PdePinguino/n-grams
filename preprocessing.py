#!/usr/bin/env python3

"""
This file cleans the scraped poems from the web.

It requires poem-scraper.py to be run first.

It reads from the 'data' folder and outputs to a pikel file
all poems.

Output file: 'poems.pkl'
"""

from os import listdir
from os.path import isfile, isdir, join
import pickle

def read_from_books(books):
    poems = {}
    for book in books:
        poems[book] = {}
        path = join('data', book)
        files = files_in_folder(path)
        for file in files:
            poems[book][file[:-4]] = read_txt(path, file)

    return poems

def read_txt(path, file):
    title = file[:-4]
    versos = []
    with open(join(path, file), 'r') as file:
        for line in file:
            if line.split():
                versos.append(clean_line(line))

    return (title, versos)

def clean_word(word):
    chars = [char for char in word if char.isalpha()]
    word = ''.join(chars)

    return word

def clean_line(line):
    words = [word for word in line.split()]
    words = [word.lower().strip() for word in words]
    words = [clean_word(word) for word in words]
    line = ' '.join(words)

    return line

def files_in_folder(path):
    files = [file for file in listdir(path) if isfile(join(path, file))]
    return files

def dir_in_folder(folder):
    directories = [dir for dir in listdir(folder) if isdir(join(folder, dir))]
    return directories


if __name__ == '__main__':
    # it assumes that poem-scraper.py was run first
    # reading poems from data folder
    books = dir_in_folder('data')
    poems = read_from_books(books)

    # saving to pkl file
    with open('poems.pkl', 'wb') as handle:
        pickle.dump(poems, handle)
