import pyodbc
import csv
import os
import glob
import datetime
import time

CNXN_TIGA = (
    r'Driver={ODBC Driver 17 for SQL Server};'
    r'Server=C35T01WPDB01;'
    r'Database=TeamMate_Prima;'
    r'UID=TeamMateUser_Prima2023;'
    r'PWD=audteammateprima2023!;'
    r'Encrypt=no;'
)
BACKUP_DIR = r'D:\Sharepoint\Pacífico Compañía de Seguros y Reaseguros\Analítica e Innovación en Auditoría - 01. Resultados Scripts\backup_prima_csv'
TABLES = [
    'TM_Recommendation', 'TM_RecommendationAction', 'TM_Issue', 'TM_Schedule',
    'TM_Project', 'TM_CategoryValue', 'TM_SecurityGroup', 'TM_Auditor', 'TM_User',
    'TM_SecurityGroupToUser', 'TM_Program', 'TM_ProjectToOrgHierarchy',
    'TM_Procedure', 'TM_List_RecommendationStatus', 'TM_List_RecActionType',
    'TM_List_ProjectStatus', 'TM_List_AuthRecRole', 'TM_Link', 'EWP_RiskToControl',
    'TM_Browser', 'EWP_Risk', 'EWP_Project', 'EWP_EntityToRisk', 'EWP_Control',
    'TM_AuthRecommendation', 'TM_ObjectAction'
]


os.makedirs(BACKUP_DIR, exist_ok=True)

for f in glob.glob(os.path.join(BACKUP_DIR, '*.csv')):
    os.remove(f)


print("Conectando a SQL Server...")
cnxn = pyodbc.connect(CNXN_TIGA)
cursor = cnxn.cursor()


start_time = time.time()
for tabla in TABLES:
    print(f"Exportando tabla {tabla}...")
    
    cursor.execute(
        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME=? "
        "ORDER BY ORDINAL_POSITION", tabla
    )
    columnas = [row[0] for row in cursor.fetchall()]

    csv_path = os.path.join(BACKUP_DIR, f"{tabla}.csv")
 
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(
            csvfile,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_ALL,
            lineterminator='\n'
        )
       
        writer.writerow(columnas)

        
        select_sql = f"SELECT {', '.join(f'[{c}]' for c in columnas)} FROM dbo.{tabla}"
        cursor.execute(select_sql)
        while True:
            rows = cursor.fetchmany(10000)
            if not rows:
                break
           
            str_rows = []
            for row in rows:
                str_row = []
                for val in row:
                    if val is None:
                        str_row.append('')
                    elif isinstance(val, datetime.datetime):
                        str_row.append(val.strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        str_row.append(str(val))
                str_rows.append(str_row)
            writer.writerows(str_rows)

    print(f"? {tabla}.csv creado: {os.path.getsize(csv_path):,} bytes")

elapsed = time.time() - start_time
print(f"\nExportación completada en {elapsed:.2f} segundos.")


db_close = getattr(cursor, 'close', None)
if db_close: cursor.close()
cnxn.close()
