# Scripts Producción - Generación de Reportes y Fuentes de Datos

## 📋 Descripción General

**scripts_produccion** es el **cuarto paso** del sistema ETL y el módulo de generación de salidas. Se ejecuta después del proceso ETL y tiene como objetivo generar todos los reportes, dashboards, fuentes de datos para PowerApps y archivos Excel que consumen los diferentes stakeholders de la organización.

## 🎯 Objetivo

Transformar los datos consolidados en TIGA en múltiples fuentes de información estructurada para:
- Dashboards de Power BI
- PowerApps (Auditron, Consultas, PEAS, Auditados)
- Reportes Excel especializados
- Anexos y validaciones de calidad

## 🏗️ Arquitectura

```
┌──────────────────────────────────────┐
│   Base de Datos TIGA                 │
│   (PROYECTOSIAV2)                    │
│   └── Datos consolidados ETL         │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│   PY001_ScriptsInnovacion            │
│   (main.py)                          │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Apps.py                       │ │
│  │  - AppsAuditron()              │ │
│  │  - AppsRegistroPruebas()       │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Dashboards.py                 │ │
│  │  - DashboardsInnovacion()      │ │
│  │  - ValidacionCarpetas()        │ │
│  │  - calidad_carpetas()          │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Rpas.py (Deshabilitado)       │ │
│  │  - RPAC03, RPAC04, etc.        │ │
│  └────────────────────────────────┘ │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│   Archivos de Salida                 │
│                                      │
│   ├── CSVs para Power BI             │
│   ├── Excel para PowerApps           │
│   ├── Excel para Validaciones        │
│   └── Logs y reportes                │
└──────────────────────────────────────┘
```

## 📂 Estructura de Archivos

```
scripts_produccion/
└── PY001_ScriptsInnovacion/
    ├── main.py                 # Orquestador principal
    ├── fuentes.py              # Carga de dataframes desde queries
    ├── functions.py            # Funciones auxiliares
    ├── params.py               # Parámetros y rutas
    ├── utils.py                # Utilidades generales
    ├── pdf.py                  # Generación de PDFs
    ├── calidad_carpetas_stefano.py  # Validación de carpetas
    ├── executable.bat          # Ejecutable
    ├── queries/                # 60+ archivos SQL
    │   ├── Anexo12.sql
    │   ├── AuditorEvaluacion.sql
    │   ├── BaseUniverso.sql
    │   ├── StockObservaciones.sql
    │   ├── HistorialObservaciones.sql
    │   ├── MapaAseguramientoBI.sql
    │   ├── RiesgosControles.sql
    │   ├── EfectividadControles.sql
    │   └── ... (57+ queries más)
    └── scripts/
        ├── Apps.py             # Generación fuentes PowerApps
        ├── Dashboards.py       # Generación fuentes Dashboards
        ├── Rpas.py             # RPAs (Deshabilitado)
        └── EncuestasB1B2/      # Módulo de encuestas
            ├── EncuestasB1_B2.py
            └── mainEncuesta.py
```

## 🔧 Configuración (params.py)

### Rutas de Salida

```python
# Power BI - Dashboards
OUTPUT_PATH_PBI = r'E:\Sharepoint\...\POWER BI'

# PowerApps
OUTPUT_PATH_APP = r'E:\Sharepoint\...\Apps'
OUTPUT_PATH_AUDITRON = r'E:\Sharepoint\...\Auditron'
OUTPUT_PATH_APP_PEAS = r'E:\Sharepoint\...\PEAS'
OUTPUT_PATH_AUDITADOS = r'E:\Sharepoint\...\Auditados'

# Generación de Informes
OUTPUT_PATH_GEN_INFORME = r'E:\Sharepoint\...\01. Resultados Scripts'

# Calidad y Validaciones
OUTPUT_PATH_CALIDAD = r'E:\Sharepoint\...\Calidad'

# Documentación de Proyectos
RUTA_DOCUMENTACION_PROYECTOS = r'E:\Sharepoint\...\Documentación Proyectos'
```

### Rutas de Carpetas por Negocio

```python
RUTAS_CARPETAS_PS = [
    r'E:\Sharepoint\...\Pacífico',
    # ... múltiples carpetas
]

RUTAS_CARPETAS_PRIMA = [
    r'E:\Sharepoint\...\Prima AFP',
    # ...
]

RUTAS_CARPETAS_CREDISEGURO = [...]
RUTAS_CARPETAS_SALUD = [...]
```

## ⚙️ Flujo Principal (main.py)

El proceso principal ejecuta módulos en secuencia con manejo de errores individual:

### 1. Apps Auditron

