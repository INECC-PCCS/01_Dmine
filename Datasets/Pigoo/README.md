# DATASET PIGOO - PROGRAMA DE INDICADORES DE GESTIÓN DE ORGANISMOS OPERADORES

**AGREGACION DE DATOS DESDE EL DATASET DEL PROGRAMA DE INDICADORES DE GESTIÓN DE ORGANISMOS OPERADORES (PIGOO)**

El dataset de indicadores del PIGOO cuenta con 29 indicadores de gestión del agua que pueden ser utilizados como parámetros para la construcción de indicadores para la Plataforma de Conocimiento de Ciudades Sustentables (PCCS). Estos indicadores cuentan con datos para cada año desde 2002 hasta 2015.

La dificultad de este dataset radica en que la desagregacion de los datos se realizó por estado y nombre de ciudad (Texto plano), una clasificación que no corresponde directamente con la establecida por el INEGI para el Marco Geoestadístico Nacional ni para la clasificación establecida por CONAPO/SEDESOL para el Sistema Urbano Nacional.

En este documento se describen las consideraciones que se tomaron para la agregación de datos desde este dataset para su uso en la PCCS.

**DOCUMENTOS INCLUIDOS EN ESTE REPOSITORIO**

Archivo|Descripción
-------|-----------
**Aclaracion_Desagregacion.pdf**|Copia de la solicitud de aclaracion de desagregacion de los datos realizada al PIGOO, así como la respuesta de PIGOO
**CiudadesPIGOO\_ClaveInegi.xlsx**|Archivo con clasificacion de ciudades por clave geoestadística, proporcionado por el PIGOO
**CiudadesPIGOO\_ClaveInegi\_prev.xlsx**|Archivo de trabajo para emparejar nombres de ciudades entre datasets ("CiudadesPIGOO\_ClaveInegi.xlsx" y Dataset Pigoo)
**pigoo\_desagregacion.py**|Detalle de procesos y consideraciones particulares tomadas para estandarizar el dataset 'PIGOO'
**pigoo\_notreviewd.xlsx**|Reporte de municipios en el dataset 'PIGOO' que no fueron incluidos en la estandarizacion por no pertenecer al Subsistema Principal del SUN
**README.md**|Este archivo
**standard-pigoo\_ooapas\_geo.xlsx**|Lista de emparejamiento entre datasets  "CiudadesPIGOO_ClaveInegi.xlsx", "Dataset Pigoo" y "CVE\_MUN" de la PCCS

----------

Instituto Nacional de Ecología y Cambio Climático

Programa de las Naciones Unidas para el Desarrollo

Plataforma de Conocimiento de Ciudades Sustentables

Octubre de 2017