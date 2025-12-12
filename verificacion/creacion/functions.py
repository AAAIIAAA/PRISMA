from params import *
import pandas as pd
import pyodbc 
import os

## Conexión al TIGA
cnxn_TIGA = pyodbc.connect(CNXN_TIGA)
print("Conectando a la base de datos... ")
cnxn = pyodbc.connect(CNXN_TIGA)
cursor = cnxn.cursor()
print("Conectado.")
cursor.execute('SET LANGUAGE SPANISH')
cursor.commit()

def obtener_codigo_de_Excel(file_path):
    df = pd.read_excel(file_path)
    codigo = df['CODIGO'].iloc[-1]
    print(codigo)
    return codigo

def obtener_tipo_de_Excel(file_path):
    df = pd.read_excel(file_path)
    tipo = df['TIPO'].iloc[-1]
    negocio = df['NEGOCIO'].iloc[-1]
    print(tipo)
    return tipo,negocio

def obtener_codigo_de_Excel_informe(file_path):
    df = pd.read_excel(file_path)
    codigo = df['CODIGO'].iloc[-1]
    print(codigo)
    return codigo


def obtener_codigo_de_Excel_PEAS(file_path):
    df = pd.read_excel(file_path)
    codigo = df['CODIGO'].iloc[-1]
    print(codigo)
    return codigo

def obtener_tipo_de_Excel_informe(file_path):
    df = pd.read_excel(file_path)
    
    negocio = df['NEGOCIO'].iloc[-1]
    
    return negocio

# -------- peas----------

def obtener_proyecto_peas(file_path):
    df = pd.read_excel(file_path)
    
    codigo = df['CODIGO'].iloc[-1]
    
    return codigo

def obtener_NEGOCIO_peas(file_path):
    df = pd.read_excel(file_path)
    
    negocio = df['NEGOCIO'].iloc[-1]
    
    return negocio


def reemplazarVariablesQueries(query : str) -> str:
    file_path = os.path.join(EXCEL_PATH,"base_creacion_ppts_v2.xlsx") 
    codigo = obtener_codigo_de_Excel(file_path)
    return query.replace('%proyecto_reemplazo%', codigo)

#---------- imaganes

def reemplazarVariablesQueries2(query : str) -> str:
    file_path = os.path.join(INFORME_PATH,"informe_insertar_v2.xlsx") 
    codigo = obtener_codigo_de_Excel(file_path)
   
    return query.replace('%proyecto_reemplazo%', codigo)

#---------- peas
def reemplazarVariablesQueries3(query : str) -> str:
    file_path = os.path.join(PEAS_PATH,"base_creacion_peas_v2.xlsx") 
    codigo = obtener_codigo_de_Excel_PEAS(file_path)
   
    return query.replace('%proyecto_reemplazo%', codigo)


def obtenerDatosDe(nombre_query : str) -> pd.DataFrame:
    print(f"Extrayendo datos de {nombre_query}...")
    sql = reemplazarVariablesQueries(open(os.path.join(QUERIES_PATH, f'{nombre_query}.sql'), 'r', encoding='utf-8-sig').read())
    cursor.execute(sql)
    dataframe_resultante = pd.DataFrame.from_records(cursor.fetchall(), columns=[col[0] for col in cursor.description]).drop_duplicates()
    print("Se extrajeron " + str(len(dataframe_resultante.index)) + " filas y " + str(len(dataframe_resultante.columns)) + " columnas de " + nombre_query + ".")
    return dataframe_resultante

def obtenerDatosDe2(nombre_query: str) -> pd.DataFrame:
    print(f"Extrayendo datos de {nombre_query}...")
    sql = reemplazarVariablesQueries2(open(os.path.join(QUERIES_PATH, f'{nombre_query}.sql'), 'r', encoding='utf-8-sig').read())
   
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(f"Registros obtenidos desde la base de datos: {len(rows)}")
    dataframe_resultante = pd.DataFrame.from_records(rows, columns=[col[0] for col in cursor.description])
    print("Se extrajeron " + str(len(dataframe_resultante.index)) + " filas y " + str(len(dataframe_resultante.columns)) + " columnas de " + nombre_query + ".")
    return dataframe_resultante

