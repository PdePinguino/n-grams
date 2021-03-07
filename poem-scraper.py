#!/usr/bin/env python3

"""
This file should be run once.

It scrapes for Pablo Neruda's poems on the web
and creates a 'data' folder with books in it.

Five folders are created within 'data' folder:
'cantogeneral'
'20pda1cd'
'100sonetos'
'losversosdelcapitan'
'residenciaenlatierra'

In each folder there is one poem in a txt file.
"""

import os
import requests
import re
from os.path import join
from bs4 import BeautifulSoup


def clean_title(title):
    title = title.lower()
    words = [word for word in title.split()]
    title = ' '.join(words)

    return title

def clean_versos(versos):
    versos = versos.split('\n')
    versos = [verso.strip() for verso in versos]

    return versos

def clean_text(text):
    text_cleaned = []
    for line in text:
        line = str(line)
        if re.match(r'<br/>', line) or re.match(r'\n', line):
            continue
        elif re.match(r'None', line):
            break
        else:
            text_cleaned.append(line.strip())

    return text_cleaned

def poems_to_txt(poems, folder):
    for poem in poems:
        file = str(poem) + '.txt'
        with open(join('data', folder, file), 'w') as file:
            for line in poems[poem]:
                file.write(f'{line}\n')

def get_page_content(link):
    page = requests.get(link)
    print(page.status_code)
    bs = BeautifulSoup(page.content, 'html.parser')

    return bs

def create_folder(folder):
    try:
        os.makedirs(join('data', folder))
    except FileExistsError:
        pass

def scrap_neruda_cantogeneral():
    folder = 'cantogeneral'
    create_folder(folder)

    # thanks to https://www.neruda.uchile.cl/
    link = "https://www.neruda.uchile.cl/obra/cantogeneral.htm"
    bs = get_page_content(link)
    #print(bs.prettify())

    links_to_poems = [a['href'] for a in bs.find_all('a', href=True) if a.text]
    # links_to_poems --> 66 links, but 63 useful
    titles = [a.getText() for a in bs.find_all('a', href=True) if a.text]
    titles = [clean_title(title) for title in titles]

    poems = {}
    parent_link = "https://www.neruda.uchile.cl/obra/"
    for link, title in zip(links_to_poems[:-3], titles[:-3]):
        print(link, title)
        page = requests.get(parent_link + link)
        bs = BeautifulSoup(page.content, 'html.parser')
        lines = bs.find_all('p')

        poems[title] = []
        for line in lines:
            text = line.getText()
            poems[title].append(text)

    poems_to_txt(poems, folder)

    return

def scrap_neruda_20poemasdeamor():
    folder = '20pda1cd'
    create_folder(folder)

    link = "http://www.rinconcastellano.com/biblio/sigloxx_27/neruda_20poe.html"
    bs = get_page_content(link)
    #print(bs.prettify())

    text = bs.find_all('p')
    lines = [line.text for line in text]
    titles = []
    versos = []
    index = 0
    while index < 42:
        titles.append(lines[index].strip())
        versos.append(clean_versos(lines[index + 1]))
        index += 2

    poems = {title:verso for title, verso in zip(titles, versos)}
    #print(len(poems))  # 21

    poems_to_txt(poems, folder)

    return

def scrap_neruda_100sonetos():
    folder = '100sonetos'
    create_folder(folder)

    link = "https://www.poemas-del-alma.com/cien-sonetos-de-amor.htm"
    bs = get_page_content(link)
    #print(bs.prettify())

    links_to_poems = [a['href'] for a in bs.find_all('a', href=True) if a.text]
    links_to_poems = [link for link in links_to_poems if re.match(r'soneto-.*', link)]
    #print(len(links_to_poems))  # 100

    sonetos = {}
    for link in links_to_poems:
        parent_link = "https://www.poemas-del-alma.com/"
        page = requests.get(parent_link + link)
        print(page.status_code, parent_link + link)
        bs = BeautifulSoup(page.content, 'html.parser')
        #print(bs.prettify())

        poem = []
        for br_tag in bs.find_all('br'):
            poem.append(br_tag.next_sibling)
        poem = clean_text(poem)
        sonetos[link[:-4]] = poem

    poems_to_txt(sonetos, folder)

    return

def scrap_neruda_losversosdelcapitan():
    folder = 'losversosdelcapitan'
    create_folder(folder)

    # thanks to https://www.neruda.uchile.cl/
    link = "http://www.neruda.uchile.cl/obra/versoscapitan.htm"
    bs = get_page_content(link)
    #print(bs.prettify())

    links_to_poems = [a['href'] for a in bs.find_all('a', href=True) if a.text]
    # links_to_poems --> 66 links, but 63 useful
    titles = [a.getText() for a in bs.find_all('a', href=True) if a.text]
    titles = [clean_title(title) for title in titles]

    poems = {}
    parent_link = "https://www.neruda.uchile.cl/obra/"
    for link, title in zip(links_to_poems[:-3], titles[:-3]):
        print(link, title)
        page = requests.get(parent_link + link)
        bs = BeautifulSoup(page.content, 'html.parser')
        lines = bs.find_all('p')

        poems[title] = []
        for line in lines:
            text = line.getText()
            poems[title].append(text)

    poems_to_txt(poems, folder)

    return

def scrap_neruda_residenciaenlatierra():
    folder = 'residenciaenlatierra'
    create_folder(folder)

    link = "https://www.literatura.us/neruda/tierra.html"
    bs = get_page_content(link)
    #print(bs.prettify())

    titles = [clean_title(b.text) for b in bs.find_all('b')]
    titles = titles[1:-2]
    print(titles)

    text = []
    for font in bs.find_all('font'):
        text.append(font.text)

    poems = {}
    for line in range(len(text)):
        if clean_title(text[line]) in titles:
            poems[clean_title(text[line])] = clean_versos(text[line + 1])

    poems_to_txt(poems, folder)

    return


if __name__ == '__main__':
    try:
        os.makedirs('data')
    except FileExistsError:
        pass

    scrap_neruda_cantogeneral()
    scrap_neruda_20poemasdeamor()
    scrap_neruda_100sonetos()
    scrap_neruda_losversosdelcapitan()
    scrap_neruda_residenciaenlatierra()
