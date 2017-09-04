# Verificador de integridad de datos para ciudades del Sistema Urbano Nacional.

Verifica cuantas ciudades del subsistema Principal del SUN se encuentran en un dataset.
De las ciudades que se encuentran en el SUN, verifica que existan todos los municipios que componen la ciudad.
para cada ciudad en el dataset, verifica que existan registros para todos los municipios que componen la ciudad. 

El algoritmo espera las siguientes entradas:

`dataframe_sun`:  dataframe con claves sun y claves mun, creado con la funcion "asignar_sun" disponible en https://github.com/Caranarq/SUN


----------


**Plataforma de Conocimiento de Ciudades Sustentables 

Instituto Nacional de Ecologia y Cambio Climatico

Programa de las Naciones Unidas para el Desarrollo**