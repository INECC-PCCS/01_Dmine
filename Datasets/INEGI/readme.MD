# INEGI - Datos obtenidos bajo solicitud

Se realizó una solicitud a INEGI (archivo CGCV-DES-005-2017.pdf del 11 de julio de 2017) por los datos del módulo 6 de la Encuesta Nacional de Gobiernos Municipales y Delegacionales (ENGMD) 2011, para la obtención de insumos para los siguientes parámetros:

ID 		| Descripcion
:---- 	| :-----
P1007	| Número de municipios con reglamentos relacionados con los RSU
P1013	| Número de municipios con rellenos sanitarios
P1014	| Número de municipios con tiraderos a cielo abierto
P1015	| Número de municipios que envían residuos a una planta de tratamiento
P1016	| Número de municipios con estaciones de transferencia

Como respuesta a la solicitud, INEGI entregó (archivo INEGI 1310-5-227-2017.pdf del 10 de agosto de 2017) microdatos de la ENGMD 2015. 

## Numero de Municipios con sitios de disposición de RSU
Dentro de los datos proporcionados por INEGI, se incluyó una capa de información geográfica (SDF.shp) compuesta por puntos, en la que cada punto representa un sitio de disposición de residuos. Los parámetros de la capa describen el tipo de sitio de disposición, por lo que para formar los parámetros P1013, P1014 y P1015 es necesario clasificar estos puntos. Para hacerlo, se abre el archivo .dbf de la capa y se guarda en formato de excel. Ya en excel, se realiza una estandarización de los datos:

	1. Creación de CVE_MUN de 5 dígitos. Eliminacion de información duplicada o irrelevante.

El archivo estandarizado se guardó como PUNTOSDISP.xlsx

Desde esta capa, y realizando un conteo de puntos por medio de la clave geoestadística, se generan los siguientes parámetros:

ID 		| Descripcion
:---- 	| :-----
P1013	| Número de rellenos sanitarios
P1014	| Número de tiraderos a cielo abierto
P1015	| Número de plantas de tratamiento [No viene en el dataset, vienen "Sitios Controlados"]

## Estaciones de Transferencia
El módulo 8 de la ENGMD 2015 (Tabla TR_CNGMD15_M6_P8_1.xlsx) contiene datos de las estaciones de transferencia de residuos solidos urbanos. La limpieza de la hoja de microdatos de este tema se realizó siguiendo los siguientes pasos:

(0) Crear CVE_MUN, Eliminar Columnas duplicadas o que no se utilizarán

(1) Eliminar columnas fuente para CVE_MUN, Compilar funciones de la estación en una sola columna

(2) Eliminar columnas fuente para "Funciones E-Transf", cambiar nombres de columnas a mnemónicos.

(3) Dataset estandarizado.

El archivo de estandarización de este dataset se encuentra en:

Carpeta		| Ubicación
:---- 		| :-----
Local		| D:\\PCCS\\01\_Dmine\\Datasets\\INEGI\\TRANSFERENCIA.xlsx
Pública		| https://github.com/INECC-PCCS/01\_Dmine/tree/master/Datasets/INEGI/TRANSFERENCIA.xlsx

## Separacion de Residuos Sólidos
Los módulos 2 y 7 de la ENGMD 2015 (Tabla TR_CNGMD15_M6.xlsx) contienen datos de cantidad de residuos solidos urbanos recolectados. En el módulo 7 se encuentran datos referentes a las cantidades de RSU clasificados en orgánicos e inorgánicos. La limpieza de la hoja de microdatos de este tema se realizó siguiendo los siguientes pasos:

(1) Crear CVE_MUN de 5 dígitos, Eliminar columnas de datos que no corresponden a este parámetro.

(2) Eliminar columnas utilizadas para CVE_MUN, cambiar encabezados a mnemónicos.

(3) Compilar columnas RSU-TOTAL-TON y RSU-TOTAL-KG en una sola RSU-TON (Para rellenar valores vacíos). Se tomaron las siguientes consideraciones especiales:
1. Para los municipios que únicamente tenían información en kilogramos, el dato en la columna RSU-TOTAL-KG se dividió entre 1000

2. Para los municipios que únicamente tenían información en toneladas, el dato en la columna RSU-TOTAL-TON se copió a RSU-TON

3. Para los municipios que tenían valores tanto en Kilogramos como en toneladas:
	
	a. Los municipios 05022, 14117, 15119 y 30133 Se sumó el dato de RSU-TOTAL-TON + (RSU-TOTAL-KG / 1000)
	
	b. Los municipios 05031, 11023 y11023 Se copió el dato de  RSU-TOTAL-TON
	
	c. El municipio 11019, se tompo el menor de los valores entre RSU-TOTAL-TON y (RSU-TOTAL-KG / 1000), esto es, 5.465 en la columna RSU-TOTAL-KG / 1000

4. Los municipios que no tenían valores en RSU-TOTAL-TON ni RSU-TOTAL-KG se dejaron vacíos

(4) Crear columna RSU-SUMSEP-TON como RSU-SUMSEP-KG / 1000 en lo general. Revisar congruencia de los datos entre RSU-TON y RSU-SUMSEP-KG. Se tomaron las siguientes consideraciones especiales:

1. La suma de RSU-ORGANICOS-KG + RSU-INORGANICOS-KG debe ser igual a RSU-SUMSEP-KG (Columna temporal CON1). Los muncipios que no cumplen con esta condicion son 14037 y 28027 (El valor de estos muncipios para RSU-SUMSEP-TON se calculó como (RSU-ORGANICOS-KG + RSU-INORGANICOS-KG) / 1000

2. El valor de RSU-SUMSEP-TON debe ser menor o igual al valor de RSU-TON. Existen 22 municipios en donde el valor de RSU-SUMSEP-TON es mayor que RSU-TON. Se tomaron las siguientes consideraciones especiales: 

	a. En los municipios donde el porcentaje de la diferencia es menor al 10%, se consideró que la discrepancia se debe al redondeo de decimales. Se asignó el valor de RSU-SUMSEP-TON a RSU-TON (Municipios 13063, 14043, 14102, 20033, 20519, 21187)

	b. En los municipios donde el porcentaje de la diferencia es mayor al 10%,se consideró que los datos no son confiables. Los datos de las columnas RSU-ORGANICOS-KG, RSU-INORGANICOS-KG y RSU-SUMSEP-KG se eliminaron para evitar que se utilicen durante la agregación.

(5) Eliminar columnas temporales creadas con motivos de verificación. Calcular porcentaje de separacion de RSU (Columna SEP-RSU-PRC). La hoja (6) Tiene el dataset final.

(6) Eliminar columnas temporales creadas con motivos de verificación. Calcular porcentaje de separacion de RSU (Columna SEP-RSU-PRC). En los municipios donde RSU-SEP es igual a 2 (No se separan), el porcentaje de separación es cero.

El archivo de estandarización de este dataset se encuentra en:

Carpeta		| Ubicación
:---- 		| :-----
Local		| D:\\PCCS\\01\_Dmine\\Datasets\\INEGI\\SEPARACION-RSU.xlsx
Pública		| https://github.com/INECC-PCCS/01\_Dmine/tree/master/Datasets/INEGI/SEPARACION-RSU.xlsx

