import requests as rq
import pandas as pd
from pandas.io.json import json_normalize

def get_df_from_endpoint(url, args=[], normalize=False, drop='notas'):
    """Returns a dataframe from given endpoint

    Parameters
    ----------
    url : str
        URL for the endpoint
    args : array, optional
        By default, 'args' is an empty array. For those endpoints which
        parameters are required, you must place them in this argument
        in the same order as they would appear in the URL
    normalize : bool, optional
        Whether the returned json should be normalized or not (default is False)
    drop : string, optional
        Column names to be droped. By default tries dropping 'notas'

    Returns
    -------
    DataFrame
        The DataFrame created from the json response string
    """

    r = rq.get(url.format(*args))
    if r.status_code == 200:
        if normalize:
            df = json_normalize(r.json(),['res'], meta=['id'])

            try:
                df = df.drop(columns=drop)
            except:
                pass

        else:
            df = pd.DataFrame(r.json())
        return df
    else:
        raise Exception('Bad Request for url\t{}'.format(url.format(*args)))

def get_mun_dict(estado, key='id'):
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    df_loc = get_df_from_endpoint(url)

    # Check arg
    if estado not in df_loc['nome'].unique():
        raise Exception("Bad value for keyword for 'estado'. Expected a valid state name, got '{}'.".format(estado))

    id_estado = df_loc[df_loc['nome'] == estado]['id'].values[0]

    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{}/municipios'
    df_mun = get_df_from_endpoint(url, [id_estado])

    mun_dict = get_dict(df_mun, key=key)

    return mun_dict

def get_dict(df, key='id'):
    # Check arg
    if key != 'nome' and key != 'id':
        raise Exception("Bad value for keyword 'key'. Expected 'id' or 'nome', got '{}'.".format(key))

    if key == 'id':
        d = dict([df.loc[i,'id'], df.loc[i,'nome']] for i in range(len(df)))
    else:
        d = dict([df.loc[i,'nome'], df.loc[i,'id']] for i in range(len(df)))
    return d
