# ETL - Transformación y Sincronización de Datos

## 📋 Descripción General

**ETL** es el **tercer paso** del sistema y el más complejo. Se ejecuta después del proceso Levantamiento y se encarga de sincronizar y transformar datos entre las bases de datos TeamMate (Prima y Pacífico) y la base de datos de integración (TIGA - PROYECTOSIAV2).

## 🎯 Objetivo

Sincronizar Observaciones, Riesgos y Controles desde las bases de datos fuente (TeamMate_Prima y TeamMateR12) hacia la base de datos consolidada TIGA, aplicando transformaciones, comparaciones y validaciones complejas.

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────┐
│  Bases de Datos Fuente                   │
│                                          │
│  ┌────────────────┐  ┌────────────────┐ │
│  │ TeamMate_Prima │  │ TeamMateR12    │ │
│  │ (Prima)        │  │ (Pacífico)     │ │
│  └────────┬───────┘  └───────┬────────┘ │
└───────────┼──────────────────┼──────────┘
            │                  │
            ▼                  ▼
┌──────────────────────────────────────────┐
│          ETL Process (main.py)           │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  1. Observaciones (run_etl)        │ │
│  │     - Insert Pacífico              │ │
│  │     - Update Pacífico              │ │
│  │     - Insert Prima                 │ │
│  │     - Update Prima                 │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  2. Riesgos y Controles            │ │
│  │     - Insert PS (Pacífico)         │ │
│  │     - Insert PRI (Prima)           │ │
│  │     - Update PS                    │ │
│  │     - Update PRI                   │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  3. Excepciones (excepcionesobs)   │ │
│  └────────────────────────────────────┘ │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│   Base de Datos Destino                  │
│   PROYECTOSIAV2 (TIGA)                   │
│                                          │
│   ├── TG_Observacion                     │
│   ├── TG_Observacion_Historial          │
│   ├── TG_Contacto                        │
│   ├── TG_Riesgos_Controles               │
│   └── Tablas auxiliares de comparación  │
└──────────────────────────────────────────┘
```

## 📂 Estructura de Archivos

```
ETL/
├── main.py                      # Orquestador principal
├── conection.py                 # Configuración de conexiones
├── executable.bat               # Ejecutable batch
├── log.txt                      # Log de ejecución
├── excepciones/
│   ├── excepciones-obs.csv      # CSV con excepciones
│   └── excepcionesObs.py        # Procesador de excepciones
├── scripts/
│   ├── scripts.py               # ETL de observaciones
│   ├── funciones.py             # Funciones auxiliares
│   ├── insert_ps.py             # Insert Riesgos/Controles Pacífico
│   ├── insert_pri.py            # Insert Riesgos/Controles Prima
│   ├── update_ps.py             # Update Riesgos/Controles Pacífico
│   └── update_pri.py            # Update Riesgos/Controles Prima
└── queries/
    ├── Backup/
    │   └── truncate.sql
    ├── Observaciones/
    │   ├── Pacifico/
    │   │   ├── insert/ (6 queries SQL)
    │   │   └── update/ (5 queries SQL)
    │   └── Prima/
    │       ├── insert/ (8 queries SQL)
    │       └── update/ (8 queries SQL)
    └── Riesgos_Controles/
        ├── Auxiliares/ (3 queries)
        ├── Pacifico/ (11 queries)
        └── Prima/ (11 queries)
```

## 🔧 Configuración de Conexiones

### Bases de Datos Conectadas

```python
# Base de datos de integración (destino)
CNXN_TIGA = (
    'Driver={ODBC Driver 17 for SQL Server};'
    'database=PROYECTOSIAV2;'
    'server=PSTMMPRD0300;'
    'uid=USTEAM02;'
    'pwd=ZU4repezaGefraMu;'
    'encrypt=no;'
)

# Base de datos TeamMate Prima (fuente)
CNXN_TEAMMATE_PRIMA = (
    'Driver={ODBC Driver 17 for SQL Server};'
    'database=TeamMate_Prima;'
    'server=PSTMMPRD0300;'
    'uid=USTEAM02;'
    'pwd=ZU4repezaGefraMu;'
    'encrypt=no;'
)

