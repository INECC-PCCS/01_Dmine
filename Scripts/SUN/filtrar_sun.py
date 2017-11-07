# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 13:40:49 2017

@author: carlos.arana

Descripcion:
Tomando como base un dataset indexado con CVE_MUN, elimina del dataset todos los registros que no corresponden a
municipios dentro del Subsistema Principal del SUN, dejando un dataset que incluye únicamente los municipios que se
encuentran dentro del subsistema principal.

"""

import pandas as pd
module_path = r'D:\PCCS\01_Dmine\Scripts'
if module_path not in sys.path:
    sys.path.append(module_path)
from SUN.CargaSunPrincipal import getsun
from SUN.asignar_sun import asignar_sun

def filtrar_sun(dataset):
    sun = getsun()
    return dataset

