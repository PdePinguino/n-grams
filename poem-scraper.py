#!/usr/bin/env python3

import requests
import re
from os.path import join
from bs4 import BeautifulSoup


def clean_title(title):
    title = title.lower()
    words = [word for word in title.split()]
    title = ' '.join(words)

    return title

# thanks to https://www.neruda.uchile.cl/
link = "https://www.neruda.uchile.cl/obra/cantogeneral.htm"
page = requests.get(link)
print(page.status_code)
bs = BeautifulSoup(page.content, 'html.parser')
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

for poem in poems:
    file = str(poem) + '.txt'
    with open(join('data/cantogeneral', file), 'w') as file:
        for line in poems[poem]:
            file.write(f'{line}\n')
