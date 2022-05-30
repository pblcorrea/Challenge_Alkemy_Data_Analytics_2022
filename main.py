from database_connection import get_engine_from_settings
from database_connection import create_db_tables
from data_collection import get_data_from_url
from data_processing import get_tables
import logging 
from datetime import datetime

# Configuration of log file
now = datetime.now()
current_date = now.strftime('%d/%m/%Y')
current_time = now.strftime('%H:%M:%S')
logging.basicConfig(filename='tasker_status.log', encoding='utf-8', level=logging.DEBUG, filemode='w')
logging.info('Execution started on %s at %s.', current_date, current_time)
#creation of database connection and creation of tables
engine = get_engine_from_settings()
create_db_tables(engine)

#data processing and uploading/updating in database
get_data_from_url() 
df_unico, df_count_categ_prov, df_count_cines = get_tables()

#data to database
with engine.begin() as connection:
    df_unico.to_sql('lugar_cultural', con=connection, if_exists='replace')
    df_count_categ_prov.to_sql('totales_categoria', con=connection, if_exists='replace')
    df_count_cines.to_sql('totales_cines', con=connection, if_exists='replace')
    logging.info('Data stored in DataBase tables.')

now = datetime.now()
current_time = now.strftime('%H:%M:%S')
logging.info('Execution finished at %s.', current_time)
