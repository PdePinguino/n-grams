"""
This file should be run once.

It cleans previously downloaded books in txt format.

Five folders are created within 'data' folder:
	'2000'
	'elegia'
	'odas elementales'
	'el libro de las preguntas'
	'confieso que he vivido'
	'geografia infructuosa'
	'paranacer he nacido'
	'tercera residencia'
	'crepusculario'
	'nuevas odas elementales'
	'plenos poderes'

In each folder there is one poem in a txt file.
"""
import os
import re
import poem_scraper as ps
from os.path import join
from os.path import isfile


def clean_2000(text):
	poems_titles = re.findall(r'\n{5}(.*)\n{6}', text)

	poems_text = re.split(rf'{"|".join(poems_titles)}', text)
	poems_text = [re.sub(r'\n+', '\n', p).strip().split('\n')
					for p in poems_text if p.split()]
	if len(poems_titles) == len(set(poems_titles)):
		poems = {k:v for k,v in zip(poems_titles, poems_text)}

	else:
		for t in range(len(poems_titles)):
			if poems_titles.count(t) > 1:
				poems_titles[t] = t+'(1)'
		poems = {k:v for k,v in zip(poems_titles, poems_text)}

	return poems

def clean_confiesoqhv(text):
	text = [line for line in text.split('\n') if line]
	text = [line for line in text
			if not (re.search(r'Colaboración de Serg io Barros', line)
			or re.search(r'Preparado por Patricio Barros', line)
			or re.search(r'www.IibrosmaraviIIosos.com', line)
			or re.search(r'^Confieso que he vivido$', line)
			or re.search(r'^\d$', line))]

	caps = {}
	for i in range(len(text)):
		result = re.match(r'(Capítulo \d+)', text[i])
		if result:
			title = '-'.join([result.group(1), text[i+1]])
			caps[title] = []
		else:
			caps[title].append(text[i])

	for k in caps:
		caps[k] = [' '.join(caps[k])]

	return caps

def clean_crepusculario(text):
	text = [line for line in text.split('\n') if line]
	poems = {}

	for line in text:
		if line.isupper() and line != "PELLEAS." and line != "MELISANDA.":
			title = line
			poems[title] = []
		else:
			poems[title].append(line)

	return poems

def clean_elegia(text):
	text = [line for line in text.split('\n') if line]
	titles = '|'.join('I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX XXI XXII XXIII XXIV XXV XXVI XXVII XXVIII XXIX XXX'.split())
	poems = {}

	for line in text:
		if re.fullmatch(rf'{titles}', line):
			title = line
			poems[title] = []
		else:
			poems[title].append(line)

	return poems

def clean_odas(text):
	text = [line for line in text.split('\n') if line]
	poems = {}
	for line in text:
		if re.match(r'El hombre invisible|Oda a.*', line):
			title = line
			poems[title] = []
		else:
			poems[title].append(line)

	return poems

def clean_nuevasodas(text):
	text = [line for line in text.split('\n') if line]
	poems = {}
	for line in text:
		if re.match(r'La casa de las odas|Oda a.*', line):
			title = line
			poems[title] = []
		else:
			poems[title].append(line)

	return poems

def clean_geografiai(text):
	poems = {}
	poems_titles = re.findall(r'\n{6}(.*)[^\\n]', text)
	text = [line for line in text.split('\n') if line]
	poems = {}

	for line in text:
		if re.match(rf'{"|".join(poems_titles)}', line):
			title = line
			poems[title] = []
		else:
			poems[title].append(line)

	return poems

def clean_paranacerhn(text):
	text = [line for line in text.split('\n') if line]
	poems = {}
	for line in text:
		if re.match(r'DULCE PATRIA, RECIBE LOS VOTOS|CON QUE CHILE EN TUS ARAS JURÓ|QUE O LA TUMBA SERÁ DE LOS LIBRES|O EL ASILO CONTRA LA OPRESIÓN.', line):
			continue
		if line.isupper():
			title = line
			poems[title] = []
		else:
			poems[title].append(line)

	return poems

def clean_plenospoderes(text):
	text = [line for line in text.split('\n') if line]
	poems = {}
	for line in text:
		if line.isupper():
			title = line
			poems[title] = []
		else:
			poems[title].append(line)

	return poems

def clean_preguntas(text):
	text = [line for line in text.split('\n') if line]
	titles = '|'.join('I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX XXI XXII XXIII XXIV XXV XXVI XXVII XXVIII XXIX XXX XXXI XXXII XXXIII XXXIV XXXV XXXVI XXXVII XXXVIII XXXIX XL XLI XLII XLIII XLIV XLV XLVI XLVII XLVIII XLIX L LI LII LIII LIV LV LVI LVII LVIII LVIX LX LXI LXII LXIII LXIV LXV LXVI LXVII LXVIII LXIX LXX LXXI LXXII LXXIII LXXIV'.split())
	poems = {}

	for line in text:
		if re.fullmatch(rf'{titles}', line):
			title = line
			poems[title] = []
		else:
			poems[title].append(line)

	return poems

def clean_tercerar(text):
	text = [line for line in text.split('\n') if line]
	poems = {}
	for line in text:
		if re.match(r'^PARTE.*', line):
			continue
		elif line.isupper() and not re.match(r'\(SONATA\)', line):
			title = line
			poems[title] = []
		else:
			try:
				poems[title].append(line)
			except UnboundLocalError:
				pass

	return poems

def read_book(title, clean_func):
	print('title', title)
	with open(join(PATH_TO_BOOKS, title+'.txt'), 'r') as file:
		text = file.read()

	poems = clean_func(text)

	return poems

def read_clean_save(title, clean_func):
	ps.create_folder(title)
	poems = read_book(title, clean_func)
	ps.poems_to_txt(poems, title)


def main():
	books = {'2000': clean_2000,
			'elegia': clean_elegia,
			'odas': clean_odas,
			'preguntas': clean_preguntas,
			'confiesoqhv': clean_confiesoqhv,
			'geografiai': clean_geografiai,
			'paranacerhn': clean_paranacerhn,
			'tercerar': clean_tercerar,
			'crepusculario': clean_crepusculario,
			'nuevasodas': clean_nuevasodas,
			'plenospoderes': clean_plenospoderes,
			}

	for title, clean_func in books.items():
		read_clean_save(title, clean_func)


if __name__ == '__main__':
	try:
		os.makedirs('data')
	except FileExistsError:
		pass
	PATH_TO_BOOKS = 'downloaded_books'
	main()
