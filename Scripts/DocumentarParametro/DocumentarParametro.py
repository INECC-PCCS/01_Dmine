# -*- coding: utf-8 -*-
"""
Started on Wed Sep  6 15:48:51 2017

@author: carlos.arana

Descripcion:
Script para documentar un parámetro. Al final del proceso de minería, el script:

* Crea un archivo README.md para la carpeta del parámetro
* Crea un archivo .txt para la última actualización del parámetro
* Guarda el parámetro y su informacion de integridad en la hoja integradora de parámetros

"""

# Librerias utilizadas
import pandas as pd
import datetime

# Descripciones, fuentes y destinos
def DocumentarParametro(DescParametro, MetaParametro, Parametro):
    # Desempacar Información
    ClaveParam = DescParametro['ClaveParametro']
    NombreParam = DescParametro['NombreParametro']
    DescParam = MetaParametro.loc['Descripcion del dataset'][0]
    DirDestino = '{}\{}'.format(DescParametro['RutaSalida'], DescParametro['ClaveParametro'])
    NomDimension = DescParametro['Nombre de Dimension']
    TituloParam = DescParametro['Titulo de Columna']
    ActDatos = DescParametro['Actualizacion de datos']
    Socavon = MetaParametro.loc['Dataset base'][0]

    # Crear README.md
    IDNOMParametro = '{} - {}'.format(ClaveParam, NombreParam)
    Titulo = '# Parametro {}\n\n'.format(IDNOMParametro)
    Encabezado = 'Archivo de mineria de datos. Parametro: {}\n\n'.format(IDNOMParametro)
    Descripcion = '**Contenido**: {}\n\n'.format(DescParam)
    Fuente = '**FUENTE**: {}\n\n'.format(MetaParametro.loc['Fuente'][0])
    Mina = '**Dataset Base**: {}\n\n'.format(Socavon)
    INECC = '**Instituto Nacional de Ecología y Cambio Climático**\n\n'
    PNUD = '**Programa de las Naciones Unidas para el Desarrollo**\n\n'
    PCCS = '**Plataforma de Conocimiento de Ciudades Sustentables**\n\n'
    actualizacion = datetime.datetime.today().strftime('**Ultima revision del parametro**: %Y/%m/%d \n\n')
    act_datos = '**Ultima Actualizacion de los datos**: {}\n\n'.format(ActDatos)
    Cierre = '{}{}----------\n\n{}{}{}'.format(actualizacion, act_datos, INECC, PNUD, PCCS)
    Glosa = '{}{}{}{}{}{}'.format(Titulo, Encabezado, Descripcion, Fuente, Mina, Cierre)
    Destino = '{}\README.md'.format(DirDestino)
    with open(Destino, 'w') as README:
        README.write(Glosa)

    # Cargar archivo integrador
    RutaIntegrador = r'D:\PCCS\01_Dmine\00_Generales\CatalogoParametros.xlsx'
    HojaIndice = pd.read_excel(RutaIntegrador, sheetname='INDICE', index_col=0)
    HojaParametros = pd.read_excel(RutaIntegrador, sheetname='PARAMETROS', dtype={'CVE_SUN' : str})
    HojaIntegridad = pd.read_excel(RutaIntegrador, sheetname='INTEGRIDAD', dtype={'CVE_SUN' : str})
    HojaParametros.set_index('CVE_SUN', inplace=True)
    HojaIntegridad.set_index('CVE_SUN', inplace=True)

    # Crear nueva entrada en Indice
    DatosIndice = pd.DataFrame(index=[DescParametro['ClaveParametro']],
                               data={
                                    'NOM_PARAMETRO': NombreParam,
                                    'ARCHIVO_LOCAL': DirDestino+r'\{}.xlsx'.format(ClaveParam),
                                    'URL_MINERIA': MetaParametro.loc['Repositorio de mineria'][0]
                                })
    HojaIndice.loc[DatosIndice.iloc[0].name] = DatosIndice.iloc[0]   # Escribe la entrada en el indice

    # Integrar datos de parámetro e integridad
    HojaParametros[ClaveParam] = Parametro[ClaveParam]
    HojaIntegridad[DescParametro['ClaveIntegridad']] = Parametro[DescParametro['ClaveIntegridad']]

    # Ordenar la informacion
    HojaIndice.sort_index(axis=0, inplace=True)
    HojaParametros.sort_index(axis=1, inplace=True)
    HojaIntegridad.sort_index(axis=1, inplace=True)

    # Escribir archivo .xlsx
    writer = pd.ExcelWriter(RutaIntegrador)
    HojaIndice.to_excel(writer, sheet_name='INDICE')
    HojaParametros.to_excel(writer, sheet_name='PARAMETROS')
    HojaIntegridad.to_excel(writer, sheet_name='INTEGRIDAD')

    print('Se ha actualizado el Catálogo de Parámetros en {}'.format(RutaIntegrador))
    writer.save()
