# DATASET PIGOO - PROGRAMA DE INDICADORES DE GESTIÓN DE ORGANISMOS OPERADORES

**AGREGACION DE DATOS DESDE EL DATASET DEL PROGRAMA DE INDICADORES DE GESTIÓN DE ORGANISMOS OPERADORES (PIGOO)**

El dataset de indicadores del PIGOO cuenta con 29 indicadores de gestión del agua que pueden ser utilizados como parámetros para la construcción de indicadores para la Plataforma de Conocimiento de Ciudades Sustentables (PCCS). Estos indicadores cuentan con datos para cada año desde 2002 hasta 2015. 

La dificultad de este dataset radica en que la desagregacion de los datos se realizó por estado y nombre de ciudad (Texto plano), una clasificación que no corresponde directamente con la establecida por el INEGI para el Marco Geoestadístico Nacional ni para la clasificación establecida por CONAPO/SEDESOL para el Sistema Urbano Nacional.

En este documento se describen las consideraciones que se tomaron para la agregación de datos desde este dataset para su uso en la PCCS.

**DOCUMENTOS INCLUIDOS EN ESTE REPOSITORIO**

Archivo|Descripción
-------|-----------
Aclaracion_Desagregacion.pdf|Copia de la solicitud de aclaracion de desagregacion de los datos realizada al PIGOO
CiudadesPIGOO_ClaveInegi.xlsx|Archivo con clasificacion de ciudades por clave geoestadística, proporcionado por el PIGOO
pigoo.py|script con instrucciones para ordenar y estandarizar el Dataset pigoo para su utilización en la creación de parámetros para la PCCS
pigoo_desagregacion.py|Detalle de analisis preliminar al archivo "CiudadesPIGOO_ClaveInegi.xlsx" para estandarización del Dataset
README.md|Este archivo

## 1. Solicitud de aclaracion al PIGOO
El 2 de octubre de 2017 se realizó por medio de correo electrónico, una solicitud de aclaracion al PIGOO del nivel de desagregación de los datos disponibles en su página (Ver archivo Aclaracion_desagregacion.pdf).

En respuesta a esta solicitud, el PIGOO proporcionó un archivo de excel (_CiudadesPIGOO\_ClaveInegi.xlsx_) que incluye una clasificación de las ciudades del dataset PIGOO por clave del Sistema Urbano Nacional.

## 2. Consideraciones Generales para la estandarización del Dataset.
El archivo _pigoo_desagregacion.py_ contiene el proceso detallado por medio del cual se analizó el archivo _CiudadesPIGOO_ClaveInegi.xlsx_, para tomar decisiones respecto a la clasificacion de ciudades del pigoo e integrarlas a la clasificacion del SUN.
Este análisis incluyó la selección de ciudades que se encuentran en el Subsistema Principal, un análisis de integridad en base a municipios así como asignaciones particulares de integridad para casos particulares (Por ejemplo, Ciudad de México), explicados en la siguiente sección.

## 3. Consideraciones Particulares para la estandarización del Dataset.
1. **Zona Metropolitana del Valle de México.**


2. **Caso 2**


3. **Caso 3**


4. **Caso 4**


----------

Instituto Nacional de Ecología y Cambio Climático

Programa de las Naciones Unidas para el Desarrollo

Plataforma de Conocimiento de Ciudades Sustentables

21 de agosto de 2017