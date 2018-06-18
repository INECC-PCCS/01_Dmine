# DATASETS DE CONAGUA #
Desde CONAGUA se obtuvieron los siguientes datasets:

- Catalogo de plantas de tratamiento en operación 2016
- Monitoreo de la calidad del agua 2017

## Catalogo de plantas de tratamiento en operación 2016
Se realizó una busqueda en datos.gob.mx

[https://datos.gob.mx/busca/dataset?q=plantas%20de%20tratamiento%20de%20aguas%20residuales&](https://datos.gob.mx/busca/dataset?q=plantas%20de%20tratamiento%20de%20aguas%20residuales&)

Fecha de descarga: 04/05/2018  12:05:00 p.m. desde:

[https://datos.gob.mx/busca/dataset/catalogo-de-plantas-de-tratamiento-de-aguas-residuales-en-operacion-de-conagua](https://datos.gob.mx/busca/dataset/catalogo-de-plantas-de-tratamiento-de-aguas-residuales-en-operacion-de-conagua)

**Proceso de limpieza:**

[https://github.com/INECC-PCCS/01_Dmine/tree/master/Datasets/CONAGUA/Catalogo_de_Plantas_de_Tratamiento_Aguas_Residuales.xlsx](https://github.com/INECC-PCCS/01_Dmine/tree/master/Datasets/CONAGUA/Catalogo_de_Plantas_de_Tratamiento_Aguas_Residuales.xlsx)

(1) Agregar CVE\_EDO y CVE\_MUN

(2) Copiar y pegar valores, eliminar columnas redundantes: CVE\_EDO, ESTADO, MUNICIPIO; Eliminar columnas que ya no se utilizarán: EE\_MUN, LOCALIDAD.

(3) tiene el dataset estandarizado

## Monitoreo de la calidad del agua 2017
Se descargaron capas geográficas desde:
[http://sina.conagua.gob.mx/sina/index_jquery-mobile2.html?tema=calidadAgua](http://sina.conagua.gob.mx/sina/index_jquery-mobile2.html?tema=calidadAgua)

Las capas descargadas son:

- Demanda Bioquimica de Oxigeno (DBO5).
- Demanda Química de Oxígeno (DQO).
- Sólidos Suspendidos Totales (SST).
- Coliformes fecales (CF).
- Sólidos Disueltos Totales (SDT).

Para iniciar el proceso de limpieza de estas capas, se utilizará con una capa geográfica con los 445 municipios que contienen las 135 ciudades del Subsistema Principal del Sistema Urbano Nacional. La capa se encuentra almacenada de manera local en 
D:\PCCS\00\_RawData\00\_Geo\ROQUE\445\_municipios\_CS.shp

### Sólidos Suspendidos Totales (SST)
La capa se procesó en ArcMap para asignar Claves Geoestadísticas Municipales de 5 dígitos (CVE_MUN) a cada estación de monitoreo.

**Proceso de limpieza:**

(0) Las capas que se utilizaron para este análisis son: 

- 445\_municipios\_CS.shp
- EMCA\_SST\_2017.shp

(1) ArcToolbox > Analysis Tools > Statistics > Tabulate Intersection

- Input Zone Features: 445\_municipios\_CS.shp
- Zones Fields: CVE_MUN, MUNICIPIO
- Input Class Features: EMCA\_SST\_2017.shp
- Class Fields: FID

(2) Por medio de un _JOIN_ se agregan las claves municipales desde la tabla recien creada a la capa EMCA\_SST\_2017.shp

(3) Se crea una capa nueva [P0108(1)] con los puntos a los que les fue asignada una clave municipal.

(4) Algunos puntos no recibieron clave municipal debido a que se encuentran ubicados en la costa y no intersectan a los polígonos municipales. A estos municipios se les asigna manualmente la clave municipal, para lo cual se crea una capa independiente [EMCA-SST-2017-NOMUN]. 

(5) Una vez asignadas las claves municipales a los puntos en costa, se guardan en una capa independiente [P0108(2)]

(6) Las capas P0108(1) y P0108(2) se unen en una sola capa P0108

(7) El archivo P0108.dbf de la capa recien creada se abre en excel y se guarda una copia P0108.xlsx

(8) Sobre P0108.xlsx se corrigen problemas de encoding. desde este archivo se realiza la desagregación a nivel SUN y la ficha del parámetro.

### Demanda Química de Oxígeno
La capa se procesó en ArcMap para asignar Claves Geoestadísticas Municipales de 5 dígitos (CVE_MUN) a cada estación de monitoreo.

**Proceso de limpieza:**

(0) Las capas que se utilizaron para este análisis son: 

- 445\_municipios\_CS.shp
- EMCA\_DQO\_2017.shp

(1) ArcToolbox > Analysis Tools > Statistics > Tabulate Intersection

- Input Zone Features: 445\_municipios\_CS.shp
- Zones Fields: CVE_MUN
- Input Class Features: EMCA\_DQO\_2017.shp
- Class Fields: FID

(2) Por medio de un _JOIN_ se agregan las claves municipales desde la tabla recien creada a la capa EMCA\_DQO\_2017.shp

(3) Algunos puntos no recibieron clave municipal debido a que se encuentran ubicados en la costa y no intersectan a los polígonos municipales. A estos municipios se les asigna manualmente la clave municipal

(4) Una vez asignadas las claves municipales a los puntos en costa, se guardan en una capa independiente [P0107] todos aquellos puntos a los que fue asignada una clave municipal.

(5) El archivo P0107.dbf de la capa recien creada se abre en excel y se guarda una copia P0107.xlsx

(6) Sobre P0107.xlsx se corrigen problemas de encoding. Desde este archivo se realiza la desagregación a nivel SUN y la ficha del parámetro.

### Coliformes Fecales
La capa geográfica ya contaba con Claves Geoestadísticas Municipales para cada estación de monitoreo. Las claves en la tabla de atributos son valores numéricos por lo que es necesario convertirlas a texto de 5 dígitos para preservar aquéllas claves con ceros a la izquierda.

**Proceso de limpieza:**

(0) Las capas que se utilizaron para este análisis son: 

- EMCA\_CF\_2017.shp

(1) El archivo EMCA\_CF\_2017 de la capa se abre en excel y se guarda una copia como P0121.xlsx

(2) Sobre P0121.xlsx se corrigen problemas de encoding y se crea la columna CVE\_MUN de 5 dígitos. Desde este archivo se realiza la desagregación a nivel SUN y la ficha del parámetro.

### Demanda Bioquímica de Oxígeno
La capa se procesó en ArcMap para asignar Claves Geoestadísticas Municipales de 5 dígitos (CVE_MUN) a cada estación de monitoreo.

**Proceso de limpieza:**

(0) Las capas que se utilizaron para este análisis son: 

- 445\_municipios\_CS.shp
- EMCA\_DBO\_2017.shp

(1) ArcToolbox > Analysis Tools > Statistics > Tabulate Intersection

- Input Zone Features: 445\_municipios\_CS.shp
- Zones Fields: CVE_MUN
- Input Class Features: EMCA\_DBO\_2017.shp
- Class Fields: FID

(2) Por medio de un _JOIN_ se agregan las claves municipales desde la tabla recien creada a la capa EMCA\_DBO\_2017.shp

(3) Algunos puntos no recibieron clave municipal debido a que se encuentran ubicados en la costa y no intersectan a los polígonos municipales. A estos municipios se les asigna manualmente la clave municipal

(4) Una vez asignadas las claves municipales a los puntos en costa, se guardan en una capa independiente [P0106] todos aquellos puntos a los que fue asignada una clave municipal.

(5) El archivo P0106.dbf de la capa recien creada se abre en excel y se guarda una copia P0106.xlsx

(6) Sobre P0106.xlsx se corrigen problemas de encoding. Desde este archivo se realiza la desagregación a nivel SUN y la ficha del parámetro.

## Disponibilidad en acuíferos.
Se descargaron 5 capas de información geográfica desde [SINA](http://sina.conagua.gob.mx/sina/tema.php?tema=acuiferos&ver=mapa), correspondientes a la disponibilidad en acuíferos de 2011 a 2015. 
Estas capas se analizarán geográficamente para seleccionar 


(1) Se abre el archivo .dbf de cada dataset para extraer el dato de disponibilidad de cada año. Posteriormente se integran a una sola capa.

(2) Se calcula el área de cada acuífero en la proyección actual (CCL\_ITRF\_1992). Este calculo no es para ser utilizado como parámetro sino como referencia.

(3) Se calcula el area de cada municipio de las ciudades del SUN en la proyección actual (CCL\_ITRF\_1992). Este calculo no es para ser utilizado como parámetro sino como referencia.

(4) Se intersectan los layers de municipios y acuíferos, para obtener un polígono de cada acuífero respecto al o los municipios en los que se encuentra.

(5) En la nueva capa creada, se eliminan columnas redundantes, columnas que ya no tienen datos valiosos y columnas que pueden generarse utilizando la CVE\_MUN. En el dataset quedan solo las siguientes columnas:

- FID
- Shape
- FID_all
- ORIG_FID
- CVE_MUN
- Area_mun
- id_acuif
- nom_acuif
- id_rha
- nom_rha
- area_acuif

(6) La capa resultante de la intersección tiene muchos objetos compuestos de dos o más polígonos. . Se crea una columna para identificar los polígonos de esta operación (FID_all), con numeros ascendentes a partir de cero.

(6) Se calcula el area de cada uno de los polígonos de acuíferos que se intersectaron en el paso anterior en la proyección actual (CCL\_ITRF\_1992), en una columna llamada AcAreaintr. Este calculo no es para ser utilizado como parámetro sino como referencia.

(7) Se seleccionan por posición, aquéllos polígonos que intersectan con polígonos de la capa "Ciudades Sustentables\_135\_localidad.shp"

(8) Se crea una nueva capa "P0105.shp" desde los polígonos seleccionados, que se utilizará para construir el parámetro.

(9) A partir del archivo .dbf de la capa "P0105" Se hace la desagregación a nivel del SUN, promediando los valores de disponibilidad para cada año.

