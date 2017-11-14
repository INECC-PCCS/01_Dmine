def cargahoja(entidad, ruta, colnames):
    # Abre el archivo de excel
    raw_data = pd.read_excel(ruta,
                              sheetname='02',
                              skiprows=7).dropna()
    # renombra las columnas
    raw_data.columns = colnames

    # Obten Unicamente las filas con valores estimativos
    raw_data = raw_data[raw_data['Estimador'] == 'Valor']

    # Crea la columna CVE_MUN
    raw_data['CVE_ENT'] = entidad
    raw_data['ID_MUN'] = raw_data.Municipio.str.split(' ', n=1).apply(lambda x: x[0])
    raw_data['CVE_MUN'] = raw_data['CVE_ENT'].map(str) + raw_data['ID_MUN']

    # Borra columnas con informacion irrelevante
    del (raw_data['CVE_ENT'])
    del (raw_data['ID_MUN'])
    del (raw_data['Entidad federativa'])
    del (raw_data['Estimador'])
    raw_data.set_index('CVE_MUN', inplace=True)
    return raw_data


dictionario = {
    '01' : {'01':'A', '02':'B'},
    '02' : {'03':'C', '04':'D'},
    '03' : {'05':'E', '06':'F'}
}

dictionario['01']['01']

'01' not in dictionario.keys()