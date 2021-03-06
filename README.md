# Pablo -el bot- Neruda: an N-Gram Language Model
¿Cómo escribiría los nuevos poemas Pablo -el Bot- Neruda?

## Cómo usar este repositorio?
Run in the terminal the following commands:
```
git clone https://github.com/PdePinguino/n-grams.git
cd n-grams
./pablo-elbot-neruda.py n=2 lines=10
```
and a poem will be printed on the console using a bigram language model.

Parameters:  
`n`: it specifies the language model (unigram, bigram, trigram...)  
`lines`: it specifies the amount of lines to be generated.

## Cómo funciona Pablo -el bot- Neruda?

Pablo -el bot- Neruda usa un modelo del lenguaje estadístico (ngram) para generar poemas. Puedes especificar el valor de N (1, 2, 3...) que afectarán tanto las probabilidades del modelo del lenguaje como el resultado final.

Las probabilidades del modelo han sido calculadas utilizando como corpus 5 poemarios de Pablo Neruda (extraídos de la web). Para facilitar el uso del modelo (y porque demora algún tiempo realizar el cálculo) el repositorio incluye las probabilidades previamente calculadas. Puedes, de todas maneras, agregar o modificar el corpus y volver a calcular las probabilidades ngrams (ver apartado "Usar otro corpus").

Estas probabilidades son calculadas por la clase `NGram` contenida en el archivo `ngram.py`.

La clase `EscritorNGram` utiliza las probabilidades del modelo del lenguaje para generar un poema.

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

La fórmula general del cálculo es:

probabilidad = ocurrencias ngrams / total ocurrencias (ngrams - 1)

## Implementación
Existen distintas maneras de implementar este modelo y varían en cómo solucionan ciertos problemas centrales. Dijimos que los cálculos de probabilidades utilizan un corpus, y todo corpus es un conjunto finito de palabras, por lo que eventualmente el modelo intentará predecir la probabilidad de ocurrencia de una secuencia que no ha visto previamente y, por tanto, no ha calculado su probabilidad de ocurrencia.

En este caso, hemos de

## Usar otro corpus

## Credits

