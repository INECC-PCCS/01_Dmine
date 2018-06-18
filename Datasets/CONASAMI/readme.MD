# SALARIOS MINIMOS GENERALES#

Se descargaron diferentes datasets desde la Comisión Nacional de los Salarios Mínimos:

**CLASIFICACIÓN DE LOS MUNICIPIOS POR ÁREA GEOGRÁFICA**

[https://www.gob.mx/conasami/documentos/clasificacion-de-los-municipios-por-area-geografica](https://www.gob.mx/conasami/documentos/clasificacion-de-los-municipios-por-area-geografica)

Fecha de descarga: 04/05/2018  12:05:00 p.m.

• Clasificación de los municipios en tres áreas geográficas (Vigente antes del 26 de noviembre de 2012)
[http://www.gob.mx/cms/uploads/attachment/file/106627/Region_A_B_y_C.pdf](http://www.gob.mx/cms/uploads/attachment/file/106627/Region_A_B_y_C.pdf)

• Clasificación de los municipios en dos áreas geográficas (Vigente antes del 01 de octubre de 2015)
[http://www.gob.mx/cms/uploads/attachment/file/106624/Region_A_y_B_-_27_nov_2012.pdf](http://www.gob.mx/cms/uploads/attachment/file/106624/Region_A_y_B_-_27_nov_2012.pdf)

CONASAMI pone los datos disponibles en formato .PDF, por lo que la transformación a dataframes bidimensionales no puede ser trazada (Fue realizada utilizando software externo)

**Proceso de limpieza:**

• Del dataset "Clasificación de los municipios en tres áreas geográficas"

	(1) Eliminar renglones vacíos y encabezados repetidos. Normalizar nombres de encabezados:
	
	| ENCABEZADO  | DESCRIPCION                                 |
	| --------    | ------------                                |
	| CVE_ENT     | Clave geoestadística de entidad (2 dígitos) |
	| NOM_ENT     | Nombre de la Entidad                        |
	| CVE_MUN_3   | Clave geoestadística Municipal (3 Dígitos)  |
	| NOM_MUN     | Nombre del Municipio                        |
	| AG_CONASAMI | Área geográfica de acuerdo con la clasificación de CONASAMI |
	
	(2) Corregir datos de Michoacan (Columnas mal asignadas)
	
	(3) Corregir CVE_MUN_3 en donde la longitud es mayor a 3 digitos, crear CVE_MUN de 5 digitos
	
	(4) Eliminar columnas que ya no se utilizarán
	
• Del dataset "Clasificación de los municipios en tres áreas geográficas"

	(1) Eliminar renglones vacíos y encabezados repetidos. Normalizar nombres de encabezados:
	
	| ENCABEZADO  | DESCRIPCION                                 |
	| --------    | ------------                                |
	| CVE_ENT     | Clave geoestadística de entidad (2 dígitos) |
	| NOM_ENT     | Nombre de la Entidad                        |
	| CVE_MUN_3   | Clave geoestadística Municipal (3 Dígitos)  |
	| NOM_MUN     | Nombre del Municipio                        |
	| AG_CONASAMI | Área geográfica de acuerdo con la clasificación de CONASAMI |
	
	(2) Corregir CVE_MUN_3 en donde la longitud es mayor a 3 digitos, crear CVE_MUN de 5 digitos
	
	(3) Eliminar columnas que ya no se utilizarán, asignar Salarios Minimos Generales para 2015. 

**Produccion de datasets de parámetros**

Para la producción de datasets y fichas de parámetros, se corrió el compilador (P0714.py) para diferentes periodos. Se ejecutó el compilador en cada periodo para producir un archivo P0714.xlsx. Se renombró el archivo de excel para incluir el año del periodo y se cambió la variable M.PeriodoParam en el compilador a la del siguiente periodo. Se repitió este proceso para los periodos 2010, 2011 y 2015.

