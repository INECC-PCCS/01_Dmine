# DATASETS DE INFONAVIT #
Desde INFONAVIT se obtuvieron los siguientes datasets:

- LISTA DE DESARROLLOS SUSTENTABLES

## Lista de Desarrollos Sustentables

Fecha de descarga: 10/05/2018  12:05:00 p.m. desde:
[http://portal.infonavit.org.mx/wps/wcm/connect/7d1462f9-4374-4630-b07d-29cbdefcd8d5/Lista_de_desarrollos_sustentables.pdf?MOD=AJPERES&CVID=lN5RKFV&CVID=lN5RKFV&CVID=lEFwNyh&CVID=lEFwNyh&CVID=lEFwNyh](http://portal.infonavit.org.mx/wps/wcm/connect/7d1462f9-4374-4630-b07d-29cbdefcd8d5/Lista_de_desarrollos_sustentables.pdf?MOD=AJPERES&CVID=lN5RKFV&CVID=lN5RKFV&CVID=lEFwNyh&CVID=lEFwNyh&CVID=lEFwNyh)

**Proceso de limpieza:**
INFONAVIT publica una lista con desarrollos sustentables en formato .PDF. El PDF fue transformado en tabla de excel utilizando el servicio [https://www.pdftoexcel.com/](https://www.pdftoexcel.com/)

El siguiente archivo parte del excel obtenido desde el PDF para desarrollar la limpieza de datos:
[https://github.com/INECC-PCCS/01_Dmine/tree/master/Datasets/CONAGUA/Catalogo_de_Plantas_de_Tratamiento_Aguas_Residuales.xlsx](https://github.com/INECC-PCCS/01_Dmine/tree/master/Datasets/INFONAVIT/Lista_de_desarrollos_sustentables.xlsx)

A continuación se describe el proceso de limpieza, desarrollado hoja por hoja:

(Sheet1) Hoja con datos crudos

(1) Alinear encabezados, eliminar renglones vacios y renglones con datos basura.

(2) Alinear columnas de Zacatecas, rellenar ENTIDAD FEDERATIVA

(3) Asignar CVE_MUN

(4) Pegar valores, eliminar columnas que ya no se utilizarán: [ENTIDAD FEDERATIVA, NOM_EDO, CVE_EDO, EE_MUN]

(5) dataset estandarizado
