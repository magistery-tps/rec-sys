# UBA - Maestría en Explotación de Datos y Descubrimiento de Conocimiento - Sistemas de recomendación


Implementación de un sistema de recomendación punta a punta. Desde el scrapping de datos hasta la implementación de una aplicación y los algoritmos necesarios.

## Requisitos

* [anaconda](https://www.anaconda.com/products/individual) / [miniconda](https://docs.conda.io/en/latest/miniconda.html) / [mamba (Recomendado)](https://github.com/mamba-org/mamba)
* [Setup de entorno (Window)](https://www.youtube.com/watch?v=O8YXuHNdIIk)
* mariadb/mysql




## Diagramas de despliegue

<img src="https://raw.githubusercontent.com/magistery-tps/rec-sys/main/diagrams/deployment.svg">

Como se puede apreciar, la aplicación esta compuesta por dos grandes partes. [RecSys](http://recsys.sytes.net) expone un interfaz web para los usuarios finales. Estos puedean realizar y consultar recomemdaciones de items. Por otro lado, [RecSys](http://recsys.sytes.net) exponen una intarface REST. Esta permite a servicios externos consultar y modificar el modelo de datos de [RecSys](http://recsys.sytes.net). tambien existent procesos o Jobs que corren en una instancia de [Airflow](https://airflow.apache.org/). Estos Jobs se encargan de consultar las interacciones de los usuarios a [RecSys](http://recsys.sytes.net) y transformarlas en matrices de similitud user-user/item-item. Finamente actualizan estas similitudes en [RecSys](http://recsys.sytes.net), para poder realizar recomendaciones al usuario final.



## Componentes

* [RecSys](http://recsys.sytes.net)
  * Expone una intefaz web para de recomendación de items
    * Permite recomendar items personalizados al usuario final.
    * Login with google.
    * Pantalla para puntuación de items.
    * Pantalla de visialización de recommendaciones.
    * CRUD de items.
    * Admin site.
  * Expone una API REST para administar los distintos recommendadores y sus matrices de similitud asociadas.
* `SurpriseSimilatiyMatrixJob`
  * _svd_similarity_matrix_job_
  * _nmf_similarity_matrix_job_
* [amazon-spider-scrapper](https://github.com/adrianmarino/amazon-spider-scrapper)
    * Es un fork del proyecto amazon-scrapper.
    * Dada una búsqueda en Amazon, permite realizar scrapping del detalle de todos los resultados (Productos) y sus variaciones, junto con sus reviews.
    * Utiliza headers fake, proxies random y delays variables para minimizar el banning de Amazon.
    * Permite, reanudar el proceso de scrapping desde el ultimo productos scrappeado.


## Screenshots


### Recomendaciones
![See Recommendations](https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot.png)

**Notas**
* Al hacer click sobre un item, se puede visualizar el detalle del mismo junto con sus items similares.

### Item Detail & Similars

<p align="center">
  <img src="https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot_3.png"  height="550" />
</p>

**Notas**
* Al hacer click sobre los simialres se abre su detalle junto con sus simialres.
* Los item similares dependen del recomendador seleccionado en la vista de recommendaciones.
* Ademas de las estadisticas asociadas a cada item es posible ver las similitud coseno de cada item similar al item detallado.
* Los items similares estan ordenados por similitud coseno decreciente.

### Scoring

<p align="center">
  <img src="https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot_2.png"  height="295" />
</p>

**Notas**
1. Selecionar scoring o rating para el item actual.
2. Presione **Vote** para aplicar el score selecionado en el punto 1 al item actual.
3. Presione **Next** para saltear la votation del item actuar.
4. El valor de estadisticas como popularidad, rating y cantidad de votaciones del item actual.
5. Al hacer click sobre la imagen, es posible ver el detalle del item.

## Notebooks

**[Amazon Books](https://nijianmo.github.io/amazon/index.html)**: Dataset de libros extraído de Amazon US.


 <p align="center">
   <img src="https://github.com/magistery-tps/rec-sys/blob/main/images/amazon-books-dataset.png"  height="350" >
 </p>
 
  * **Raw pre-processing**
    * Se realizo un pre-procesamiento inicial en [MongoDB](https://www.mongodb.com/home) dada la cantidad masiva de datos.
      * [Queries](https://github.com/magistery-tps/rec-sys/blob/main/database/amazon-books.js)
      * [Commands](https://github.com/magistery-tps/rec-sys/blob/main/database/commands.sh)
  * **[build-datasets](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon-books/build-datasets.ipynb)**
    * Pre-procesamiento.
    * Selección de features.
    * Construcción de un datasets de items e interacciones de usuarios.
  * **[data-loading](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon-books/data-loader.ipynb)**
    *  Preprosesamiento final.
    *  Filtro de item e interaciones según un mínimo de popularidad.
    *  Carga de datos via SQL en la base de datos de [RecSys](http://recsys.sytes.net).
  * **[similarity-matrix-jobs](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon-books/distance-matrix-job.ipynb)**
    * Testing de jobs:
      * _svd_distance_matrix_job_
      * _nmf_distance_matrix_job_
    * Ambos jobs son instancias de _SurpriseSimilarityMatrixJob_.
    * _SurpriseSimilarityMatrixJob_ consulta las interacciones via REST a [RecSys](http://recsys.sytes.net).
    * Predice los ratings de las interacciones faltantes.
    * Cosntruye una matrix de ratings completa. Es decir, esta contien las interacciones actuales y las predichas.
    * Calcula las similitudes user-user/item-item, solo para un numero N de usuarios e items vecinos. Esto disminuir los tiempo de ejecución y evita tener en tienta usuario e item muy lejanos.
    * Finalmente, crear o actualiza via REST (En [RecSys](http://recsys.sytes.net)) las entidades _Recommender_ para cada modelos SVD y NMF, junto con sus propias matrices de similitud (_SimilarityMatrix_, entidades asociada a _Recommender_).
    * Las entidades _SimilarityMatrix_ son versionadas cada vez que correr cada job. Al correr un job, se crea una nueva versión de las matrices. Al finalizar el proceso, se borra la versión anterior quendado disponibilizada la nueva versión. Es posible mantener una ventana de versiones, pero por el momento no es necesario.
    * Los jobs solo se ejecutan cuando se encuentran nuevas interacciones, para evitar re-procesamiento innecesario.

**[Amazon Sneakers](https://www.amazon.com/sneakers/s?k=sneakers)**: Datasets de zapatillas extraído de Amazon US.
 * **[build-datasets](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon-sneakers/build-datasets.ipynb):** Construcción de un datasets de items e interacciones de usuarios en base a files generados en la etapa de scrapping de datos.
 * **[data-loader](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon-sneakers/data-loader.ipynb):** Carga de datos en la base de datos de RecSys](http://recsys.sytes.net) Abstraccion `Repository`.

**[Movie Lens](https://grouplens.org/datasets/movielens/)**: Datasets de películas con scoring personalizado.
 * **[preprocessing](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/movielens/preprocessing.ipynb)**
 * **[data-loader](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/movielens/data-loader.ipynb):** Carga de datos en la base de datos de RecSys](http://recsys.sytes.net).

**[RecSys REST client testing](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/api-client-test.ipynb):** Administrar users, items, interacciones y matrices de distancia via [RecSys](http://recsys.sytes.net) REST API.



## Comenzando

**Step 1**: Clonar repo.

```bash
$ git clone https://github.com/adrianmarino/rec-sys.git
$ cd rec-sys
```

**Step 2**: Crear environment.

```bash
$ conda env create -f environment.yml
```

**Step 3**: Activar environment.

```bash
$ conda activate rec-sys
```

**Step 4**: Crear base de datos.

```bash
$ mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS recsys"
$ python manage.py migrate
```

**Step 5**: Cear usuario administrador.

```bash
$ python manage.py createsuperuser
```

**Step 6**: Iniciar aplicación web utilizando una clave secreta dummy.

```bash
$ cd recsys
$ export SECRET_KEY="^BJ>Nzq>*8[HKH/ew:]TdfgD<nul;v9R571yvxI"
$ python manage.py runserver localhost:8000
```

**Step 7**: Ir a http://localhost:8000.

**Step 8**: Levantar jupiter lab.

```bash
$ cd ../
$ jupyter lab

Jupyter Notebook 6.1.4 is running at:
http://localhost:8888/?token=45efe99607fa6......
```

**Step 9**: Ejecutar notebook [data-loader](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon/data-loader.ipynb): Carga de datos en la base de datos de [RecSys](http://recsys.sytes.net) Abstraccion `Repository`.



## Calcular Matrices de Similitud

**Step 1**: Activar environment.

```bash
$ conda activate rec-sys
```

**Step 2**: Calcular matrices de distancia utilizando SVD.

```bash
$ cd recsys
$  python bin/svd_distance_matrix_job.py
```

**Step 3**: Calcular matrices de distancia utilizando NMF.

```bash
$ cd recsys
$  python bin/nmf_distance_matrix_job.py
```

Ambos jobs calcular matrices de distancia user-user/item-item en base a la matriz de rating predicha por cada model (SVD/NMF). Luego, realizan un upsert de estas matrices en la base de datos, insertando unicamente los N vecinos mas cercanos en ambos casos (user-user/item-item). Cada matrix esta versionada. Es decir, que cada ejecución de un job crear una nueva versión de la matrix. Finalmente, ambas matrices queda asociadas a una entidad en la base de datos que representa al modelo con el que fue predicha.


## SurpriseSimilarityMatrixJob : Diagrama de interación


<img src="https://raw.githubusercontent.com/magistery-tps/rec-sys/main/diagrams/similarity_matrix_job.svg">

## Correr [RecSys](http://recsys.sytes.net) como servicio [systemd](https://systemd.io/)


**Step 1**: Clonar repo.

```bash
$ cd ~
$ git clone https://github.com/adrianmarino/airflow-systemd.git
$ mv airflow-systemd airflow
$ cd recsys
```

**Step 2**: Crear conda environment requerido para correr recsys como un servicio.

```bash
$ conda env update -f environment.yml
```

**Step 3**: Copiar file.service a `~/.config/systemd/user/`:

```bash
$ cp recsys.service ~/.config/systemd/user/
```

**Step 4**: Importar variable de entoeno requeridas por la aplicación:

```bash
$ echo "source ~/recsys/.shell.recsysrc" >> ~/.bashrc
ó
$ echo "source ~/recsys/.shell.recsysrc" >> ~/.zshrc
```


**Step 4**: Referscar la configuración de systemd.

```bash
$ systemctl --user daemon-reload
```

**Step 5**: Habilitar el servicio apra que se inie al bootear el sistema.

```bash
$ systemctl --user enable recsys
```

**Step 6**: Iniciar el servicio en background.

```bash
$ systemctl --user start recsys
```
gd
