# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 11:14:28 2018

@author: carlos.arana

Objeto estándar de metadatos
"""

import pandas as pd
module_path = r'D:\PCCS\01_Dmine\Scripts'
if module_path not in sys.path:
    sys.path.append(module_path)

from AsignarDimension.AsignarDimension import AsignarDimension

class Meta:
    def __init__(self, name):
        # Descripciones del Parámetro
        self.name = name
        self.ClaveParametro = str()
        self.NombreParametro = str()
        self.DescParam = str()
        self.UnidadesParam = str()
        self.TituloParametro = str()  # Para nombrar la columna del parametro
        self.PeriodoParam = str()
        self.TipoInt = int()
        self.ParDtype = str()

        # Descripciones del proceso de Minería
        self.nomarchivodataset = str()
        self.extarchivodataset = str()
        self.ArchivoDataset = str()
        self.ContenidoHojaDatos = str()
        self.ClaveDataset = str()
        self.ActDatos = str()
        self.Agregacion = str()
        self.DescVarIntegridad = str()
        self.DirFuente = str()
        self.DSBase = str()
        self.ClaveDimension = str()
        self.NomDimension = str()
        self.DirDimension = str()
        self.RepoMina = str()
        self.DirDestino = str()

        # Metadatos desde dataset estandarizado
        self.metadataset = pd.DataFrame()

    def fillmeta(self):
        if self.TipoInt == 1:
            self.DescVarIntegridad = 'La variable de integridad municipal para esta Dataset es binaria: \n' \
                                '1 =  El municipio cuenta con informacion \n0 = El municipio no cuenta con información'
        if self.TipoInt == 2:
            self.DescVarIntegridad = 'Para calcular la variable de integridad de este dataset, se verifica la ' \
                                     'existencia de datos en cada una de las variables que se utilizaron para ' \
                                     'construir el parámetro. El valor de la variable de integridad multiplicado por ' \
                                     '100 indica el porcentaje de variables del dataset que tienen datos para ' \
                                     'la construcción del parámetro'
        self.ArchivoDataset = self.nomarchivodataset + self.extarchivodataset
        self.DirFuente = r'D:\PCCS\01_Dmine\Datasets\{}'.format(self.ClaveDataset)
        self.DSBase = '"{}", disponible en https://github.com/INECC-PCCS/01_Dmine/tree/master/Datasets/{}'.format(
            self.ArchivoDataset, self.ClaveDataset)
        self.ClaveDimension = self.ClaveParametro[1:3]
        self.NomDimension = AsignarDimension(self.ClaveDimension)['nombre']
        self.DirDimension = self.ClaveDimension + "_" + AsignarDimension(self.ClaveDimension)['directorio']
        self.RepoMina = 'https://github.com/INECC-PCCS/01_Dmine/tree/master/{}/{}'.format(
            self.DirDimension, self.ClaveParametro)
        self.DirDestino = r'D:\PCCS\01_Dmine\{}'.format(
            self.ClaveDimension + "_" + AsignarDimension(self.ClaveDimension)['directorio'])

    def metafromds(self):
        # Cargar metadatos del dataset
        metadataset = pd.read_excel(DirFuente + '\\' + ArchivoDataset,
                                    sheetname="METADATOS")
        metadataset.set_index('Metadato', inplace=True)
        metadataset = metadataset['Descripcion']

        # Descripciones generadas desde los metadatos del dataset.
        self.NomDataset = metadataset['Nombre del Dataset']
        self.DescDataset = metadataset['Descripcion del dataset']
        self.DispTemp = metadataset['Disponibilidad Temporal']
        self.PeriodoAct = metadataset['Periodo de actualizacion']
        self.DesagrMax = metadataset['Nivel de Desagregacion']
        self.Notas = metadataset['Notas']
        self.NomFuente = metadataset['Fuente']
        self.UrlFuente = metadataset['URL_Fuente']

# Actualizar notas del parametro de forma manual, ya sea agregando notas o reemplazando
# las que por defecto trae el dataset.
