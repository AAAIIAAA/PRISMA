import os
import time
from conection import *

# Diccionario con los grupos de queries y sus rutas
query_groups = {
    'Pacifico Insert': QUERIES_PACIFICO_INSERT_OBSERVACIONES_PATH,
    'Pacifico Update': QUERIES_PACIFICO_UPDATE_OBSERVACIONES_PATH,
    'Prima Insert': QUERIES_PRIMA_INSERT_OBSERVACIONES_PATH,
    'Prima Update': QUERIES_PRIMA_UPDATE_OBSERVACIONES_PATH
}
'''
route_parche='..\queries\Riesgos_Controles\Auxiliares\A_Delete_TMP_Parche.sql'

def parche_etl():
'''

def run_etl():
    total_queries = sum(len(os.listdir(path)) for path in query_groups.values())
    print(f"Total de queries a ejecutar: {total_queries}")

    start_time = time.time()

    for group_name, path in query_groups.items():
        print(f"\nEjecutando grupo: {group_name}")
        queries = [f for f in os.listdir(path) if f.endswith('.sql')]

        for query in queries:
            print(f"Ejecutando {query}... ⏳")
            try:
                rows, flag = execute_query_TIGA(os.path.join(path, query))
                print("Ejecución completada.")
                print(f"Flag recibido: {flag}")
                if flag == 1:
                    print(f"{query}: {rows} filas afectadas ✔️")
                else:
                    print(f"{query}: Flag inválido o no recibido ⚠️")
                    break
            except Exception as e:
                print(f"{query}: Error ❌ - {str(e)}")

        print("-" * 30)

    elapsed_time = round(time.time() - start_time, 4)
    print(f"\nTiempo total de ejecución: {elapsed_time} segundos")