# Base de datos TeamMate Pacífico (fuente)
CNXN_TEAMMATE_PS = (
    'Driver={ODBC Driver 17 for SQL Server};'
    'database=TeamMateR12;'
    'server=PSTMMPRD0300;'
    'uid=USTEAM02;'
    'pwd=ZU4repezaGefraMu;'
    'encrypt=no;'
)
```

### Rutas de Queries

```python
# Observaciones
QUERIES_PACIFICO_INSERT_OBSERVACIONES_PATH = r'E:\Proyectos\ETL\Oficial\queries\Observaciones\Pacifico\insert'
QUERIES_PACIFICO_UPDATE_OBSERVACIONES_PATH = r'E:\Proyectos\ETL\Oficial\queries\Observaciones\Pacifico\update'
QUERIES_PRIMA_INSERT_OBSERVACIONES_PATH = r'E:\Proyectos\ETL\Oficial\queries\Observaciones\Prima\insert'
QUERIES_PRIMA_UPDATE_OBSERVACIONES_PATH = r'E:\Proyectos\ETL\Oficial\queries\Observaciones\Prima\update'

# Riesgos y Controles
QUERIES_PACIFICO_RIESGOS_CONTROLES_PATH = r'E:\Proyectos\ETL\Oficial\queries\Riesgos_Controles\Pacifico'
QUERIES_PRIMA_RIESGOS_CONTROLES_PATH = r'E:\Proyectos\ETL\Oficial\queries\Riesgos_Controles\Prima'
QUERIES_AUXILIARES_RIESGOS_CONTROLES_PATH = r'E:\Proyectos\ETL\Oficial\queries\Riesgos_Controles\Auxiliares'
```

## ⚙️ Flujo Principal (main.py)

El archivo `main.py` orquesta 7 procesos principales:

### 1. Observaciones (run_etl)

```python
try:
    print("\nOBSERVACIONES")
    run_etl()
    registrar_ejecucion_TIGA('Exito Observaciones', 'Succesful')
except Exception as e:
    registrar_ejecucion_TIGA('Error Observaciones', str(e))
    print(traceback.format_exc())
```

**Procesa 4 grupos de queries:**
- Pacífico Insert (6 queries)
- Pacífico Update (5 queries)
- Prima Insert (8 queries)
- Prima Update (8 queries)

### 2. Riesgos y Controles - Insert Pacífico

```python
try:
    print("\nRIESGOS Y CONTROLES INSERT PS")
    insertar_ps()
    registrar_ejecucion_TIGA('Exito R Y C insert ps', 'Succesful')
except Exception as e:
    registrar_ejecucion_TIGA('Error R Y C insert ps', str(e))
```

### 3. Riesgos y Controles - Insert Prima

```python
try:
    print("\nRIESGOS Y CONTROLES INSERT PRI")
    insertar_pri()
    registrar_ejecucion_TIGA('Exito R Y C insert pri', 'Succesful')
except Exception as e:
    registrar_ejecucion_TIGA('Error R Y C insert pri', str(e))
```

### 4. Riesgos y Controles - Update Pacífico

```python
try:
    print("\nRIESGOS Y CONTROLES UPDATE PS")
    update_ps()
    registrar_ejecucion_TIGA('Exito R Y C update ps', 'Succesful')
except Exception as e:
    registrar_ejecucion_TIGA('Error R Y C update ps', str(e))
```

### 5. Riesgos y Controles - Update Prima

```python
try:
    print("\nRIESGOS Y CONTROLES UPDATE PRI")
    update_pri()
    registrar_ejecucion_TIGA('Exito R Y C update pri', 'Succesful')
except Exception as e:
    registrar_ejecucion_TIGA('Error R Y C update pri', str(e))
```

### 6. Excepciones

```python
# Casuística para excepciones
excepcionesobs()
```

## 📊 Proceso: Observaciones (scripts.py)

### Función run_etl()

Ejecuta queries SQL en secuencia ordenada:

```python
query_groups = {
    'Pacifico Insert': QUERIES_PACIFICO_INSERT_OBSERVACIONES_PATH,
    'Pacifico Update': QUERIES_PACIFICO_UPDATE_OBSERVACIONES_PATH,
    'Prima Insert': QUERIES_PRIMA_INSERT_OBSERVACIONES_PATH,
    'Prima Update': QUERIES_PRIMA_UPDATE_OBSERVACIONES_PATH
}

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
                if flag == 1:
                    print(f"{query}: {rows} filas afectadas ✔️")
                else:
                    print(f"{query}: Flag inválido ⚠️")
                    break
            except Exception as e:
                print(f"{query}: Error ❌ - {str(e)}")