def obtenerDatosDe3(nombre_query: str) -> pd.DataFrame:
    print(f"Extrayendo datos de {nombre_query}...")
    sql = reemplazarVariablesQueries3(open(os.path.join(QUERIES_PATH, f'{nombre_query}.sql'), 'r', encoding='utf-8-sig').read())
   
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(f"Registros obtenidos desde la base de datos: {len(rows)}")
    dataframe_resultante = pd.DataFrame.from_records(rows, columns=[col[0] for col in cursor.description])
    print("Se extrajeron " + str(len(dataframe_resultante.index)) + " filas y " + str(len(dataframe_resultante.columns)) + " columnas de " + nombre_query + ".")
    return dataframe_resultante


def obtenerpath2(codigo):
    codigo_final = codigo.replace(' ','')
    ruta_previa=os.path.join(MAPAYEVOLUTIVO_PATH,codigo_final)
    return os.path.join(ruta_previa,"Documentos Input")

def obtenerpath3(negocio,codigo):
   
    programado = 'PROGRAMADOS'
    anio= '2025'
    if codigo.__contains__('NPRO'):
        programado = 'NO PROGRAMADOS'
    if codigo.__contains__('2026'):
        anio = '2026'
    final =''

    if negocio == 'Pacifico Seguros':
        final = os.path.join(FINAL_PATH,"Auditoria Interna - Evaluaciones-Documentos Seguros")
    elif negocio == 'Prima AFP':
        final = os.path.join(FINAL_PATH,"Auditoria Interna - Evaluaciones-Documentos Prima AFP")
    
    elif negocio == 'Pacifico Salud':
        final = os.path.join(FINAL_PATH,"Auditoria Interna - Evaluaciones-Documentos Salud")
    
    elif negocio == 'Crediseguro':
        final = os.path.join(FINAL_PATH,"Auditoria Interna - Evaluaciones-Documentos Crediseguro")
    
    final= os.path.join(final,anio)
    final = os.path.join(final,programado)
    final = os.path.join(final,codigo)

    
    final=os.path.join(final,"Documentacion")
    print(final)
    if os.path.exists(final):
        print ("existe1")
    else:
        print ("problemas1")

    final=os.path.join(final,"PT")
    print("12")
    if os.path.exists(final):
        print ("existe1.1")
    else:
        print ("problemas1.1")
    
    return final

def obtenerpath2(codigo):
    codigo_final = codigo.replace(' ','')
    ruta_previa=os.path.join(MAPAYEVOLUTIVO_PATH,codigo_final)
    return os.path.join(ruta_previa,"Documentos Input")

def obtenerpath(tipo,negocio,codigo):
    programado = 'PROGRAMADOS'
    anio= '2025'
    if codigo.__contains__('NPRO'):
        programado = 'NO PROGRAMADOS'
    if codigo.__contains__('2026'):
        anio = '2026'

    if negocio == 'SEGUROS':
        final = os.path.join(FINAL_PATH,"Auditoria Interna - Evaluaciones-Documentos Seguros")
    elif negocio == 'PRIMA':
        final = os.path.join(FINAL_PATH,"Auditoria Interna - Evaluaciones-Documentos Prima AFP")
    
    elif negocio == 'SALUD':
        final = os.path.join(FINAL_PATH,"Auditoria Interna - Evaluaciones-Documentos Salud")
    
    elif negocio == 'CREDISEGUROS':
        final = os.path.join(FINAL_PATH,"Auditoria Interna - Evaluaciones-Documentos Crediseguro")
    
    final= os.path.join(final,anio)
    final = os.path.join(final,programado)
    final = os.path.join(final,codigo)

    if tipo=='Sprint Planning':
        final=os.path.join(final,"Documentacion")
        final=os.path.join(final,"Planificacion")
        final=os.path.join(final,"Sprint Planning.pptx")
    elif tipo=='Observaciones Borrador':
        final=os.path.join(final,"Informe Borrador")
        final=os.path.join(final,"Borrador Observaciones.pptx")
    elif tipo=='Observaciones Final':
        final=os.path.join(final,"Informe Final")
        final=os.path.join(final,"Observaciones.pptx")        
    elif tipo=='Informe Final':
        final=os.path.join(final,"Informe Final")
        final=os.path.join(final,"Informe Final.pptx")
    elif tipo=='Informe Borrador':
        final=os.path.join(final,"Informe Borrador")
        final=os.path.join(final,"Borrador Informe.pptx")
    print(final)
    
    
    return final


