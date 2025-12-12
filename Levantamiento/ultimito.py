import os
import re
import time
import pyodbc
import pandas as pd
from datetime import datetime

# -----------------------------------
# Configuración de conexión y rutas
# -----------------------------------
CNXN_STR = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=PSTMMPRD0300;"
    "Database=TeamMate_Prima;"
    "UID=USTEAM02;"
    "PWD=ZU4repezaGefraMu;"
    "Encrypt=no;"
)
CSV_DIR = r'E:\Sharepoint\Pacífico Compañía de Seguros y Reaseguros\Analítica e Innovación en Auditoría - 01. Resultados Scripts\backup_prima_csv'
QUERIES_DIR = r'E:\Proyectos\ETL\Levantamiento\queries'
CHUNKSIZE = 10000  # filas por lote

# -----------------------------------
# Tablas en orden de carga
# -----------------------------------
GROUP1 = [
    'TM_RecommendationAction', 'TM_Recommendation', 'TM_Schedule',
    'TM_Issue', 'TM_Project', 'TM_CategoryValue',
    'TM_SecurityGroup', 'TM_Auditor', 'TM_User'
]
GROUP2 = ['TM_ObjectAction']
GROUP3 = [
    'EWP_Control', 'EWP_EntityToRisk', 'EWP_Project', 'EWP_RiskToControl',
    'EWP_Risk', 'TM_AuthRecommendation', 'TM_Browser', 'TM_Link',
    'TM_List_AuthRecRole', 'TM_List_ProjectStatus', 'TM_List_RecActionType',
    'TM_List_RecommendationStatus', 'TM_Procedure', 'TM_Program',
    'TM_ProjectToOrgHierarchy', 'TM_SecurityGroupToUser'
]

# Scripts SQL a ejecutar antes y después
PRE_SQL_SCRIPTS  = ['drop_object_action.sql', 'truncate.sql']
POST_SQL_SCRIPTS = ['object_action.sql']

# -----------------------------------
# Funciones auxiliares
# -----------------------------------
def split_sql_batches(script: str) -> list:
    """Divide un script SQL en batches separados por líneas 'GO'."""
    return [
        b.strip() for b in re.split(r"^GO\s*(?:\r\n?|\n)", script,
                                   flags=re.IGNORECASE|re.MULTILINE)
        if b.strip()
    ]

def run_sql_scripts(cursor, scripts: list):
    """Ejecuta cada archivo SQL (pre/post) en orden, batch por batch."""
    for fname in scripts:
        path = os.path.join(QUERIES_DIR, fname)
        print(f"Ejecutando script SQL: {fname}")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        for batch in split_sql_batches(content):
            cursor.execute(batch)
        cursor.commit()
    print("Scripts SQL ejecutados.\n")

