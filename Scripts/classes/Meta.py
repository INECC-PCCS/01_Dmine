# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 11:14:28 2018

@author: carlos.arana

Objeto estándar de metadatos
"""

import pandas as pd
from AsignarDimension.AsignarDimension import AsignarDimension

class Meta(object):
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

        # Handlings
        self.ParDtype = str()
        self.TipoVar = str()
        self.array = []
        self.TipoAgr = str()

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

        # Prepara definiciones que vienen desde la fuente
        self.NomDataset = str()
        self.DescDataset = str()
        self.DispTemp = str()
        self.PeriodoAct = str()
        self.DesagrMax = str()
        self.Notas = str()
        self.NomFuente = str()
        self.UrlFuente = str()

        # Instrucciones incluidas para el compilador
        self.getmetafromds = 0       # Si es 1, el compilador jalará metadatos desde el dataset estándar.
        self.percent = 0             # Si es 1, el compilador asignará los datos del parámetro como el porcentaje de
                                     # municipios con datos.

        # Genera metadatos automáticos

    def metafromds(self):
        # Cargar metadatos del dataset
        metadataset = pd.read_excel(self.DirFuente + '\\' + self.ArchivoDataset,
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

    def fillmeta(self):
        self.ArchivoDataset = self.nomarchivodataset + "." + self.extarchivodataset
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
        if self.getmetafromds == 1:
            self.metafromds(self)
        DescIntegridad = {
            1 : 'La variable de integridad municipal para esta Dataset es binaria: \n'
                '1 =  El municipio cuenta con informacion \n0 = El municipio no cuenta con información',
            2 : 'Para calcular la variable de integridad de este dataset, se verifica la existencia de datos en '
                'cada una de las variables que se utilizaron para construir el parámetro. El valor de la variable '
                'de integridad multiplicado por 100 indica el porcentaje de variables del dataset que tienen '
                'datos para la construcción del parámetro',
            3 : 'Los datos para este parametro se agregaron desde los individuos de una poblacion, por lo que se '
                'considera que los datos están completos y que si un municipio no tiene datos significa que ese '
                'municipio tiene cero unidades de las que está considerando el parámetro',
        }
        self.DescVarIntegridad = DescIntegridad[self.TipoInt]

    def checkall(self):
        contents = {
            'name': self.name,
            'ClaveParametro': self.ClaveParametro,
            'NombreParametro': self.NombreParametro,
            'DescParam': self.DescParam,
            'UnidadesParam': self.UnidadesParam,
            'TituloParametro': self.TituloParametro,
            'PeriodoParam': self.PeriodoParam,
            'TipoInt': self.TipoInt,
            'ParDtype': self.ParDtype,
            'TipoVar': self.TipoVar,
            'nomarchivodataset': self.nomarchivodataset,
            'extarchivodataset': self.extarchivodataset,
            'ArchivoDataset': self.ArchivoDataset,
            'ContenidoHojaDatos': self.ContenidoHojaDatos,
            'ClaveDataset': self.ClaveDataset,
            'ActDatos': self.ActDatos,
            'Agregacion': self.Agregacion,
            'DescVarIntegridad': self.DescVarIntegridad,
            'DirFuente': self.DirFuente,
            'DSBase': self.DSBase,
            'ClaveDimension': self.ClaveDimension,
            'NomDimension': self.NomDimension,
            'DirDimension': self.DirDimension,
            'RepoMina': self.RepoMina,
            'DirDestino': self.DirDestino,

            'NomDataset': self.NomDataset,
            'DescDataset': self.DescDataset,
            'DispTemp': self.DispTemp,
            'PeriodoAct': self.PeriodoAct,
            'DesagrMax': self.DesagrMax,
            'Notas': self.Notas,
            'NomFuente': self.NomFuente,
            'UrlFuente': self.UrlFuente,

            'getmetafromds': self.getmetafromds,
            'NomDataset': self.NomDataset,
            'DescDataset': self.DescDataset,
            'DispTemp': self.DispTemp,
            'PeriodoAct': self.PeriodoAct,
            'DesagrMax': self.DesagrMax,
            'Notas': self.Notas,
            'NomFuente': self.NomFuente,
            'UrlFuente': self.UrlFuente,
            'ArchivoDataset': self.ArchivoDataset,
            'DirFuente': self.DirFuente,
            'DSBase': self.DSBase,
            'ClaveDimension': self.ClaveDimension,
            'NomDimension': self.NomDimension,
            'DirDimension': self.DirDimension,
            'RepoMina': self.RepoMina,
            'DirDestino': self.DirDestino,
            'DescVarIntegridad': self.DescVarIntegridad,
        }

        for k,v in contents.items():
            try:
                if v == '' or v == int():
                    print(k)
            except:
                print('{} : {}'.format(k, v))


# Actualizar notas del parametro de forma manual, ya sea agregando notas o reemplazando
# las que por defecto trae el dataset.