def wrap_label(label, max_width=12):
    words = label.split()
    lines = []
    current_line = []
    current_length = 0
    for word in words:
        if current_length + len(word) <= max_width:
            current_line.append(word)
            current_length += len(word) + 1  # +1 por el espacio
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word) + 1
    if current_line:
        lines.append(" ".join(current_line))
    return "\n".join(lines)

def procesar_dataframe_circulos(df):
    
   
    
    eje_x = {"Bajo": 0, "Moderado": 1, "Relevante": 2, "Alto": 3, "Crítico": 4}
    eje_y = {
        "EFECTIVO_NO_FORMALIZADO": 3,
        "INEFECTIVO_PRUEBA": 2,
        "INEFECTIVO_DISEÑO": 1,
        "CONTROL_INEXISTENTE": 0,
    }


    cantidades_circulos = {}

    for col in df.columns:
        
        for tipo_riesgo, x in eje_x.items():
            for tipo_control, y in eje_y.items():
                if tipo_control in col and tipo_riesgo.upper() in col and "TOTAL" not in col:
                    cantidad = df[col].iloc[0] 
                    if cantidad != "-" and int(cantidad) > 0: 
                        cantidades_circulos[(y, x)] = int(cantidad)

    cantidades_circulos_ordenado = dict(sorted(cantidades_circulos.items()))

    return cantidades_circulos_ordenado


def procesar_dataframe_simbolos(df):
   
    
    eje_x = {"Bajo": 0, "Moderado": 1, "Relevante": 2, "Alto": 3, "Crítico": 4}

    
    categorias_riesgo = {
        "Riesgo de Crédito": "#",
        "Riesgo Operacional": "▲",
        "Riesgo de Mercado": "■",
        "Riesgo Legal": "$",
        "Riesgo Estratégico": "x",
        "Riesgo de Producción/Suscripción": "◆",
    }

    
    cantidades_simbolos = {}

  
    for _, row in df.iterrows():
        
        for nivel_riesgo, x in eje_x.items():
            if f"EFECTIVOS_{nivel_riesgo.upper()}" in df.columns:
                cantidad = row[f"EFECTIVOS_{nivel_riesgo.upper()}"]
                if cantidad != "-" and int(cantidad) > 0:  
                    categoria = row["Categoría del Riesgo"]
                    if categoria in categorias_riesgo:
                       
                        key = ((4, x), categoria)
                        cantidades_simbolos[key] = cantidades_simbolos.get(key, 0) + int(cantidad)

    return cantidades_simbolos


# ============================
# MAPA DE ASEGURAMIENTO
# ============================

def read_excel_sheets(file_paths):
    data_matrix = []
    for file_path in file_paths:
        try:
            # Leer ambas hojas
            df_controles = pd.read_excel(file_path, sheet_name="Controles", engine='openpyxl')
            df_riesgos   = pd.read_excel(file_path, sheet_name="Riesgos",   engine='openpyxl')

            # Normalizar headers
            df_controles.columns = df_controles.columns.str.strip().str.upper()
            df_riesgos.columns   = df_riesgos.columns.str.strip().str.upper()

            # Renombrar columnas
            df_riesgos = df_riesgos.rename(columns={
                'CÓDIGO': 'NRO_RIESGO',
                '¿RIESGO SOX?': 'RIESGO_SOX'
            })
            df_controles = df_controles.rename(columns={
                'CÓDIGO DEL CONTROL': 'NRO_CONTROL',
                'CÓDIGO DE RIESGO': 'NRO_RIESGO',
                '¿CONTROL CLAVE?': 'CONTROL_CLAVE',
                'HERRAMIENTA - SISTEMA DE CONTROL': 'HERRAMIENTA_SISTEMA',
                'ASEVERACIONES DE LOS ESTADOS FINANCIEROS': 'ASEVERACIONES_EEFF'
            })

            # Normaliza texto clave
            for df in (df_controles, df_riesgos):
                if 'NRO_RIESGO' in df.columns:
                    df['NRO_RIESGO'] = df['NRO_RIESGO'].astype(str).str.replace('\xa0', ' ').str.strip().str.upper()
                if 'NRO_CONTROL' in df.columns:
                    df['NRO_CONTROL'] = df['NRO_CONTROL'].astype(str).str.replace('\xa0', ' ').str.strip().str.upper()
                if 'CÓDIGO DEL PROYECTO' in df.columns:
                    df['CÓDIGO DEL PROYECTO'] = df['CÓDIGO DEL PROYECTO'].astype(str).str.replace(' ', '').str.upper()

            # Merge: cada control hereda sus campos de riesgo
            merged_df = pd.merge(
                df_controles,
                df_riesgos[['NRO_RIESGO', 'TÍTULO DEL RIESGO', 'DESCRIPCIÓN', 'CATEGORÍA', 'IMPACTO', 'FRECUENCIA', 'RIESGO_SOX']],
                on='NRO_RIESGO',
                how='left'
            )

            # Cargar a la matriz
            for _, row in merged_df.iterrows():
                data_matrix.append(row.to_dict())

        except Exception as e:
            print(f"❌ Error leyendo {file_path}: {e}")

    return data_matrix