```

### Estructura de Queries de Observaciones

#### Pacífico Insert (6 archivos)
1. `A_TG_Observacion_i_p.sql` - Inserta observaciones principales
2. `B_TG_ALL_Observacion_i_p.sql` - Inserta todas las observaciones
3. `C_TG_Contacto_i_p.sql` - Inserta contactos
4. `D_TG_Observacion_Historial_i_p.sql` - Inserta historial
5. `E_TG_ALL_Observacion_to_compare_i_p.sql` - Tabla de comparación ALL
6. `F_TG_Observacion_to_compare_i_p.sql` - Tabla de comparación

#### Prima Insert (8 archivos)
1. `A_TG_Observacion_i_pr.sql` - Inserta observaciones principales
2. `B_TG_ALL_Observacion_i_pr.sql` - Inserta todas las observaciones
3. `C_TG_Observacion_otros_i_pr.sql` - Observaciones otros
4. `D_TG_Observacion_Historial_i_pr.sql` - Historial
5. `E_TG_Contacto_i_pr.sql` - Contactos
6. `F_TG_Observacion_to_compare_i_pr.sql` - Comparación
7. `G_TG_Observacion_otros_to_compare_i_pr.sql` - Comparación otros
8. `H_TG_ALL_Observacion_to_compare_i_pr.sql` - Comparación ALL

## 📊 Proceso: Riesgos y Controles

### Insert Pacífico (insert_ps.py)

Este proceso lee datos de TeamMateR12 (Pacífico) y genera una matriz compleja de riesgos y controles:

```python
columnas_insert = [
    "Identificador", "Referencia_del_Proceso", "Descripción del Proceso",
    "N° Riesgo", "Causa", "Evento", "Consecuencia",
    "Categoría del Riesgo", "Tipo de Riesgo",
    "Impacto", "Impacto (en US$ miles)", "Frecuencia",
    "N° Control", "Descripción del Control",
    "Control_Clave", "Control_Sox", "Control Regulatorio",
    "Evaluación del Control", "Ponderado del Control",
    # ... 85 columnas en total
]
```

#### Flujo de Procesamiento

1. **Lee cambios pendientes**:
```python
ds1 = obtener_query_TIGA(os.path.join(
    QUERIES_PACIFICO_RIESGOS_CONTROLES_PATH, 
    'Cambios_insert.sql'
))
```

2. **Procesa cada registro**:
```python
for idx, rd in ds1.iterrows():
    # Extrae Causa, Evento, Consecuencia
    matriz.at[i, "Causa"] = causa_evento_consecuencia(rd["Descripcion"], "Causa")
    matriz.at[i, "Evento"] = causa_evento_consecuencia(rd["Descripcion"], "Evento")
    matriz.at[i, "Consecuencia"] = causa_evento_consecuencia(rd["Descripcion"], "Consecuencia")
    
    # Obtiene categoría del riesgo
    if not pd.isnull(rd["UserCategory1CID"]):
        temp = categoría_ps(rd["UserCategory1CID"])
        matriz.at[i, "Categoría del Riesgo"] = cat_riesgo(temp, "Categoría")
        matriz.at[i, "Tipo de Riesgo"] = cat_riesgo(temp, "Tipo")
```

3. **Calcula métricas de riesgo**:
```python
# Query dinámica para obtener modificaciones de Impacto
temp = open(os.path.join(QUERIES_PACIFICO_RIESGOS_CONTROLES_PATH, 
            'PS_CCModificaciones.sql'), 'r').read()
temp = temp.replace("'ValorPR'", str(rd["ID Proyecto"]))
           .replace("'ValorR'", str(rd["ID Riesgo"]))
           .replace("'ValorC'", str(rd["ID Control"]))

ds5 = obtener_query_tiga(temp)

if not ds5.empty:
    matriz.at[i, "Impacto (en US$ miles)"] = ds5.iloc[0, 9]
    matriz.at[i, "Impacto"] = cálculo_editar_ps(
        matriz.at[i, "Impacto (en US$ miles)"], "Impacto"
    )
```

### Update Pacífico (update_ps.py)

Actualiza registros existentes basándose en cambios detectados:

```python
def update_ps():
    ds1 = obtener_query_TIGA(os.path.join(
        QUERIES_PACIFICO_RIESGOS_CONTROLES_PATH, 
        'Cambios_update.sql'
    ))
    
    for idx, rd in ds1.iterrows():
        # Construye query UPDATE dinámica
        # Actualiza solo los campos que cambiaron
```

### Insert/Update Prima (insert_pri.py, update_pri.py)

Similar a Pacífico pero con queries específicas para TeamMate_Prima.

## 📋 Excepciones (excepcionesObs.py)

Maneja casos especiales de observaciones que requieren tratamiento manual:

```python
def excepcionesobs():
    # Lee CSV con excepciones configuradas
    df_excepciones = pd.read_csv('excepciones/excepciones-obs.csv')
    
    # Aplica reglas especiales
    for idx, row in df_excepciones.iterrows():
        # Procesa cada excepción
        ...