# -----------------------------------
# Carga de tabla con validaciones
# -----------------------------------
def load_table_from_csv(cursor, cnxn, table: str):
    csv_path = os.path.join(CSV_DIR, f"{table}.csv")
    print(f"---- Cargando tabla {table} ----")
    if not os.path.exists(csv_path):
        print(f"ERROR: CSV no encontrado: {csv_path}")
        return

    # 1) Leer metadata incluyendo IS_NULLABLE
    cursor.execute("""
        SELECT COLUMN_NAME, DATA_TYPE, NUMERIC_PRECISION, NUMERIC_SCALE, IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME=?
        ORDER BY ORDINAL_POSITION
    """, table)
    cols_info = cursor.fetchall()
    cols = [c for c, *_ in cols_info]
    col_list = ", ".join(f"[{c}]" for c in cols)
    placeholders = ", ".join("?" for _ in cols)
    insert_sql = f"INSERT INTO dbo.{table} ({col_list}) VALUES ({placeholders})"

    # 2) Activar IDENTITY_INSERT si corresponde
    cursor.execute("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME=?
          AND COLUMNPROPERTY(
            object_id(TABLE_SCHEMA + '.' + TABLE_NAME),
            COLUMN_NAME, 'IsIdentity'
          ) = 1
    """, table)
    identity = cursor.fetchone()
    if identity:
        cursor.execute(f"SET IDENTITY_INSERT dbo.{table} ON")
        cnxn.commit()
        print(f"IDENTITY_INSERT ON para {table}")

    text_types = {'char','nchar','varchar','nvarchar','text','ntext'}
    int_types  = {'tinyint','smallint','int','bigint'}

    # 3) Leer e insertar por chunks
    total_inserted = 0
    for idx, chunk in enumerate(
        pd.read_csv(csv_path, encoding='utf-8-sig', chunksize=CHUNKSIZE),
        start=1
    ):
        # 3a) Rellenar nulos en texto NOT NULL
        for col, dtype, *_ in cols_info:
            if dtype in text_types:
                # remplaza cadenas vacías o NaN con marcador
                chunk[col] = chunk[col].fillna('<NULL>')

        # 3b) Validar nulos en INT NOT NULL
        bad_int = []
        for col, dtype, *_ in cols_info:
            if dtype in int_types:
                is_nullable = next(x for x in cols_info if x[0]==col)[4]
                if is_nullable == 'NO':
                    nuls = int(chunk[col].isna().sum())
                    if nuls > 0:
                        bad_int.append((col, nuls))
        if bad_int:
            msgs = "; ".join(f"{c} tiene {cnt} nulos" for c, cnt in bad_int)
            raise RuntimeError(f"Error chunk {idx}: INT NOT NULL con nulos -> {msgs}")

        # 3c) Construir filas para inserción
        rows = []
        for _, series in chunk.iterrows():
            row = []
            for col, dtype, *_ in cols_info:
                val = series[col]
                if pd.isna(val):
                    row.append(None)
                elif dtype in int_types:
                    row.append(int(val))
                elif dtype in ('decimal','numeric','float','real','money','smallmoney'):
                    row.append(float(val))
                elif 'date' in dtype or 'time' in dtype:
                    try:
                        # evitar overflow
                        dt = pd.to_datetime(val)
                        row.append(dt.to_pydatetime())
                    except Exception:
                        row.append(None)
                else:
                    row.append(str(val))
            rows.append(row)

        # 3d) Insertar batch, con fallback fila a fila
        try:
            cursor.fast_executemany = True
            cursor.executemany(insert_sql, rows)
            cnxn.commit()
            print(f"  Chunk {idx}: insertadas {len(rows)} filas")
            total_inserted += len(rows)
        except Exception as batch_err:
            print(f"⚠️ Batch {idx} fallo: {batch_err}. Probando fila a fila...")
            for r_idx, row in enumerate(rows, start=1):
                try:
                    cursor.execute(insert_sql, row)
                    cnxn.commit()
                    total_inserted += 1
                except Exception as row_err:
                    print(f"  🚫 chunk {idx}, fila {r_idx} error: {row_err}")
                    print(f"    Valores: {row}")
                    raise

    # 4) Desactivar IDENTITY_INSERT
    if identity:
        cursor.execute(f"SET IDENTITY_INSERT dbo.{table} OFF")
        cnxn.commit()
        print(f"IDENTITY_INSERT OFF para {table}")

    print(f"✔️ Total filas insertadas en {table}: {total_inserted}\n")


# -----------------------------------
# Main
# -----------------------------------
if __name__ == '__main__':
    print("Conectando a SQL Server...")
    cnxn = pyodbc.connect(CNXN_STR)
    cursor = cnxn.cursor()
    start = time.time()

    # Pre-carga: drop y truncate
    run_sql_scripts(cursor, PRE_SQL_SCRIPTS)

    # Grupo 1
    for tbl in GROUP1:
        load_table_from_csv(cursor, cnxn, tbl)

    # Post-carga: recreate ObjectAction
    run_sql_scripts(cursor, POST_SQL_SCRIPTS)

    # Grupo 2 + 3
    for tbl in GROUP2 + GROUP3:
        load_table_from_csv(cursor, cnxn, tbl)

    elapsed = time.time() - start
    print(f"\n🎉 Proceso completo en {elapsed:.2f} segundos.")

    cursor.close()
    cnxn.close()