def count_and_store_excel_files(path_main, ruta_negocio):
    file_paths = []
    for negocio in ruta_negocio:
        full_path = os.path.join(path_main, negocio)
        for root, dirs, files in os.walk(full_path):
            for file in files:
                if file.endswith('_v2.xlsx'):
                    file_paths.append(os.path.join(root, file))
    return len(file_paths), file_paths


def delete_exists_asegurate_map(excel_file_paths, conexion_tiga):
    connection = pyodbc.connect(conexion_tiga)
    cursor = connection.cursor()
    procedure_name = "sp_eliminar_mapa_aseguramiento"

    for file_path in excel_file_paths:
        nombre_base = os.path.splitext(os.path.basename(file_path))[0]
        nombre_proyecto = nombre_base.replace('_v2', '')  # elimina "_v2"

        sql_query = f"EXEC {procedure_name} @NombreProyecto='{nombre_proyecto}'"
        print(f"Executing SQL Query: {sql_query}")
        cursor.execute(sql_query)

    connection.commit()
    cursor.close()
    connection.close()


def simulate_procedure_call(data_matrix, conexion_tiga):
    connection = pyodbc.connect(conexion_tiga)
    cursor = connection.cursor()
    procedure_name = "SP_Insertar_Mapa_Aseguramiento"

    def clean_value(v):
        if pd.isna(v) or v is None or str(v).strip().lower() in ['nan', 'none', '']:
            return None
        else:
            return str(v).replace("'", "''").replace("\n", " ").replace("\r", " ")

    for i, row in enumerate(data_matrix, 1):
        codigo_proyecto   = clean_value(row.get('CÓDIGO DEL PROYECTO'))
        nrocontrol        = clean_value(row.get('NRO_CONTROL'))
        nroriesgo         = clean_value(row.get('NRO_RIESGO'))
        titulo_riesgo     = clean_value(row.get('TÍTULO DEL RIESGO'))
        descripcion_riesgo= clean_value(row.get('DESCRIPCIÓN'))
        categoria         = clean_value(row.get('CATEGORÍA'))
        impacto           = clean_value(row.get('IMPACTO'))
        frecuencia        = clean_value(row.get('FRECUENCIA'))
        riesgo_sox        = clean_value(row.get('RIESGO_SOX'))
        titulo_control    = clean_value(row.get('TÍTULO DEL CONTROL'))
        descripcion_control = clean_value(row.get('DESCRIPCIÓN DEL CONTROL'))
        naturaleza        = clean_value(row.get('NATURALEZA'))
        tipo              = clean_value(row.get('TIPO'))
        evaluacion_control= clean_value(row.get('EVALUACIÓN DEL CONTROL'))
        herramienta_sistema= clean_value(row.get('HERRAMIENTA_SISTEMA'))
        control_aplicacion= clean_value(row.get('CONTROL DE APLICACIÓN'))
        cuenta_contable   = clean_value(row.get('CUENTA CONTABLE'))
        aseveraciones_eeff= clean_value(row.get('ASEVERACIONES_EEFF'))
        unidad_responsable= clean_value(row.get('UNIDAD RESPONSABLE'))
        control_clave     = clean_value(row.get('CONTROL_CLAVE'))

        sql_query = f"""
        EXEC {procedure_name}
            @Referencia_Proceso='{codigo_proyecto or ''}',
            @NroRiesgo='{nroriesgo or ''}',
            @NroControl='{nrocontrol or ''}',
            @Titulo_Riesgo='{titulo_riesgo or ''}',
            @Descripcion_Riesgo='{descripcion_riesgo or ''}',
            @Categoria='{categoria or ''}',
            @Impacto='{impacto or ''}',
            @Frecuencia='{frecuencia or ''}',
            @Riesgo_Sox='{riesgo_sox or ''}',
            @Titulo_Control='{titulo_control or ''}',
            @Descripcion_Control='{descripcion_control or ''}',
            @Naturaleza='{naturaleza or ''}',
            @Tipo='{tipo or ''}',
            @Evaluacion_Control='{evaluacion_control or ''}',
            @Herramienta_Sistema='{herramienta_sistema or ''}',
            @Control_Aplicacion='{control_aplicacion or ''}',
            @Cuenta_Contable='{cuenta_contable or ''}',
            @Aseveraciones_EEFF='{aseveraciones_eeff or ''}',
            @Unidad_Responsable='{unidad_responsable or ''}',
            @Control_Clave='{control_clave or ''}'
        """

        print(f"Ejecutando {i}/{len(data_matrix)}: {sql_query[:100]}...")
        cursor.execute(sql_query)

    connection.commit()
    cursor.close()
    connection.close()


