import pandas as pd
import pyodbc
from conection import CNXN_TIGA

def leer_registros_con_pandas(nombre_archivo):
    return pd.read_csv(nombre_archivo)

def ejecutar_procedure(id_historial, conexion):
    cursor = conexion.cursor()
    try:
        cursor.execute("EXEC SP_functions_regularizar_amp ?", id_historial)
        
        while True:
            if cursor.description:
                for row in cursor:
                    print(f"ID {id_historial} → Resultado: {row[0]}")
            if not cursor.nextset():
                break
        conexion.commit()
    except Exception as e:
        print(f"Error con ID {id_historial}: {e}")
    finally:
        cursor.close()

def excepcionesobs():
    df = leer_registros_con_pandas('excepciones/excepciones-obs.csv')
    conexion = pyodbc.connect(CNXN_TIGA)

    for _, fila in df.iterrows():
        ejecutar_procedure(int(fila['ID_Historial']), conexion)

    conexion.close()