```python
try:
    error_en = "Apps Auditron"
    AppsAuditron()
except Exception as e:
    print("Error en", error_en)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_lines = ''.join(traceback.format_exception(...))
    
    # Escribir log de error si es producción
    if env == "AIA_Produccion":
        exception_filename = f"{project_name[:5]}_{datetime}.txt"
        with open(os.path.join(exceptions_route, exception_filename), 'w') as f:
            f.write(error_lines)
```

### 2. Dashboards Innovación

```python
try:
    error_en = "Dashboards Innovación"
    DashboardsInnovacion()
except Exception as e:
    # Manejo de errores...
```

### 3. Validación Carpetas

```python
try:
    error_en = "Validacion Carpetas"
    ValidacionCarpetas()
except Exception as e:
    # Manejo de errores...
```

### 4. Calidad de Carpetas

```python
try:
    error_en = "Calidad carpetas"
    calidad_carpetas()
except Exception as e:
    # Manejo de errores...
```

### 5. RPAs (Comentado)

```python
# Estos módulos están deshabilitados:
# RPAC03(), RPAC04(), RPAC05(), RPAC07(), RPAC19()
# AppsRegistroPruebasAnaliticas()
# mainExcel() # Encuestas B1B2
```

## 📊 Módulo: Apps.py

Genera fuentes de datos para PowerApps y aplicaciones web.

### AppsAuditron()

Genera archivos Excel para la aplicación Auditron:

```python
def AppsAuditron():
    eliminar_fuentes_anexo_12()
    
    # Diccionario de dataframes a exportar
    dataframes_anexo12 = {
        "Proyectos_con_Anexo12": df_TieneAnexo12,
        "Matriz_Calificacion_Conteo": df_MatrizCalificacionConteo,
        "Matriz_Calificacion": df_matrizCalificacion,
        "Matriz_Pruebas": df_MatrizPruebas,
        "Programa_Trabajo_Credicorp": df_programaTrabajoCredicorp
    }
    
    for nombre_hoja, df in dataframes_anexo12.items():
        archivo_excel = os.path.join(OUTPUT_PATH_AUDITRON, f"{nombre_hoja}.xlsx")
        
        # Exportar a Excel
        with pd.ExcelWriter(archivo_excel) as writer:
            df.to_excel(writer, sheet_name=nombre_hoja, index=False)
        
        # Aplicar formato de tabla Excel
        wb = load_workbook(archivo_excel)
        ws = wb[nombre_hoja]
        
        max_row = ws.max_row
        max_col = ws.max_column
        rango = f"A1:{get_column_letter(max_col)}{max_row}"
        
        tabla = Table(displayName=f"tbl_{nombre_hoja}", ref=rango)
        estilo = TableStyleInfo(name="TableStyleMedium9", ...)
        tabla.tableStyleInfo = estilo
        ws.add_table(tabla)
        
        wb.save(archivo_excel)
```

**Archivos Generados:**
- `Proyectos_con_Anexo12.xlsx`
- `Matriz_Calificacion_Conteo.xlsx`
- `Matriz_Calificacion.xlsx`
- `Matriz_Pruebas.xlsx`
- `Programa_Trabajo_Credicorp.xlsx`

### Otros Módulos de Apps

```python
# Consultas generales
dataframes_consultas = {
    "Consultas_Actividades": df_consulta_actividades,
    "Consultas_Observaciones": df_consulta_observaciones,
    "Consultas_Proyectos": df_consulta_proyectos,
    "Consultas_Estructura": df_consulta_estructura,
    "Consultas_contactos": df_consulta_contactos,
    "Consultas_ampliaciones": df_consulta_ampliaciones,
    # ...
}

# PEAS (Programa de Evaluación de Auditoría)
dataframes_peas = {
    "Base_PEAS": df_consulta_base_proyectos_pea,
    "PEAS": df_PEAS
}

# Auditados
dataframes_consultas_auditados = {
    "Consultas_Observaciones": df_consulta_observaciones,
    "Consultas_base_obs_auditados": df_consulta_base_obs_auditados
    # ...
}
```

## 📊 Módulo: Dashboards.py

Genera fuentes CSV para dashboards de Power BI.

### DashboardsInnovacion()

Función principal que genera **30+ archivos CSV** para Power BI:

#### 1. Limpieza de Archivos Anteriores

```python
print("Eliminando excels  ...")
if os.listdir(OUTPUT_PATH_PBI):
    for archivo in os.listdir(OUTPUT_PATH_PBI):
        archivo_completo = os.path.join(OUTPUT_PATH_PBI, archivo)
        if os.path.isfile(archivo_completo):
            os.remove(archivo_completo)
```

#### 2. Stock Observaciones Diario

Genera vista diaria del estado de observaciones:

