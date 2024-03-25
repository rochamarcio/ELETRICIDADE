import pandas as pd
import numpy as np
import warnings
import datetime as dt
warnings.filterwarnings('ignore')

def preprocessing():

    df = pd.read_table('../data/household_power_consumption.txt', sep=";")
    # renomear colunas com títulos mais intuitivos e traduzidos
    df.columns = ['Data','Tempo','Potencia_ativa_total','Potencia_reativa_total','Tensao','Corrente_Total','Sub_area_cozinha','Sub_area_lavanderia','Sub_area_Aq_Ar']
    # configurar o pandas para não dgerar saídas por notação científica e sim float com duas casas decimais
    pd.set_option('display.float_format', '{:.2f}'.format)
    # configurar o pandas para mostrar todas as colunas sem corte
    pd.set_option('display.max_columns',None)

    df.dropna(axis=0, how='all')

    # Verificar se cada célula contém '?', inicialmente foi gerado erro na tentativa de converter objeto em número. explicação do erro apresentou a string "?"
    erro = df.applymap(lambda x: '?' in str(x))
    # Iterar sobre as colunas com '?' e substituir '?' por NaN e converter para float
    for coluna in erro.columns:
        if erro[coluna].any():
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
            
    # Lista de colunas e seus respectivos formatos de data/tempo
    colunas_formatos = {'Data': '%d/%m/%Y', 'Tempo': '%H:%M:%S'}
    # Iterar sobre as colunas e formatos
    for coluna, formato in colunas_formatos.items():
        df[coluna] = pd.to_datetime(df[coluna], format=formato)
        
    df.dropna(how='any' , inplace=True, axis=0)

    col_ind = ['Data','Tempo','Corrente_Total']
    df.insert(2, 'Ano', df['Data'].dt.year)
    df.insert(3, 'Trimestre', df['Data'].dt.quarter)
    df.insert(4, 'Periodo', df['Tempo'].apply(lambda x: 'Dia' if 6 <= x.hour < 18 else ('Noite' if 18 <= x.hour < 24 else 'Madrugada')))
    df.drop(columns=col_ind, inplace=True)
    return df

