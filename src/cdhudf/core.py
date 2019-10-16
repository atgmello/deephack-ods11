import os
import shutil
from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
from .utils import *

def preproc_df(df, agg=True, mun_col=False):
    try:
        df.drop(columns='Unnamed: 11', inplace=True)
    except:
        pass
    try:
        df.drop(columns='Unnamed: 0', inplace=True)
    except:
        pass

    df.columns = [c.strip() for c in df.columns]
    df.drop(index=(len(df)-1), inplace=True)

    df['Data de Entrega'] = pd.to_datetime(df['Data de Entrega'])
    df['Total de UHS'] = pd.to_numeric(df['Total de UHS'])
    df['Total de CCs'] = pd.to_numeric(df['Total de CCs'])
    df["Total de Fam (Urb)"] = pd.to_numeric(df["Total de Fam (Urb)"])

    if agg:
        df.insert(3, 'Ano de Entrega', df['Data de Entrega'].dt.year)
        df.insert(4, 'Mês de Entrega', df['Data de Entrega'].dt.month)

        df = df.sort_values(by='Ano de Entrega').reset_index(drop=True)
        df['Acumulado Total de UHS'] = df['Total de UHS'].cumsum()
        df['Acumulado Total de CCs'] = df['Total de CCs'].cumsum()
        df["Acumulado Total de Fam (Urb)"] = df["Total de Fam (Urb)"].cumsum()

        if mun_col:
            mun_dict = get_unidecode_dict(get_mun())
            def municipio(s):
                mun = s.split()[0].capitalize()
                i = 1
                while mun not in list(mun_dict.keys()) and i < len(mun):
                    mun = " ".join(s.split()[:i]).title()
                    i+=1

                return mun_dict[mun]

            df.insert(0, 'Município', df['Empreendimento'].apply(municipio))

    return df


def get_df(municipio='all', driver=None, tmp_path = '/tmp/cdhu', verbose=True):
    """
    Clean tmp dir for downloading files
    """
    try:
        os.mkdir(tmp_path)
    except OSError as oserr:
        print ("Creation of the directory {} failed".format(tmp_path))
        print(oserr)

    if driver == None:
        driver = get_default_driver(tmp_path)

    print('Acessando site...') if verbose else False
    url = 'http://www.cdhu.sp.gov.br/web/guest/producao-habitacional/consultar-producao-habitacional'
    try:
        driver.get(url)
        driver.implicitly_wait(15)
    except Exception as e:
        print(e)
        driver.quit()

    id_municipio_dropdown = driver.\
                find_element_by_id('_ProducaoHabitacional_WAR_ProducaoHabitacional_:form:municipio')
    select = Select(id_municipio_dropdown)

    today = date.today()
    date_ini = driver.find_element_by_id('dataini')
    date_end = driver.find_element_by_id('datafim')

    date_ini.send_keys("01/01/1986")
    date_end.send_keys(today.strftime("%d/%m/%Y"))

    print('Coletando dados de {}...'.format(municipio)) if verbose else False

    try:
        select.select_by_value(municipio)
    except Exception as e:
        print(e)
        return pd.DataFrame()

    search_button = driver.find_element_by_id('_ProducaoHabitacional_WAR_ProducaoHabitacional_:form:btPesquisar')
    search_button.click()

    before = [f for f in os.listdir(tmp_path)]

    try:
        print('Fazendo download de arquivos...')
        download_csv = driver.find_element_by_id(
              "_ResultadoProducaoHabitacional_WAR_ProducaoHabitacional_:formEntregas:exportarXLSX")

        # TODO - fix weird click behavior?
        download_csv.click()
        download_csv.click()
    except:
        print('Tentando novamente...')
        download_csv = driver.find_element_by_id(
              "_ResultadoProducaoHabitacional_WAR_ProducaoHabitacional_:formEntregas:exportarXLSX")
        download_csv.click()
    finally:
        print('Tentando novamente...')
        download_csv = driver.find_element_by_id(
              "_ResultadoProducaoHabitacional_WAR_ProducaoHabitacional_:formEntregas:exportarXLSX")
        download_csv.click()

    stop = 0
    while stop < 20:
        sleep (1)
        after = [f for f in os.listdir(tmp_path)]
        if before != after:
            break
        stop+=1

    filename = max([os.path.join(tmp_path,f) for f in os.listdir(tmp_path)], key=os.path.getctime)
    df = pd.read_csv(filename, sep=';', encoding='latin1')

    # Drops last row, just simple aggregated data
    df.drop(index=(len(df)-1), inplace=True)

    driver.quit()
    try:
        shutil.rmtree(tmp_path)
    except Exception as e:
        print(e)

    return df
