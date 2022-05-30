# Challenge Alchemy de Data Analytics con Python

## Objetivo
Creación de un proyecto que consume datos desde 3 fuentes distintas para popular una base de datos SQL con información cultural sobre bibliotecas, museos y salas de cines argentinos.


##  Instrucciones de ejecución

#### 1. Creación de entorno virtual e instalación de paquetes
Ejecutar los siguientes comandos en una terminal:

* Crear entorno virtual `python -m venv venv` o `py -m venv env` dentro de la carpeta del proyecto. 
* Activar el entorno `\venv\Scripts\activate.bat` (en cmd Shell Windows) o `venv\Scripts\Activate.ps1` (en PowerShell Windows) o `source venv/bin/activate` (en Bash Shell Linux).
* Instalar paquetes dentro del entorno virtual desde el archivo 
```
pip install -r requirements.txt
```

#### 2.  Conexión Base de Datos: Creación de archivo de configuración local

EL proyecto requiere guardar datos en una base de datos local. Para ello, 
se debe tener instalado [PostgreSQL](https://www.postgresql.org/). Luego: 

* Crear un archivo de variables de entorno local con el nombre `.env` en la carpeta del proyecto. 

* El archivo debe contener las siguientes variables con las credenciales de acceso a la base de datos PostgreSQL:
```
PGUSER = <USUARIO> (por defecto: postgres)
PGPASSWD = <YOUR_PASSWORD>
PGHOST = <HOST> (por defecto: localhost)
PGPORT = <PUERTO> (por defecto: 5432)
PGDB = <DATA_BASE_NAME> (puede o no existir)
```


## Ejecución del proyecto

Ejecutar el archivo `main.py`. 

El programa consume los datos de las 3 fuentes, los guarda en la carpeta de trabajo en 3 rutas distintas, los procesa y los guarda en la base de datos especificada. La primera vez que se ejecute creará la base de datos (si no existe) y tablas necesarias en PostgreSQL. Se genera un archivo `tasker_status.log` con el registro de eventos. 

 Para **actualizar** la base de datos por posibles actualizaciones de las 3 fuentes, ejecutar nuevamente `main.py`.

 ## Archivos del proyecto

* `main.py` es el script de ejecución del proyecto.
* `database_connection.py` contiene funciones para la creación de la base de datos, su conexión y creación de tablas a partir de un script .sql
* `data_collection.py` contiene funciones para buscar los datos a partir de las 3 fuentes (3 URL's), extraerlos y descargarlos en la carpeta del proyecto (las rutas relativas se almacenan en un archivo nuevo llamado `file_paths.txt`). 
* `data_processing.py` lee los archivos de datos guardados y los procesa con la librería Pandas para generar 3 dataframes que luego serán almacenados en la base de datos en `main.py`.
* `tables.sql` contiene los scripts para la creación de 3 tablas. 
