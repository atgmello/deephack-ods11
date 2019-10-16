import unidecode
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import unidecode as uni

def get_default_driver(tmp_path='/tmp/cdhu'):
    """Utility function.

    Parameters
    ----------
    tmp_path : optional, string
        String pointing to the desired temporary folder in which files can
        be saved.

    Returns
    -------
    selenium.webdriver
        Webdriver with the correct options for the required functionality.
    """

    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : tmp_path}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.binary_location = '/usr/bin/chromium-browser'
#    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Enable headless downloading
    # https://github.com/TheBrainFamily/chimpy/issues/108#issuecomment-406796688
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': tmp_path}}
    command_result = driver.execute("send_command", params)

    return driver

def get_mun(driver=None):
    """Gets available 'municipios'.

    Parameters
    ----------
    driver : optional, selenium.webdriver
        The desired selenium driver.

    Returns
    -------
    array
        Array of 'municipios'.
    """
    if driver == None:
        driver = get_default_driver()

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
    options = [opt.text for opt in select.options]
    options = options[1:]
    driver.close()

    return options

def get_unidecode_dict(mun_arr):
    return dict((uni.unidecode(val), val) for val in mun_arr)
