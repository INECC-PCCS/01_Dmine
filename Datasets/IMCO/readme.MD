# INSTITUTO MEXICANO PARA LA COMPETITIVIDAD
## Producto Interno Bruto

Se obtuvieron datos desde el Indice de Competitividad Urbana 2016 publicado por el Instituto Mexicano para la Competitividad. Los datos que publica el IMCO ya se encuentran disponibles a un nivel de desagregación municipal, en periodos anuales de 2008 a 2014. Para la agregación de datos a nivel del SUN, se compilaron para cada parámetro de los listados en este documento los datos correspondientes a los años 2010 y 2014.

Los parámetros que se obtienen desde esta fuente son:

Parámetro | Descripcion
:-------- | :------------
P0030     | Índice de Competitividad Urbana 
P0038     | Coeficiente de Gini
P0204     | Recomendaciones a la población asociadas a la calidad del aire
P0308     | Áreas urbanas verdes per cápita
P0614     | Producto Interno Bruto
P0812     | Indice de Impunidad
P1012     | Aprovechamiento o quema de biogás en rellenos sanitarios


Pagina del IMCO: 

[http://imco.org.mx/](http://imco.org.mx/ "IMCO")

Indice de Competitividad Urbana 2016
Fecha de descarga: 09/05/2018  12:59:00 p. m.
URL: [http://imco.org.mx/indices/reeleccion-municipal-y-rendicion-de-cuentas/capitulos/resultados-del-indice-de-competitividad-urbana-2016](http://imco.org.mx/indices/reeleccion-municipal-y-rendicion-de-cuentas/capitulos/resultados-del-indice-de-competitividad-urbana-2016 "Indice de Competitividad Urbana")

Base de datos: [http://api.imco.org.mx/release/latest/vendor/imco/indices-api/documentos/Competitividad/%C3%8Dndice%20de%20Competitividad%20Urbana/2016-09-07_0900%20Reelecci%C3%B3n%20municipal%20y%20rendici%C3%B3n%20de%20cuentas%3A%20%C2%BFC%C3%B3mo%20lograr%20el%20c%C3%ADrculo%20virtuoso%3F/Documentos%20de%20resultados/2016%20ICU%20Base%20de%20datos.xlsx](http://api.imco.org.mx/release/latest/vendor/imco/indices-api/documentos/Competitividad/%C3%8Dndice%20de%20Competitividad%20Urbana/2016-09-07_0900%20Reelecci%C3%B3n%20municipal%20y%20rendici%C3%B3n%20de%20cuentas%3A%20%C2%BFC%C3%B3mo%20lograr%20el%20c%C3%ADrculo%20virtuoso%3F/Documentos%20de%20resultados/2016%20ICU%20Base%20de%20datos.xlsx)

**Produccion de datasets de parámetros**

Para la producción de datasets y fichas de parámetros, se extrajeron los datos de cada parametro desde la base de datos de IMCO hacia un archivo estandarizado para cada parámetro. 
Se corrió el compilador (P0XXX.py) para diferentes periodos. Se ejecutó el compilador en cada periodo para producir una ficha de parámetro para cada periodo. Se renombró el archivo de excel para incluir el año del periodo y se cambió la variable var1 en la seccion "_Generar dataset para parámetro y Variable de Integridad_" del compilador, a la del siguiente periodo. Se repitió este proceso para los periodos 2010 y 2014.

Parámetro | Descripcion
:-------- | :------------
P0038     | Coeficiente de Gini
P0308     | Áreas urbanas verdes per cápita
P1012     | Aprovechamiento o quema de biogás en rellenos sanitarios

