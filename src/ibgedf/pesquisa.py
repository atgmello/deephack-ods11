import requests as rq
import pandas as pd
import sys
import re
from pandas.io.json import json_normalize
from . import utils
from .utils import *

def filter_by_municipio(s):
    """Function for filtering 'pesquisas' related to 'municipios'

    This function can be applyed to a pandas dataframe in order to generate a
    True/False list. This list, in turn, can be used for filtering the rows from
    this given dataframe. Refer to filter_pesquisa.

    Parameters
    ----------
    s : string
        Binary representation of where the 'pesquisa' has been applyed

    Returns
    -------
    bool
        Whether the binary is related to 'municipio'
    """

    re_municipio = re.compile(r"(0|1)*1(1|0)\b")
    if s:
        return True if re_municipio.match(s) else False
    else:
        return False

def filter_pesquisa(df, by):
    """Function for filtering 'pesquisas' based on where it's been applyed

    Refer to filter_municipio.

    Parameters
    ----------
    df : DataFrame
        Original DataFrame
    by : string
        Where the 'pesquisa' has been applyed. Only 'municipio' available for
        now

    Returns
    -------
    DataFrame
        Filtered DataFrame
    """

    if by == 'municipio':
        filter_by = df['contexto'].apply(filter_by_municipio)
    else:
        raise Exception("Bad value for keyword 'key'")
    return df[filter_by].reset_index(drop=True)

def get_pes_mun():
    """Helper function.

    Parameters
    ----------

    Returns
    -------
    DataFrame
        DataFrame for all 'pesquisas' related to 'municipios'
    """

    url = 'https://servicodados.ibge.gov.br/api/v1/pesquisas'
    df_pes = get_df_from_endpoint(url)
    df_pes_mun = filter_pesquisa(df_pes, by='municipio')
    return df_pes_mun

def expand_res(df, columns=['ano','valor','id','localidade']):
    df_un = pd.DataFrame(columns=columns)
    for index,row in df.iterrows():
        for k,v in row['res'].items():
            '''
            Em alguns casos, ano é um range, e.g. '2010-2014'
            Se esse for o caso, é preciso quebrar a string e
            adicionar uma linha para cada ano no intervalo
            '''
            if len(k) > 4:
                for k_n in range(int(k[:4]),int(k[5:])):
                    data = [k_n,None,row.loc['id'],row.loc['localidade']]
                    new_row = pd.DataFrame([data], columns=columns)
                    df_un = df_un.append(new_row)
            else:
                data = [k,v,row.loc['id'],row.loc['localidade']]
                new_row = pd.DataFrame([data], columns=columns)
                df_un = df_un.append(new_row)

    df = df.merge(df_un, on=['id','localidade']).drop(columns='res')
    return df


def unnest_ind(df, drop='fonte'):
    """Returns an unnested dataframe with respect to the 'children' col
    for the 'indicadores' of a 'pesquisa'

    Parameters
    ----------
    df : DataFrame
        Orininal dataframe containing nested children data
    drop : array or string, optional
        Columns to be dropped by the end of the processing;
        By default, drops 'fonte'

    Returns
    -------
    DataFrame
        The processed DataFrame
    """

    df_all = df.copy()

    while df_all['children'].isna().sum() < len(df_all):
        for i in range(len(df_all)):
            try:
                children_df = pd.concat([json_normalize(x) for x in df_all.loc[i,'children']],
                            ignore_index=True, sort=False)
                df_all = df_all.append(children_df, sort=False).reset_index(drop=True)
            except  Exception as e:
                pass
            finally:
                df_all.loc[i,'children'] = None
        df_all = df_all.reset_index(drop=True)

    df_all = df_all.drop(columns='children')

    if drop:
        try:
            df_all = df_all.drop(columns=drop)
        except:
            pass

    return df_all

def get_unnested_ind(pes, drop='fonte'):
    """Helper function.

    Returns unnested DataFrame with 'indicadores' for given 'pesquisa'

    Parameters
    ----------
    pes : string
        String composed of one or more 'pesquisa' identifiers, separated by |
        (pipe)

    Returns
    -------
    DataFrame
        The processed DataFrame
    """

    url = 'https://servicodados.ibge.gov.br/api/v1/pesquisas/{}/indicadores/0'
    df = get_df_from_endpoint(url, [pes])
    df = unnest_ind(df, drop=drop)
    return df

def get_expanded_res(pes,loc):
    """Helper function.

    Returns expanded DataFrame with 'resultados' for given 'pesquisa'
    and 'localidade'

    Parameters
    ----------
    pes : string
        String composed of one or more 'pesquisa' identifiers, separated by |
        (pipe)
    loc : string
        String composed of one or more 'localidade' identifiers, separated by |
        (pipe)

    Returns
    -------
    DataFrame
        The processed DataFrame
    """

    url = 'https://servicodados.ibge.gov.br/api/v1/pesquisas/{}/resultados/{}'
    df = get_df_from_endpoint(url,[pes,loc],normalize=True)
    df = expand_res(df)
    return df

def get_denorm_res_ind(pes,loc):
    """Helper function.

    Returns merged DataFrame created from the expanded 'resultados'
    (for given 'pesquisa' and 'localidade') and unnested 'indicadores'
    (for given 'pesquisa')


    Parameters
    ----------
    pes : string
        String composed of one or more 'pesquisa' identifiers, separated by |
        (pipe)
    loc : string
        String composed of one or more 'localidade' identifiers, separated by |
        (pipe)

    Returns
    -------
    DataFrame
        The processed DataFrame
    """

    df_ind = get_unnested_ind(pes)
    df_res = get_expanded_res(pes,loc)
    df_res = df_res.merge(df_ind, sort=False)
    return df_res