def delete_analyzed_files(file_paths):
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Could not delete file {file_path}: {e}")


def obtenerpath_imagen(negocio, codigo, filename):
    codigo_final = codigo.replace(' ', '')
    final = os.path.join(FINAL_PATH_IMAGEN, codigo_final)
    final = os.path.join(final, "Documentos Final")
    final = os.path.join(final, filename)
    return final

## ACTUALIZAR CAMPOS EXISTENTES - MAPA ASEGURAMEINTO
'''
def count_and_store_excel_files_original(path_main, ruta_negocio):
    """
    Busca todos los archivos Excel SIN '_v2' en su nombre dentro de las rutas de negocio.
    Devuelve la cantidad y la lista de rutas completas de los archivos encontrados.
    """
    file_paths = []
    for negocio in ruta_negocio:
        full_path = os.path.join(path_main, negocio)
        for root, dirs, files in os.walk(full_path):
            for file in files:
                if file.endswith('.xlsx') and not file.endswith('_v2.xlsx'):
                    file_paths.append(os.path.join(root, file))
    return len(file_paths), file_paths

def _norm_txt(s):
    if pd.isna(s):
        return None
    return str(s).replace('\xa0', ' ').strip().upper()

def read_excel_sheets(file_paths):
    data_matrix = []
    for file_path in file_paths:
        try:
            df_controles = pd.read_excel(file_path, sheet_name="Controles", engine='openpyxl')
            df_riesgos   = pd.read_excel(file_path, sheet_name="Riesgos",   engine='openpyxl')

            # Normaliza headers
            df_controles.columns = df_controles.columns.str.strip().str.upper()
            df_riesgos.columns   = df_riesgos.columns.str.strip().str.upper()

            # Renombres
            df_riesgos = df_riesgos.rename(columns={
                'CÓDIGO': 'NRO_RIESGO',
                '¿RIESGO SOX?': 'RIESGO_SOX'
            })
            df_controles = df_controles.rename(columns={
                'CÓDIGO DEL CONTROL': 'NRO_CONTROL',
                'CÓDIGO DE RIESGO':   'NRO_RIESGO',
                '¿CONTROL CLAVE?':    'CONTROL_CLAVE',
                'HERRAMIENTA - SISTEMA DE CONTROL': 'HERRAMIENTA_SISTEMA',
                'ASEVERACIONES DE LOS ESTADOS FINANCIEROS': 'ASEVERACIONES_EEFF'
            })

            # 🔧 Normaliza VALORES clave para que el merge funcione
            for df in (df_controles, df_riesgos):
                if 'NRO_RIESGO' in df.columns:
                    df['NRO_RIESGO'] = df['NRO_RIESGO'].apply(_norm_txt)
                if 'NRO_CONTROL' in df.columns:
                    df['NRO_CONTROL'] = df['NRO_CONTROL'].apply(_norm_txt)
                if 'CÓDIGO DEL PROYECTO' in df.columns:
                    df['CÓDIGO DEL PROYECTO'] = df['CÓDIGO DEL PROYECTO'].apply(lambda x: _norm_txt(x).replace(' ', '') if not pd.isna(x) else x)

            # ✅ MERGE: cada control hereda sus datos de riesgo
            cols_riesgo = ['NRO_RIESGO','TÍTULO DEL RIESGO','DESCRIPCIÓN','CATEGORÍA','IMPACTO','FRECUENCIA','RIESGO_SOX']
            for c in cols_riesgo:
                if c not in df_riesgos.columns:
                    df_riesgos[c] = None

            merged_df = pd.merge(
                df_controles,
                df_riesgos[cols_riesgo],
                on='NRO_RIESGO',
                how='left'
            )

            # Empuja filas a la matriz
            for _, row in merged_df.iterrows():
                data_matrix.append(row.to_dict())

        except Exception as e:
            print(f"❌ Error leyendo {file_path}: {e}")

    return data_matrix
def simulate_update_call(data_matrix, conexion_tiga):
    """
    Llama al procedimiento SP_Actualizar_Mapa_Aseguramiento
    para actualizar columnas faltantes en TG_Proyecto_Riesgo_Control.
    """
    connection = pyodbc.connect(conexion_tiga)
    cursor = connection.cursor()
    procedure_name = "SP_Actualizar_Mapa_Aseguramiento"

    def clean_value(v):
        if pd.isna(v) or v is None or str(v).strip().lower() in ['nan', 'none', '']:
            return None
        else:
            return str(v).replace("'", "''").replace("\n", " ").replace("\r", " ")

    for i, row in enumerate(data_matrix, 1):
        codigo_proyecto   = clean_value(row.get('CÓDIGO DEL PROYECTO'))
        nrocontrol        = clean_value(row.get('NRO_CONTROL'))
        nroriesgo         = clean_value(row.get('NRO_RIESGO'))
        titulo_riesgo     = clean_value(row.get('TÍTULO DEL RIESGO'))
        descripcion_riesgo= clean_value(row.get('DESCRIPCIÓN'))
        categoria         = clean_value(row.get('CATEGORÍA'))
        impacto           = clean_value(row.get('IMPACTO'))
        frecuencia        = clean_value(row.get('FRECUENCIA'))
        riesgo_sox        = clean_value(row.get('RIESGO_SOX'))
        titulo_control    = clean_value(row.get('TÍTULO DEL CONTROL'))
        descripcion_control = clean_value(row.get('DESCRIPCIÓN DEL CONTROL'))
        naturaleza        = clean_value(row.get('NATURALEZA'))
        tipo              = clean_value(row.get('TIPO'))
        evaluacion_control= clean_value(row.get('EVALUACIÓN DEL CONTROL'))
        herramienta_sistema= clean_value(row.get('HERRAMIENTA_SISTEMA'))
        control_aplicacion= clean_value(row.get('CONTROL DE APLICACIÓN'))
        cuenta_contable   = clean_value(row.get('CUENTA CONTABLE'))
        aseveraciones_eeff= clean_value(row.get('ASEVERACIONES_EEFF'))
        unidad_responsable= clean_value(row.get('UNIDAD RESPONSABLE'))
        control_clave     = clean_value(row.get('CONTROL_CLAVE'))

        sql_query = f"""
        EXEC {procedure_name}
            @Referencia_Proceso='{codigo_proyecto or ''}',
            @NroRiesgo='{nroriesgo or ''}',
            @NroControl='{nrocontrol or ''}',
            @Titulo_Riesgo='{titulo_riesgo or ''}',
            @Descripcion_Riesgo='{descripcion_riesgo or ''}',
            @Categoria='{categoria or ''}',
            @Impacto='{impacto or ''}',
            @Frecuencia='{frecuencia or ''}',
            @Riesgo_Sox='{riesgo_sox or ''}',
            @Titulo_Control='{titulo_control or ''}',
            @Descripcion_Control='{descripcion_control or ''}',
            @Naturaleza='{naturaleza or ''}',
            @Tipo='{tipo or ''}',
            @Evaluacion_Control='{evaluacion_control or ''}',
            @Herramienta_Sistema='{herramienta_sistema or ''}',
            @Control_Aplicacion='{control_aplicacion or ''}',
            @Cuenta_Contable='{cuenta_contable or ''}',
            @Aseveraciones_EEFF='{aseveraciones_eeff or ''}',
            @Unidad_Responsable='{unidad_responsable or ''}',
            @Control_Clave='{control_clave or ''}'
        """
        print(f"🔄 {i}/{len(data_matrix)} | Proyecto: {codigo_proyecto} | Riesgo: {nroriesgo} | Control: {nrocontrol}")
        cursor.execute(sql_query)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Actualización completada correctamente.")
'''

        
    