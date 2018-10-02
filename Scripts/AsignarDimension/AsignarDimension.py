# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 10:00:29 2017

@author: carlos.arana
Descripcion: Diccionario con claves y nombres de dimensiones.
Entradas:
ClaveDimension: str (2 digitos) - clave de 2 d+igitos de la dimensiónm
dimension[ClaveDimension]: dict (2 keys) - Nombre de directorio y Nombre de dimensión.
Salidas:

"""

def AsignarDimension(ClaveDimension):
    dimension = {
        '00': {'directorio': 'Generales', 'nombre': 'Generales'},
        '01': {'directorio': 'Agua', 'nombre': 'Agua'},
        '02': {'directorio': 'Aire', 'nombre': 'Aire'},
        '03': {'directorio': 'UsoDeSuelo', 'nombre': 'Uso de Suelo'},
        '04': {'directorio': 'Edificaciones', 'nombre': 'Edificaciones'},
        '05': {'directorio': 'Industria', 'nombre': 'Industria'},
        '06': {'directorio': 'Energia', 'nombre': 'Energía'},
        '07': {'directorio': 'Movilidad', 'nombre': 'Movilidad'},
        '08': {'directorio': 'Habitabilidad', 'nombre': 'Habitabilidad'},
        '09': {'directorio': 'BienesAmbientalesYServiciosPublicos',
               'nombre': 'Bienes Ambientales y Servicios Públicos'},
        '10': {'directorio': 'ResiduosSolidosUrbanos', 'nombre': 'Residuos Sólidos Urbanos'},
        '99': {'directorio': 'Descentralizacion', 'nombre': 'Descentralizacion'},
    }
    return dimension[ClaveDimension]