```python
fecha_actual = fecha_hoy()

# Obtener historial hasta hoy
df_historialObservacionesHoy = df_historialObservaciones.rename(
    columns={"Estado": "SITUACION", "ID": "ID_HISTORIAL"}
)
df_historialObservacionesHoy = df_historialObservacionesHoy.query('FECHA <= @fecha_actual')
df_historialObservacionesHoy = df_historialObservacionesHoy.sort_values(
    by='ID_HISTORIAL', ascending=False
)
df_historialObservacionesHoy = df_historialObservacionesHoy.groupby(
    'ID_OBSERVACION_CONSOLIDADO'
).first()

# Fusionar con stock actual
df_stockObservacionesHoy = df_stockObservaciones.merge(
    df_historialObservacionesHoy, 
    left_on="ID_CONSOLIDADO", 
    right_on="ID_OBSERVACION_CONSOLIDADO", 
    how="left"
)

# Calcular estado (Vencido/En Fecha)
df_stockObservacionesHoy['ESTADO'] = np.where(
    df_stockObservacionesHoy['FECHA_DE_VENCIMIENTO'] < df_stockObservacionesHoy['FECHA_CORTE'],
    'Vencido', 
    'En Fecha'
)
```

#### 3. Stock Observaciones TI

Filtro específico para Gerencia de TI:

```python
# Exclusión de nombres específicos
nombres_excluidos = [
    "Renzo Zapata Euribe",
    "Marlon Jose Torrico Marchan",
    # ... otros nombres
]

df_stockObservaciones_TI = df_stockObservacionesHoy[
    (((df_stockObservacionesHoy['GERENCIA_NIVEL_1'] == 'CSC Sistemas') | 
      (df_stockObservacionesHoy['GERENCIA_NIVEL_1'] == 'División de Tecnología, Data, IA y Operaciones')) & 
     (df_stockObservacionesHoy['AÑO'] >= 2024)) & 
    (~df_stockObservacionesHoy['PROPIETARIO'].isin(nombres_excluidos))
]
```

#### 4. Exportación Masiva de CSVs

```python
# Stock Observaciones
df_stockObservaciones.to_csv(route_stockObservaciones, index=False)

# Historial Observaciones
df_historialObservaciones.to_csv(route_historialObservaciones, index=False)

# Validación Plan
df_validacionPlan.to_csv(route_validacionPlan, index=False)

# Efectividad de Controles
df_efectividadControles.to_csv(route_efectividadControles, index=False)

# Riesgos y Controles
df_riesgosControles.to_csv(route_riesgosControles, index=False)

# Equipo Auditoría
df_equipoAuditoria.to_csv(route_equipoAuditoria, index=False)

# ... 25+ exportaciones más
```

### CSVs Generados para Power BI

1. **StockObservaciones.csv** - Estado actual de observaciones
2. **StockObservaciones_Diario.csv** - Vista diaria
3. **StockObservaciones_TI.xlsx** - Vista específica TI
4. **HistorialObservaciones.csv** - Historial completo
5. **ValidacionPlan.csv** - Validación de planificación
6. **EfectividadControles.csv** - Efectividad de controles
7. **RiesgosControles.csv** - Matriz de riesgos y controles
8. **EquipoAuditoria.csv** - Información del equipo
9. **ProyectoEquipo.csv** - Asignaciones de proyectos
10. **IndicadoresDesempenio.csv** - KPIs
11. **RotacionPersonal.csv** - Rotación de personal
12. **AuditorEvaluacion.csv** - Evaluaciones de auditores
13. **BaseUniverso.csv** - Universo auditable
14. **HistorialEvaluaciones.csv** - Historial de evaluaciones
15. **ScoringEvaluacion.csv** - Scoring de evaluaciones
16. **ReporteFeriados.csv** - Feriados
17. **ProyectoActividad.csv** - Actividades de proyectos
18. **ProyectosConsolidado.csv** - Proyectos consolidados
19. **CumplimientoPlan.csv** - Cumplimiento del plan
20. **ControlesClave.csv** - Controles clave
21. **EfectividadPlanAnual.csv** - Efectividad anual
22. **EfectividadHistorico.csv** - Efectividad histórica
23. **Matriz.csv** - Matriz de evaluación
24. **Matriz_Evaluacion.csv** - Matriz de evaluación detallada
25. **Scoring_historico.csv** - Scoring histórico
26. **Anexo12.csv** - Anexo 12
27. **Encuesta_ISA.xlsx** - Encuesta ISA
28. **MapaAseguramientoBI.xlsx** - Mapa de aseguramiento
29. **MapaConsolidado.csv** - Mapa consolidado
30. **ValidacionPlanIndicadores.csv** - Validación indicadores
31. **log.csv** - Logs del sistema
32. **ProyectosAuditoria.csv** - Proyectos de auditoría
33. **HistorialProyectos.csv** - Historial de proyectos
34. **HistoricoGeneralProyectos.csv** - Histórico general
35. **PwApps_UniversoControles.xlsx** - Universo de controles

