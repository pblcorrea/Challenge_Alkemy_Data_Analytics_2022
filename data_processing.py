import pandas as pd
import numpy as np
from datetime import date

#Reading of the local .csv files using the file_path file created in the data_collection process.
with open('file_paths.txt','r') as f:
    file_paths = f.readlines()

df_museos = pd.read_csv(file_paths[0].strip())
df_cines = pd.read_csv(file_paths[1].strip())
df_bibliotecas = pd.read_csv(file_paths[2].strip())

#Normalization of the columns 
df_bibliotecas = df_bibliotecas.rename(columns={'Cod_Loc': 'Cod_Localidad',
                                                'Teléfono': 'Telefono'})
                                                
df_cines = df_cines.rename(columns={'Cod_Loc': 'Cod_Localidad', 
                                    'Dirección': 'Domicilio', 
                                    'Teléfono': 'Telefono'})

df_museos = df_museos.rename(columns={'Cod_Loc': 'Cod_Localidad',
                                      'categoria': 'Categoría',
                                      'provincia': 'Provincia',
                                      'localidad': 'Localidad',
                                      'nombre': 'Nombre',
                                      'direccion': 'Domicilio', 
                                      'telefono': 'Telefono'})

#Replacing missing data with null values
df_bibliotecas.replace('s/d', np.NaN, inplace=True)
df_cines.replace('s/d', np.NaN, inplace=True)
df_museos.replace('s/d', np.NaN, inplace=True)

#Table 1
#Assembling of the unique table
df_unico = pd.concat([df_bibliotecas, df_cines, df_museos], ignore_index=True)
df_unico.drop(df_unico.columns.difference(['Cod_Localidad', 'IdProvincia', 'IdDepartamento', 'Categoría', 'Provincia', 'Localidad', 'Nombre', 'Domicilio', 'CP', 'Telefono', 'Mail', 'Web']), axis=1, inplace=True)

#Adding a new column with the current updating date
today =     today = date.today().strftime("%d-%m-%Y")
df_unico['Fecha_carga'] = today

#Table 2
df_count_categ_prov = df_unico.pivot_table(values='Cod_Localidad', index=['Provincia'], columns=['Categoría'], aggfunc='count', margins=True, fill_value=0)
df_count_categ_prov.reset_index(inplace=True)
df_count_categ_prov['Fecha_carga'] = today

#Table 3
df_cines.espacio_INCAA.replace({'SI': 1,
                                'si': 1,
                                '0': 0,
                                np.nan: 0}, inplace=True)
df_count_cines = df_cines.groupby(['Provincia'])[['Pantallas', 'Butacas', 'espacio_INCAA']].sum().reset_index()
df_count_cines['Fecha_carga'] = today

#------------------
def get_tables():
    '''
    Returns the processed tables 
    '''
    return df_unico, df_count_categ_prov, df_count_cines
