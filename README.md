# 01_Dmine - Carpeta de Archivos de Minería de datos de parámetros para la Plataforma de Conocimientos de Ciudades Sustentables
----------
**INSTITUTO NACIONAL DE ECOLOGÍA Y CAMBIO CLIMÁTICO.**

**PROGRAMA DE LAS NACIONES UNIDAS PARA EL DESARROLLO**

----------


###Introduccion

*"…Una ciudad sustentable permite a todos sus ciudadanos satisfacer sus propias necesidades y mejorar su bienestar sin dañar el entorno natural ni poner en peligro las condiciones de vida de otras personas, en el presente o en el futuro… "* (Girardet, 2001)

La Plataforma de Conocimiento sobre Ciudades Sustentables (PCCS) es un proyecto que comenzó formalmente en agosto de 2016, como una iniciativa para dar respuesta al impacto ambiental de las ciudades mexicanas. El objetivo del proyecto es diseñar y desarrollar una plataforma para suministrar servicios de información, asesoría y vinculación a tomadores de decisiones y a la sociedad en general. Dado que no existe una definición formal para el concepto de ciudad en la Ley General de Asentamientos Humanos, Ordenamiento Territorial y Desarrollo Humano, el INECC ha adoptado las definiciones del Sistema Urbano Nacional (SUN). La determinación del grado de sustentabilidad de las ciudades mexicanas se realiza con base en 10 dimensiones:

1. Agua
2. Aire
3. Uso de Suelo
4. Edificaciones
5. Industria
6. Energia
7. Movilidad
8. Habitabilidad
9. Bienes Ambientales y Servicios Públicos
10. Residuos Sólidos Urbanos

Estas 10 dimensiones, a su vez, se conforman con indicadores de sustentabilidad cuyos parámetros son la información cuantitativa y cualitativa de cada ciudad. Los parámetros son obtenidos desde múltiples fuentes, en todos los casos oficiales y disponibles al público para su consulta. Los datos obtenidos de estas fuentes se transforman con el objetivo de tenerlos disponibles para la PCCS con el nivel de agregación del SUN y en formatos estándar que permitan su análisis de manera ágil y en su caso, sistematizada.

Este directorio contiene la memoria de construcción de indicadores para la PCCS. A pesar de que la transformación de la información podría realizarse manualmente utilizando software de hoja de cálculo, el manejo de la información se ha realizado desde scripts de python, a manera de que se cuente con una memoria del trabajo de transformación de datos, que la investigación sea reproducible, y que sea posible rastrear las fuentes de información, dar seguimiento a las transformaciones y soportar los resultados presentados a manera de dimensiones e indicadores en la PCCS. 

### Descripcion del Contenido
**Tipos de Archivos**

Para lograr que la investigación de parámetros sea reproducible, esta carpeta se ofrece para su consulta desde internet y contiene los siguientes archivos especializados:

- **Archivos readme.md** - Archivos en formato Markdown para ser leídos desde navegador web, que incluyen descripciones y aclaraciones para cada carpeta  dentro del directorio
- **Archivos \*.py** - Scripts en python 3.6.1, por medio de los cuales se realizan transformaciones, estandarizaciones y presentaciones de la información.
- **Archivos \*.ipynb** - Scripts en Jupyter Notebook Markdown, análisis realizados directamente sobre datasets y disponibles para su consulta desde navegador web, para casos en los que los manejos de la información requieren consideraciones especiales.
- __Archivos P****.xlsx__ - Libros de formato "Open XML Spreadsheet" con parámetros procesados, incluyendo metadatos e información de integridad.

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

----------

Octubre, 2017

