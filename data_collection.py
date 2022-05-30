import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import os
import logging

def get_data_from_url():
    '''
    Collects the data from the 3 url's, downloads it in local directories
    and saves a local file with their local paths.
    '''

    URL_ARG_MUSEOS = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_4207def0-2ff7-41d5-9095-d42ae8207a5d'
    URL_ARG_SALAS_CINES = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_392ce1a8-ef11-4776-b280-6f1c7fae16ae'
    URL_ARG_BIBLIOTECAS = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_01c6c048-dbeb-44e0-8efa-6944f73715d7'

    try: 
        res_museos = requests.get(URL_ARG_MUSEOS)
        logging.info('%s HTTP Request Status code: %s', 'ARG_MUSEOS', res_museos.status_code)
        res_cines = requests.get(URL_ARG_SALAS_CINES)
        logging.info('%s HTTP Request Status code: %s', 'ARG_SALAS_CINES', res_cines.status_code)
        res_bibliotecas = requests.get(URL_ARG_BIBLIOTECAS)
        logging.info('%s HTTP Request Status code: %s', 'ARG_BIBLIOTECAS', res_bibliotecas.status_code)
        res_list = [res_museos, res_cines, res_bibliotecas]
    except Exception as err:
        logging.error('Data from URL Error: %s', err)

    local_file_paths = []

    for res in res_list:
        link_csv, local_file_path, file_name_csv = extract_file_path(res)
        download_file(link_csv, local_file_path, file_name_csv)
        local_file_paths.append(f'{local_file_path}\{file_name_csv}')

    #Write and save the local file paths to the .csv files to be readed in the data processing file
    with open('file_paths.txt','w') as f:
        for path in local_file_paths: 
            f.write(f'{path}\n')



def extract_file_path(res):
    '''
    Extraction of the .csv url from a given the html response (res).
    It uses the BeautifulSoup library to find the csv url by scraping the html
    and to extracts the date of its last update.
    
    Returns 3 strings 
    link_csv: url of the .csv file
    local_file_path: local directory to download the file
    file_name_csv: name of the local file to be created
    '''
    html = BeautifulSoup(res.text, 'html.parser')
    link_csv = html.find(href=re.compile(".csv"))['href']
    last_update = html.find(text=re.compile('ltimo cambio'))
    last_update_date = last_update.find_next('div')
    full_date = last_update_date.text.strip().split(' ')
    year_update = full_date[-1]
    month_update = full_date[-3]


    file_name_aux= link_csv.split('/')
    file_name = file_name_aux[-1].split('.')[0]

    today = date.today().strftime("%d-%m-%Y")

    local_file_path = f'.\{file_name}\{year_update}-{month_update}'

    file_name_csv = f'{file_name}-{today}.csv'

    return link_csv, local_file_path, file_name_csv


def remove_old_files():
    '''
    Remove files from current directory
    '''
    old_files = os.listdir()    
    if bool(old_files):
        for old_file in old_files:
            os.remove(old_file)


def download_file(link_csv, local_file_path, file_name_csv):
    '''
    Makes the request to a .csv file and download its data to a local .csv file
    in the specified directory. 
    It also removes old files with older versions of the data.
    
    Parameters 
    link_csv: url of the .csv file
    local_file_path: local directory to download the file
    file_name_csv: name of the local file to be created 
    '''
    if not os.path.exists(local_file_path):
        os.makedirs(local_file_path)

    os.chdir(local_file_path)
    
    try:
        response = requests.get(link_csv, allow_redirects=True)
        #deleting old downloaded csv files versions
        remove_old_files()
        encoding_format = response.encoding 
        with open(file_name_csv, 'w', encoding=encoding_format) as f:
         f.write(response.text)
         logging.info('Data file %s saved in %s.', file_name_csv, local_file_path)
    except requests.exceptions.HTTPError as errh:
        logging.error("HTTP Error: %s", errh)
    except requests.exceptions.ConnectionError as errc:
        logging.error("Connection Error: %s", errc)
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error: %s", errt)
    except requests.exceptions.RequestException as err:
        logging.error("Error: %s", err)


    os.chdir('..\..')