```

## 🔍 Funciones Auxiliares Clave (funciones.py)

### causa_evento_consecuencia()
Extrae partes de la descripción del riesgo:
```python
def causa_evento_consecuencia(descripcion, tipo):
    # Busca patrones: "Causa: ... Evento: ... Consecuencia: ..."
    # Retorna la sección solicitada
```

### cat_riesgo()
Clasifica categorías y tipos de riesgo:
```python
def cat_riesgo(valor, tipo):
    # Mapea códigos de categoría a nombres
    # Retorna categoría o tipo según parámetro
```

### cálculo_editar_ps()
Calcula valores de impacto y frecuencia:
```python
def cálculo_editar_ps(valor, tipo):
    # Convierte valores cuantitativos a cualitativos
    # Ejemplo: 5000 USD -> "Alto"
```

## 🔌 Funciones de Conexión (conection.py)

### execute_query_TIGA()
Ejecuta query en base de datos TIGA con captura de flag:
```python
def execute_query_TIGA(query_path):
    query = open(query_path, encoding='utf-8').read()
    cursor = cnxn_TIGA.cursor()
    cursor.execute('SET LANGUAGE SPANISH')
    cursor.execute(query)
    
    rows_affected = cursor.rowcount
    flag = None
    
    # Busca SELECT 1 AS flag en result sets
    while True:
        if cursor.description:
            result = cursor.fetchone()
            if result:
                flag = result[0]
                break
        if not cursor.nextset():
            break
    
    cursor.commit()
    return rows_affected, flag
```

### obtener_query_TIGA()
Ejecuta query y retorna DataFrame:
```python
def obtener_query_TIGA(query_path):
    query = open(query_path, encoding='utf-8').read()
    return pd.read_sql(query, cnxn_TIGA)
```

## 🚀 Ejecución

### Manual
```bash
python main.py
```

### Via Batch
```batch
executable.bat
```

### Automatizada
Se ejecuta diariamente después del proceso **Levantamiento** mediante tarea programada.

## 📈 Características Técnicas

### Manejo de Errores
- Try-catch individual por cada proceso
- Logging detallado de errores
- Registro en base de datos con `registrar_ejecucion_TIGA()`
- Continúa con siguiente proceso aunque uno falle

### Transaccionalidad
- Commits después de cada query exitosa
- Rollback automático en caso de error
- Flags de validación (SELECT 1 AS flag)

### Performance
- Queries optimizadas con índices
- Procesamiento en lotes
- Ejecución secuencial controlada

## ⏱️ Tiempo de Ejecución

**Total aproximado: 15-25 minutos**
- Observaciones: 5-8 minutos
- Riesgos y Controles Insert: 3-5 minutos cada uno
- Riesgos y Controles Update: 2-4 minutos cada uno
- Excepciones: 1-2 minutos

## 📊 Tablas Destino Principales

### PROYECTOSIAV2 (TIGA)

**Observaciones:**
- `TG_Observacion` - Observaciones principales
- `TG_ALL_Observacion` - Todas las observaciones
- `TG_Observacion_otros` - Observaciones especiales
- `TG_Observacion_Historial` - Historial de cambios
- `TG_Contacto` - Contactos relacionados
- `TG_Observacion_to_compare` - Tabla de comparación

**Riesgos y Controles:**
- `TG_Riesgos_Controles` - Matriz principal
- `TG_TMP` - Tabla temporal de trabajo
- `TG_RC` - Riesgos y controles procesados

## 🛠️ Dependencias

```python
import os
import pyodbc         # Conexión SQL Server
import pandas as pd   # Procesamiento de datos
import time           # Medición de tiempos
import traceback      # Manejo de errores
from datetime import datetime
```

### Instalación
```bash
pip install pyodbc pandas sqlalchemy
```

## ⚠️ Consideraciones Importantes

1. **Orden de Ejecución**: Respetar el orden de procesos en main.py
2. **Dependencias de Datos**: Levantamiento debe completarse antes
3. **Conexiones Múltiples**: Maneja 3 bases de datos simultáneamente
4. **Validación de Flags**: Queries deben retornar SELECT 1 AS flag al finalizar
5. **Manejo de Nulos**: Validación exhaustiva de campos NULL
6. **Encoding**: Todos los archivos SQL deben estar en UTF-8

## 🔗 Integración

### Entrada
- Datos cargados por **Levantamiento**
- TeamMate_Prima (fuente)
- TeamMateR12 (fuente)

### Salida
- Base de datos TIGA actualizada
- Lista para consumo por **scripts_produccion**

## 📞 Contacto y Soporte

Para consultas sobre este módulo, contactar al equipo de Analítica e Innovación en Auditoría.

---

**Última actualización**: Diciembre 2025  
**Versión**: 1.0  
**Autor**: Equipo Analítica e Innovación - Pacífico Seguros
