# 01_Dmine - Carpeta de Archivos de Minería de datos de parámetros para la Plataforma de Conocimientos de Ciudades Sustentables
----------
**INSTITUTO NACIONAL DE ECOLOGÍA Y CAMBIO CLIMÁTICO.**

**PROGRAMA DE LAS NACIONES UNIDAS PARA EL DESARROLLO**

----------


### Introduccion

*"…Una ciudad sustentable permite a todos sus ciudadanos satisfacer sus propias necesidades y mejorar su bienestar sin dañar el entorno natural ni poner en peligro las condiciones de vida de otras personas, en el presente o en el futuro… "* (Girardet, 2001)

Aludir al concepto de ciudades sustentables significa, esencialmente, una declaración hacia una planeación urbana comprometida con el medio ambiente y orientada a mejorar la calidad de vida de sus habitantes, tanto a nivel local como en el entorno de los centros urbanos.

Es posible evaluar el nivel de Sustentabilidad de una Ciudad en Diez Dimensiones: Agua, Aire, Uso de Suelo, Edificaciones, Industria, Energía, Movilidad, Habitabilidad, Bienes y Servicios Ambientales y Residuos Sólidos Urbanos; cada dimensión compuesta por métricas construidas desde criterios, parámetros y atributos inherentes a todas las ciudades.

En este sentido, y para ofrecer Información Oportuna, Confiable, Actualizada y Valiosa en materia de evaluación de la sustentabilidad en las ciudades del país, el Instituto Nacional de Ecología y Cambio Climático (INECC) desarrolla el proyecto de  Plataforma de Conocimiento sobre Ciudades Sustentables (PCCS).

La PCCS proporciona servicios de Información, asesoría y vinculación para instituciones públicas, privadas y sociales, gobiernos locales y ciudadanía interesada en materia de combate al cambio climático y desarrollo urbano Sustentable. Los contenidos de la PCCS se proporcionan de manera sistematizada en Diez Dimensiones para las 135 ciudades que conforman el Subsistema Principal del Sistema Urbano Nacional (SUN).

Este directorio contiene la memoria de construcción de parámetros para la PCCS. A pesar de que la transformación de la información podría realizarse manualmente utilizando software de hoja de cálculo, el manejo de la información se ha realizado desde scripts de python, con los objetivos de: 

1. Generar una memoria del trabajo de transformación de datos, 
2. Que la investigación sea reproducible, 
3. Que sea posible rastrear las fuentes de información, dar seguimiento a las transformaciones de datos y soportar los resultados presentados a manera de dimensiones e indicadores en la PCCS. 

### Descripcion del Contenido
**Tipos de Archivos**

Para lograr que la investigación de parámetros sea reproducible, esta carpeta se ofrece para su consulta desde internet y contiene los siguientes archivos especializados:

- **Archivos readme.md** - Archivos en formato Markdown para ser leídos desde navegador web, que incluyen descripciones y aclaraciones para cada carpeta  dentro del directorio
- **Archivos \*.py** - Scripts en python 3.6.1, por medio de los cuales se realizan transformaciones, estandarizaciones y presentaciones de la información.
- **Archivos \*.ipynb** - Scripts en Jupyter Notebook Markdown, análisis realizados directamente sobre datasets y disponibles para su consulta desde navegador web, para casos en los que los manejos de la información requieren consideraciones especiales.
- __Archivos P****.xlsx__ - Fichas de parámetro en formato "Open XML Spreadsheet" con datos procesados, incluyendo metadatos e información de integridad.

**Contenido de las Carpetas**

- **00_Generales** - Parámetros de uso general y transversal en la plataforma
- **01_Agua** - Parámetros identificados durante la elaboración de indicadores para la dimensión agua.
- **02_Aire** - Parámetros identificados durante la elaboración de indicadores para la dimensión Aire.
- **03_UsoDeSuelo** - Parámetros identificados durante la elaboración de indicadores para la dimensión Uso de Suelo. 
- **04_Edificaciones** - Parámetros identificados durante la elaboración de indicadores para la dimensión Edificaciones.
- **05_Industria** - Parámetros identificados durante la elaboración de indicadores para la dimensión Industria.
- **06_Energia** - Parámetros identificados durante la elaboración de indicadores para la dimensión Energía.
- **07_Movilidad** - Parámetros identificados durante la elaboración de indicadores para la dimensión Movilidad.
- **08_Habitabilidad** - Parámetros identificados durante la elaboración de indicadores para la dimensión Habitabilidad.
- **09_BienesAmbientalesYServiciosPublicos** - Parámetros identificados durante la elaboración de indicadores para la dimensión Bienes Ambientales y Servicios Públicos.
- **10_ResiduosSolidosUrbanos** - Parámetros identificados durante la elaboración de indicadores para la dimensión Residuos Sólidos Urbanos.
- **Datasets** - Incluye los datasets fuente desde los cuales se realizó la desagregación de parámetros, incluyendo memoria de las fuentes y metadatos para cada dataset.
- **Scripts** - Incluye scripts que se reutilizan durante la construcción de parámetros.

**Descripcion de los archivos PXXX.xlsx**
Cada parámetro procesado en el proceso de minería y estandarización cuenta con una ficha que contiene:

METADATOS: Descripciones del paquete de datos (Detalladas mas adelante en este documento)

PARAMETRO: Datos que se utilizarán para la PCCS, desagregados a nivel de clave del SUN.

DATOS: Datos fuente que se utilizaron para la construccion del parámetro.

INTEGRIDAD: Análisis de integridad por ciudad, calculado como el promedio de *"VAR\_INTEGRIDAD"* de los municipios que componen cada ciudad del SUN. 

EXISTENCIA: Verificación *"VAR\_INTEGRIDAD"* por municipio. El método de cálculo de integridad por municipio se describe en la hoja de metadatos en el renglón *"VAR\_INTEGRIDAD"*

**Descripciones de las fichas de metadatos**

*DESCRIPCION DEL PARAMETRO*

- **Clave**: Clave única del Parámetro
- **Nombre del Parametro**: Nombre corto del Parametro
- **Descripcion del Parametro**: Descripcion a detalle del parámetro
- **Periodo**: Periodo al que corresponde el parámetro.
- **Unidades**: Unidades en las que se encuentra el parámetro.
  
*DESCRIPCION DEL PROCESO DE MINERIA*

- **Nombre del Dataset**: Nombre del dataset desde donde se obtuvieron los datos
- **Descripcion del dataset**: Descripcion del dataset fuente desde donde se obtuvieron los datos.
- **Disponibilidad Temporal**: Periodos disponibles en el dataset desde donde se obtuvieron los datos. 
- **Periodo de actualizacion**: Periodicidad con la que el autor del dataset fuente actualiza los datos.  
- **Nivel de Desagregacion**: Nivel de detalle en el que se encuentran disponibles los datos.
Notas: Notas especificas referentes al procesmiento de datos de cada parámetro. 
- **Fuente**: Organismo o institución autora de los datos
- **URL_Fuente**: Sitio desde donde se realizó la descarga de los datos. 
- **Dataset base**: localización del Dataset fuente después de realizados los procesos de estandarizacion que permiten el uso de los datos 
- **Repositorio de mineria**: 
Método de Agregación: 
- **VAR_INTEGRIDAD**: Calculo de integridad independiente para cada Dataset de la PCCS (Ver metadatos del Dataset).

----------
Junio, 2018
