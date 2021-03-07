# NGram Pablo Neruda: an N-Gram Language Model
¿Cómo escribiría los nuevos poemas NGram Pablo Neruda?

## Cómo usar este repositorio?
Run in the terminal the following commands:
```
git clone https://github.com/PdePinguino/n-grams.git
cd n-grams
./ngram_pablo_neruda.py -n bigram
```
and a poem will be printed on the console using a bigram language model.

Parameters:  
`-n`, `ngram`: it specifies the language model (ngrams available: unigram, bigram, trigram, fourthgram)  
`-l`, `max_words_per_line`: it overwrites the default value of `max_words_per_line`  
`-p`, `lines_per_poem`: it overwrites the default value of `lines_per_poem`  
`-t`, `words_per_title`: it overwrites the default value of `words_per_title`  

`ngram_pablo_neruda.py` instantiates a PabloNeruda class that uses the ngram probabilities previously saved in a pikle file by the `NGram` class.

PabloNeruda Class Parameters:  
`max_words_per_line`: int  
`lines_per_poem`: int  
`words_per_title`: int  
(see more details in .py)  

## Cómo funciona NGram Pablo Neruda?

NGram Pablo Neruda usa un modelo del lenguaje estadístico (ngram) para generar poemas. Puedes especificar el valor de N (unigram, bigram, trigram...) que afectarán tanto las probabilidades del modelo del lenguaje como el resultado final. Asimismo puedes especificar cuántas palabras máximo por verso, cuántos versos en el poema y de cuántas palabras el título.

Las probabilidades del modelo han sido calculadas utilizando como corpus 5 poemarios de Pablo Neruda (ver apartado "Créditos"). Para facilitar el uso del modelo (y porque demora algún tiempo realizar el cálculo) el repositorio incluye las probabilidades previamente calculadas. Puedes, de todas maneras, agregar o modificar el corpus y volver a calcular las probabilidades ngrams (ver apartado "Usar otro corpus").

Estas probabilidades son calculadas por la clase `NGram` contenida en el archivo `ngram.py`.

La clase `PabloNeruda` utiliza las probabilidades del modelo del lenguaje para generar un poema. En esta implementación, solo se generan ngrams que han sido vistos.

## Qué son N-grams?

N-grams son secuencias de N palabras.  

Cuando N = 1 (uni-gram), tenemos secuencias de 1 palabra:  
`la`, `casa`, `es`, `de`, `color`, `rojo`  
Cuando N = 2 (bi-gram), la secuencia es de 2 palabras:
`la casa`, `casa es`, `es de`, `de color`, `color rojo`  
Y si N = 3 (tri-gram), entonces `la casa es`, `casa es de`, `es de color`, `de color rojo`

Los n-grams son utilizados para generar un Modelo del Lenguaje que sea capaz de asignar probabilidades de ocurrencia a una secuencia de palabras.  

¿Qué quiere decir eso?  

Que el modelo es capaz de predecir qué secuencia es más probable de ocurrir. Por ejemplo, `la casa es de colores` o `la es colores casa de`.

¿Cómo puede saberlo?

Para saberlo, necesitamos un corpus para contar la ocurrencia de ngrams y estadísticamente predecir la probabilidad de que cierta secuencia ocurra o no ocurra.

## Cálculo de probabilidades
Existen distintas maneras de implementar este modelo y varían en cómo solucionan ciertos problemas centrales (por ejemplo, asignar probabilidades o emitir ngrams que no están contenidos en el corpus). En este caso, la clase es solo capaz de emitir ngrams que están contenidos en el corpus.

Imaginemos un corpus de 3 versos y un modelo en el que n = 2 (bigram):  
```
<s> puedo escribir los versos </s>  
<s> los versos tristes </s>  
<s> los de esta noche </s>  
```
Los símbolos \<s\> y \<\/s\> significan inicio de oración y término de oración, respectivamente.  

Para calcular la probabilidad de que ocurra la secuencia `los de`, entonces debemos contar cuántas veces ocurre esta secuencia dividida por todas las secuencias que comiencen con `los`, es decir:

probabilidad('de'|'los') = frecuencia('de'|'los') / frecuencia('x'|'los')

en donde 'x' es reemplazada por todas las palabras que efectivamente ocurren en el corpus. En este caso, `los versos` ocurre 2 veces.

probabilidad('de'|'los') = 1 / 3

En otras palabras, cuando mi modelo vea la palabra `los`, entonces determinará hay 0.333 de probabilidades de que la siguiente palabra sea `de` y 0.666 de probabilidades de que la siguiente palabra sea `versos`.

## Poemas de NGram Pablo Neruda
**(unigram)**

"y mi esperemos"

infancia mismos guitarra  
me escucha mi  
lunares meteoros bienamada  
esperemos y solamente  

**(bigram)**

"tu detenidas murciélagos"

soldaditos  
príncipes rodean oyes  
papel escrito  
detenidas y esas  
ligera  
intención nupcial edad  
murciélagos una mano  
trajiste del brazo  
encadenado sobre tu  

**(trigram)**

"amargas la literatura tan lejos"

dormida y desnuda fuego y a cielo  
calles amargas derrotadas  
la literatura  
traída de tan lejos la lluvia de  
de frutos agudos  
pero por sobre todo hay un planeta  


## Usar otro corpus
Para calcular nuevamente las probabilidades, debes utilizar la clase NGram. Esta recoge el corpus contenido en el archivo `poems.pkl` de la carpeta `pkls`. El archivo está en formato de diccionario[libro-1][poema-1] = [list of verses]  

Para utilizar otro corpus, debes generar otro archivo .pkl y pasarlo por la NGram class que generará nuevas probabilidades.

## Credits
Libros de Pablo Neruda extraídos de:  
"Canto general" https://www.neruda.uchile.cl/obra/cantogeneral.htm  
"20 poemas de amor y una canción desesperada" http://www.rinconcastellano.com/biblio/sigloxx_27/neruda_20poe.html  
"100 sonetos" https://www.poemas-del-alma.com/cien-sonetos-de-amor.htm  
"Los versos del capitán" http://www.neruda.uchile.cl/obra/versoscapitan.htm  
"Residencia en la tierra" https://www.literatura.us/neruda/tierra.html