### ValidacionCarpetas()

Valida la estructura de carpetas de proyectos:

```python
def ValidacionCarpetas():
    # Valida existencia y estructura de carpetas
    # por cada negocio (PS, Prima, CrediSeguro, Salud)
    pass
```

### calidad_carpetas()

Realiza auditoría de calidad sobre carpetas de proyectos:

```python
def calidad_carpetas():
    # Verifica completitud de documentación
    # Genera reportes de calidad
    pass
```

## 📊 Módulo: fuentes.py

Carga todos los dataframes desde queries SQL:

```python
from functions import *
from params import *

# Cargar 60+ dataframes
df_controles = obtenerDatosDe("controles")
df_mapaAuxiliar = obtenerDatosDe("mapaaseguramiento_auxiliar")
df_indicadoresDesempenio = obtenerDatosDe("IndicadoresDesempenio")
df_mapaAseguramientoBI = obtenerDatosDe("MapaAseguramientoBI")
df_scoring = obtenerDatosDe("scoring")
df_proyectosPs = obtenerDatosDe("ProyectosPs")
df_stockObservaciones = obtenerDatosDe("StockObservaciones")
df_historialObservaciones = obtenerDatosDe("HistorialObservaciones")
# ... 52+ dataframes más
```

## 🔍 Módulo: functions.py

Funciones auxiliares para procesamiento:

```python
def obtenerDatosDe(nombre_query):
    """Ejecuta query SQL y retorna DataFrame"""
    query_path = os.path.join(QUERIES_PATH, f"{nombre_query}.sql")
    query = open(query_path, encoding='utf-8').read()
    return pd.read_sql(query, cnxn_TIGA)

def fecha_hoy():
    """Retorna fecha actual"""
    return datetime.datetime.now().date()

def aplicar_formato_tabla(worksheet, nombre_tabla):
    """Aplica formato de tabla Excel"""
    # ...
```

## 🚀 Ejecución

### Manual
```bash
cd PY001_ScriptsInnovacion
python main.py
```

### Via Batch
```batch
executable.bat
```

### Automatizada
Se ejecuta diariamente después del proceso **ETL** mediante tarea programada.

## 📈 Características Técnicas

### Manejo de Errores
- Try-catch por cada módulo independiente
- Logging detallado con timestamps
- Generación de archivos de error en producción
- Variable de entorno `ENVIRONMENT` para diferenciar dev/prod

### Optimizaciones
- Limpieza automática de archivos antiguos
- Exportación en paralelo cuando es posible
- Formato de tablas Excel para mejor consumo
- Encoding UTF-8 para compatibilidad

### Validaciones
- Verificación de existencia de carpetas
- Validación de estructura de datos
- Filtros de negocio específicos
- Exclusiones configurables

## ⏱️ Tiempo de Ejecución

**Total aproximado: 10-15 minutos**
- Apps Auditron: 2-3 minutos
- Dashboards Innovación: 5-8 minutos
- Validación Carpetas: 1-2 minutos
- Calidad Carpetas: 2-3 minutos

## 🛠️ Dependencias

```python
import os
import sys
import pandas as pd
import numpy as np
import openpyxl as ox
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from datetime import datetime
from dateutil.relativedelta import relativedelta
import traceback
```

### Instalación
```bash
pip install pandas numpy openpyxl python-dateutil pyodbc
```

## ⚠️ Consideraciones Importantes

1. **Variable de Entorno**: Configurar `ENVIRONMENT=AIA_Produccion` en producción
2. **Rutas de SharePoint**: Deben estar sincronizadas correctamente
3. **Permisos**: Requiere permisos de escritura en todas las carpetas de salida
4. **Queries SQL**: 60+ archivos SQL deben existir en carpeta queries/
5. **Consumidores**: Power BI y PowerApps dependen de estos archivos

## 🔗 Integración

### Entrada
- Base de datos TIGA actualizada por **ETL**

### Salida (Consumidores)
- **Power BI**: 35+ dashboards
- **PowerApps**: Auditron, PEAS, Consultas, Auditados
- **Usuarios Finales**: Reportes Excel directos
- **Proceso de Verificación**: Archivos específicos monitoreados

## 📞 Contacto y Soporte

Para consultas sobre este módulo, contactar al equipo de Analítica e Innovación en Auditoría.

---

**Última actualización**: Diciembre 2025  
**Versión**: 1.0  
**Autor**: Equipo Analítica e Innovación - Pacífico Seguros
