
<p align="left">
<b>University of Buenos Aires (UBA)</br>Master in Data Mining and Knowledge Discovery</b>
</p>

# Sistemas de recomendación


Implementación de un sistema de recomendación end-to-end. Desde el scrapping de datos hasta la implementación de una aplicación y los algoritmos necesarios.

## Requisitos

* [anaconda](https://www.anaconda.com/products/individual) / [miniconda](https://docs.conda.io/en/latest/miniconda.html) / [mamba (Recomendado)](https://github.com/mamba-org/mamba)
* mariadb/mysql

## WIKI

Para mas detalle ver la [WIKI](https://github.com/magistery-tps/rec-sys/wiki) del proyecto.



## Primeros Pasos y explicación basica de modelos

<p align="center">
    <a href="http://www.youtube.com/watch?v=zh78fp9g3BI" target="_tab"/>
    <img src="http://img.youtube.com/vi/zh78fp9g3BI/0.jpg" 
        title="RecSys: Primeros Pasos" 
        alt="RecSys: Primeros Pasos"/>
    </a>
</p>






## Probar RecSys

Ir a  [recsys](http://recsys.ddns.net:8000/)

## Screenshots

### Recomendaciones
![See Recommendations](https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot.png)

**Notas**
* 1,2 y 3 con resultados de 3 distintos recomendadores. Es posible configurar ditintos recomendadores y ensambles de los mismo.
* Al hacer click sobre un ítem, se puede visualizar el detalle del mismo junto con sus items similares.
* Los distintos carruseles o swimlanes de recomendaciones representan a distintos recomendadores.
* Inicialmente se pueden ver los recomendadores por defecto:
   * Top populars.
   * New Populars: Populares no vistos por el usuario.
* Dependiendo de los recomendadores o ensambles de recomendadores que se configuren, es necesario cumplir con un número mínimo de calificaciones para comenzar a visualizar sus recomendaciones. Por ejemplo, para recomendadores basados en filtros colaborativos, se requiere que el usuario califique 20 ítems como mínimo. Los ensambles de recomendadores combinan recomendadores basados en filtros colaborativos con recomendadores por popularidad o basados en contenido. Los ensambles pueden no tener un requisito mínimo de calificaciones, depende de la configuración.


### Item Detail & Similars

<p align="center">
  <img src="https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot_2.png"  height="550" />
</p>

**Notas**
1. Cada item tiene una lista de tags. En este caso los tags son generos pero se peude utilizar cualquier dato.
2. Los item similares dependen del recomendador seleccionado en la vista de recommendaciones.Al hacer click sobre los simialres se abre su detalle junto con sus simialres.
3. Ademas de las estadisticas asociadas a cada item es posible ver las similitud coseno de cada item similar al item detallado. Los items similares estan ordenados por similitud coseno decreciente.
4. Son las estadisticas el item detallado: Su nivel de popularidad normalizado, la media de su rating y la cantidad de usaurios que lo calificaron.

### Scoring

En la pantalla de scoring o calificaciones. se pretenta una lsiat de item a calificar.

<p align="center">
  <img src="https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot_3.png"  height="800" />
</p>

**Notas**
1. Selecionar la calificación o rating para el item actual.
2. Por defecto la calificacion es cero.
3. El valor de estadisticas como popularidad, rating y cantidad de votaciones del item actual.
4. Presione **Vote** para aplicar el score selecionado en el punto 1 al item actual.
5. Presione **Next** para saltear la votation del item actuar.
6. Ensemble: Especifica cual es el nombre del recomendador principal (El cuales un ensamble de otros recomendadores).
7. Step: Espeficica cual es el recomendador oncluido en el ensamble que se utilizop para pgenerar la recomendacion actual.
8. [Discount Cumulative Gain](https://en.wikipedia.org/wiki/Discounted_cumulative_gain)
  * Es la metrica utilizada para valorar la calidad acumulada de las recomendaciones a partir de la primera calificación realizada por el usuario.
  * Es un metrica a nivel usuario.
9. Al hacer click sobre la imagen, es posible ver el detalle del item.



### Remove ratings

Es posible borrar todos los items del usaurio para volver a realiazr el proceso de calificacion desde cero.

<p align="center">
  <img src="https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot_5.png"  height="120" />
</p>

<p align="center">
  <img src="https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot_6.png"  height="120" />
</p>


### Manage Item

Existe un CRUD de items que permite modificarlo mismos. Tambien es posible filtar los items por tags. Esto ultimo es muy util para encontar listas curadas de items.

<p align="center">
  <img src="https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot_4.png"  height="550" />
</p>

**Notas**

1. El filtro soporta pasar una lista de tags separados por comas. Ademas, se puede buscar items quw no contenga un tag con el operador se negación (**-**).
2. Ver la vista de detalle de un item.
3. Navegar una lista de items resulado de una buqeuda o



### Metrics

Es posible visualizar metricas tanto a nivel usuario en sesion(Logueado) como todos los usuarios. La metricas Principal es Normalized Discount Cumulative Gain(NDGC). En ambas secciones se puede visualizar:

* Timeline: Linea de tiempo de NDGC calculado en cada paso de votación. (Cada paso de votacion evalua una lsita de recomendaciones).
* Histograma y boxplot de NDGC.
* A nivel usuario se puede visualizar los usuarios mar cercanos, junto con su nivel de similitud con el usuario actual. Nota: El usuario actual tiene similitud 1 con sigo mismo.


<p align="center">
  <img src="https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot_7.png"  height="1400" />
</p>

**Notas**
1. Sección de metricas para el usuario en sesión(Logueado).
2. Sección de metricas generales.


