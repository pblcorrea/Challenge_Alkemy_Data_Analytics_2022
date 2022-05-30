from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import text
from sqlalchemy import inspect
from decouple import config
import logging

def get_engine(user, passwd, host, port, db):
    '''
    Connection to the local DataBase using the connection settings 
    given as function parameters.
    Returns the storage engine.
    '''
    url = f'postgresql://{user}:{passwd}@{host}:{port}/{db}'
    if not database_exists(url):
        create_database(url)
        logging.info('DataBase successfully created.')

    engine = create_engine(url, pool_size=50, echo=False)
    logging.info('DataBase engine created.')
    return engine

def get_engine_from_settings():
    '''
    Obtains the DataBase engine using the get_engine function and
    the local setting of the DataBase saved in .env
    ''' 
    try:
        settings_file = '.env'
        file = open(settings_file, 'r')
        file.close()
    except FileNotFoundError as err:
        logging.error("File %s Not Found: %s", settings_file, err)

    return get_engine(config('PGUSER'),
                    config('PGPASSWD'),
                    config('PGHOST'),
                    config('PGPORT'),
                    config('PGDB')
                    )
 
def create_db_tables(engine):
    '''
    Creates of tables in the database. Checks if the tables allready exist.
     Uses the sql script from tables.sql
    '''
    if not inspect(engine).has_table("lugar_cultural"):
        TABLE_CREATION= 'tables.sql'
        with engine.connect() as con:
            with open(TABLE_CREATION) as file:
                query = text(file.read())
                con.execute(query)
                logging.info('Tables successfully created in DataBase.')

 
