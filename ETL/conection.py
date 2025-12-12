
import pyodbc
import re
import pandas as pd
from sqlalchemy import create_engine
import urllib

QUERIES_PACIFICO_INSERT_OBSERVACIONES_PATH = r'E:\Proyectos\ETL\Oficial\queries\Observaciones\Pacifico\insert'
QUERIES_PACIFICO_UPDATE_OBSERVACIONES_PATH = r'E:\Proyectos\ETL\Oficial\queries\Observaciones\Pacifico\update'
QUERIES_PRIMA_INSERT_OBSERVACIONES_PATH = r'E:\Proyectos\ETL\Oficial\queries\Observaciones\Prima\insert'
QUERIES_PRIMA_UPDATE_OBSERVACIONES_PATH = r'E:\Proyectos\ETL\Oficial\queries\Observaciones\Prima\update'
QUERIES_BACKUP_PATH = r'E:\Sharepoint\Pacífico Compañía de Seguros y Reaseguros\Analítica e Innovación en Auditoría - 01. Resultados Scripts\backup_prima'
QUERIES_TRUNCATE_PATH = r'E:\Proyectos\ETL\Oficial\queries\backup'


QUERIES_PACIFICO_RIESGOS_CONTROLES_PATH = r'E:\Proyectos\ETL\Oficial\queries\Riesgos_Controles\Pacifico'
QUERIES_PRIMA_RIESGOS_CONTROLES_PATH = r'E:\Proyectos\ETL\Oficial\queries\Riesgos_Controles\Prima'
QUERIES_AUXILIARES_RIESGOS_CONTROLES_PATH = r'E:\Proyectos\ETL\Oficial\queries\Riesgos_Controles\Auxiliares'


CNXN_TIGA = r'Driver={ODBC Driver 17 for SQL Server};database=PROYECTOSIAV2;encrypt=no;integrated security=False;min_tls=1.0;port=1433;server=PSTMMPRD0300;trusted_connection=no;uid=USTEAM02;pwd=ZU4repezaGefraMu'
CNXN_TEAMMATE_PRIMA = r'Driver={ODBC Driver 17 for SQL Server};database=TeamMate_Prima;encrypt=no;integrated security=False;min_tls=1.0;port=1433;server=PSTMMPRD0300;trusted_connection=no;uid=USTEAM02;pwd=ZU4repezaGefraMu'
CNXN_TEAMMATE_PS = r'Driver={ODBC Driver 17 for SQL Server};database=TeamMateR12;encrypt=no;integrated security=False;min_tls=1.0;port=1433;server=PSTMMPRD0300;trusted_connection=no;uid=USTEAM02;pwd=ZU4repezaGefraMu'


cnxn_TIGA = pyodbc.connect(CNXN_TIGA)
cnxn_TEAMMATE_PRIMA = pyodbc.connect(CNXN_TEAMMATE_PRIMA)
cnxn_TEAMMATE_PS = pyodbc.connect(CNXN_TEAMMATE_PS)

def execute_query_TIGA(query_path):
    query = open(query_path, encoding='utf-8').read()
    cursor = cnxn_TIGA.cursor()
    cursor.execute('SET LANGUAGE SPANISH')
    cursor.execute(query)

    # Captura de filas afectadas por el INSERT
    rows_affected = cursor.rowcount

    # Inicializamos el flag como None
    flag = None

    # Exploramos todos los result sets hasta hallar uno con columnas (el SELECT 1 AS flag)
    while True:
        if cursor.description:  # Esto significa que este result set es de un SELECT
            result = cursor.fetchone()
            if result:
                flag = result[0]
                break
        if not cursor.nextset():
            break

    cursor.commit()
    return rows_affected, flag

def execute_query_TEAMMATE_Prima(query_path):
    query = open(query_path, encoding='utf-8', mode='r').read()
    cursor = cnxn_TEAMMATE_PRIMA.cursor()
     
    try:
        cursor.execute(query)
        cursor.commit()
        print('El script se ejecutó con éxito.')
    except Exception as e:
        print(f'Error al ejecutar el script: {e}')
    return cursor.rowcount

def execute_query_TEAMMATE_Prima_backup(query_path):
    with open(query_path, encoding='utf-8', mode='r') as f:
        queries = re.split(r';\s*(?=(INSERT|UPDATE))', f.read())

    cursor = cnxn_TEAMMATE_PRIMA.cursor()
    rowcount = 0

    for query in queries:
        query = query.strip() 
        if query: 
            try:
                cursor.execute(query)
                cursor.commit()
                rowcount += cursor.rowcount
                
            except Exception as e:
                print("error")
                

    return rowcount


def execute_query_TEAMMATE_ps(query_path):
    query = open(query_path, encoding='utf-8', mode='r').read()
    cursor = cnxn_TEAMMATE_PS.cursor()
    
    cursor.execute(query)
    cursor.commit()
    return cursor.rowcount



def obtener_query_TIGA(query_path):
    query = open(query_path, encoding='utf-8', mode='r').read()
    cursor = cnxn_TIGA.cursor()
    cursor.execute('SET LANGUAGE SPANISH')
    cursor.execute(query)
    results = cursor.fetchall()
    results = [[value if value is not None else 'N/A' for value in row] for row in results]

    columns = [column[0] for column in cursor.description]

    df = pd.DataFrame(results, columns=columns)

    return df


def registrar_ejecucion_TIGA(estado, descripcion):
    cursor = cnxn_TIGA.cursor()
    cursor.execute('SET LANGUAGE SPANISH')
    
    from datetime import datetime
    fecha_hora = datetime.now()
      
    query = """
    INSERT INTO TG_ETL_Log (Estado, FechaEjecucion, Descripcion)
    VALUES (?, ?, ?)
    """  
    cursor.execute(query, (estado, fecha_hora, descripcion))

    cnxn_TIGA.commit()



def obtener_query_teammate_ps(query):
    params = urllib.parse.quote_plus('Driver={ODBC Driver 17 for SQL Server};database=TeamMateR12;encrypt=no;integrated security=False;min_tls=1.0;port=1433;server=PSTMMPRD0300;trusted_connection=no;uid=USTEAM02;pwd=ZU4repezaGefraMu')
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(params))

    df = pd.read_sql(query, engine)

    return df

def obtener_query_teammate_pri(query):
    params = urllib.parse.quote_plus('Driver={ODBC Driver 17 for SQL Server};database=TeamMate_Prima;encrypt=no;integrated security=False;min_tls=1.0;port=1433;server=PSTMMPRD0300;trusted_connection=no;uid=USTEAM02;pwd=ZU4repezaGefraMu')
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(params))

    df = pd.read_sql(query, engine)

    return df

def obtener_query_tiga(query):
    params = urllib.parse.quote_plus('Driver={ODBC Driver 17 for SQL Server};database=PROYECTOSIAV2;encrypt=no;integrated security=False;min_tls=1.0;port=1433;server=PSTMMPRD0300;trusted_connection=no;uid=USTEAM02;pwd=ZU4repezaGefraMu')
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(params))

    df = pd.read_sql(query, engine)

    return df







