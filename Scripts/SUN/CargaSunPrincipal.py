# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 11:33:18 2017

@author: carlos.arana

Descripcion: Carga el dataset de ciudades del Sistema Urbano Nacional que se encuentran en el subsistema principal
"""
import pandas as pd

def getsun():
    # Cargar archivo del Subsistema Principal del SUN
    sun = pd.read_csv(r'D:\PCCS\01_Dmine\00_Generales\sun_main.csv',
                      dtype={'CVE_SUN': str,
                             'CVE_ENT': str,
                             'CVE_MUN': str,
                             'CVE_LOC': str,
                             'CVE_SUNMUN': str},
                      encoding='UTF-8',
                      )
    sun['CVE_SUN'] = sun['CVE_SUN'].apply('{:0>3}'.format)
    sun['CVE_ENT'] = sun['CVE_ENT'].apply('{:0>2}'.format)
    sun['CVE_MUN'] = sun['CVE_MUN'].apply('{:0>5}'.format)
    return sun
