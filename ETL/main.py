import os
import pyodbc
import time
import traceback

from scripts.scripts import run_etl, query_groups
from scripts.insert_ps import insertar_ps
from scripts.insert_pri import insertar_pri
from scripts.update_ps import update_ps
from scripts.update_pri import update_pri
from scripts.insert_rc_ps import insertar_ps_rc
from scripts.insert_rc_pri import insertar_pri_rc
from excepciones.excepcionesObs import excepcionesobs
from conection import *

# Mostrar los grupos de queries
for group_name, path in query_groups.items():
    queries = [f for f in os.listdir(path) if f.endswith('.sql')]
    print(f"Grupo: {group_name} - {len(queries)} queries")

# Ejecución de procesos
try:
    print("\nOBSERVACIONES")
    run_etl()
    registrar_ejecucion_TIGA('Exito Observaciones', 'Succesful')
except Exception as e:
    registrar_ejecucion_TIGA('Error Observaciones', str(e))
    print(traceback.format_exc())

# Parche: Eliminar Controles y Riesgos: Se ejecuta desde las 12am hasta 2am

'''
try:
    print("\nEjecutar Parche del ETL")
    run_etl()
    registrar_ejecucion_TIGA('Exito Parche Controles y Riesgos TMP', 'Succesful')
except Exception as e:
    registrar_ejecucion_TIGA('Error TMP', str(e))
    print(traceback.format_exc())

'''


try:
    print("\nRIESGOS Y CONTROLES INSERT PS")
    insertar_ps()
    registrar_ejecucion_TIGA('Exito R Y C insert ps', 'Succesful')
except Exception as e:
    registrar_ejecucion_TIGA('Error R Y C insert ps', str(e))
    print(traceback.format_exc())

# Comentado por obsolescencia
'''

try:
    print("\nRIESGOS Y CONTROLES INSERT PS RC")
    insertar_ps_rc()
    registrar_ejecucion_TIGA('Exito R Y C insert ps rc', 'Succesful')
except Exception as e:
    registrar_ejecucion_TIGA('Error R Y C insert ps rc', str(e))
    print(traceback.format_exc())

try:
    print("\nRIESGOS Y CONTROLES INSERT PRI RC")
    insertar_pri_rc()
    registrar_ejecucion_TIGA('Exito R Y C insert pri rc', 'Succesful')
except Exception as e:
    registrar_ejecucion_TIGA('Error R Y C insert pri rc', str(e))
    print(traceback.format_exc())
'''

try:
    print("\nRIESGOS Y CONTROLES INSERT PRI")
    insertar_pri()
    registrar_ejecucion_TIGA('Exito R Y C insert pri', 'Succesful')
except Exception as e:
    registrar_ejecucion_TIGA('Error R Y C insert pri', str(e))
    print(traceback.format_exc())

try:
    print("\nRIESGOS Y CONTROLES UPDATE PS")
    update_ps()
    registrar_ejecucion_TIGA('Exito R Y C update ps', 'Succesful')
except Exception as e:
    registrar_ejecucion_TIGA('Error R Y C update ps', str(e))
    print(traceback.format_exc())

try:
    print("\nRIESGOS Y CONTROLES UPDATE PRI")
    update_pri()
    registrar_ejecucion_TIGA('Exito R Y C update pri', 'Succesful')
except Exception as e:
    registrar_ejecucion_TIGA('Error R Y C update pri', str(e))
    print(traceback.format_exc())

# Casuística para excepciones
excepcionesobs()

print("\nFINAL")
