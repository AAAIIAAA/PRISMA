# Backup Prima - Exportación de Datos TeamMate

## 📋 Descripción General

Este módulo es el **primer paso** del sistema ETL completo. Se ejecuta en una máquina virtual independiente y tiene como objetivo exportar datos desde la base de datos **TeamMate_Prima** hacia archivos CSV, los cuales son sincronizados automáticamente mediante OneDrive para ser consumidos por los procesos posteriores.

## 🎯 Objetivo

Generar backups diarios de 26 tablas críticas del sistema TeamMate_Prima en formato CSV, almacenándolos en una carpeta sincronizada de SharePoint/OneDrive para su posterior procesamiento.

## 🏗️ Arquitectura

```
┌─────────────────────────────────────┐
│   Máquina Virtual 1 (Independiente) │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   TeamMate_Prima Database    │  │
│  │   (C35T01WPDB01)            │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │      main.py                 │  │
│  │   (Backup Prima)             │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │   Archivos CSV               │  │
│  │   (26 tablas)                │  │
│  └──────────┬───────────────────┘  │
└─────────────┼───────────────────────┘
              │
              ▼ (Sincronización OneDrive)
┌─────────────────────────────────────┐
│  SharePoint/OneDrive                │
│  backup_prima_csv/                  │
│  ├── TM_Recommendation.csv          │
│  ├── TM_Project.csv                 │
│  └── ... (24 tablas más)            │
└─────────────────────────────────────┘
              │
              ▼
      [Procesos ETL Posteriores]
```

## 📂 Estructura de Archivos

```
Backup_Prima/
├── main.py          # Script principal de exportación
└── README.md        # Esta documentación
```

## 🔧 Configuración

### Conexión a Base de Datos

```python
CNXN_TIGA = (
    r'Driver={ODBC Driver 17 for SQL Server};'
    r'Server=C35T01WPDB01;'
    r'Database=TeamMate_Prima;'
    r'UID=TeamMateUser_Prima2023;'
    r'PWD=audteammateprima2023!;'
    r'Encrypt=no;'
)
```

### Directorio de Backup

```python
BACKUP_DIR = r'D:\Sharepoint\Pacífico Compañía de Seguros y Reaseguros\Analítica e Innovación en Auditoría - 01. Resultados Scripts\backup_prima_csv'
```

> ⚠️ **Importante**: Este directorio debe estar sincronizado con OneDrive para que los archivos estén disponibles para los siguientes procesos.

## 📊 Tablas Exportadas

El sistema exporta **26 tablas** de TeamMate_Prima:

### Recomendaciones y Acciones
- `TM_Recommendation` - Observaciones de auditoría
- `TM_RecommendationAction` - Acciones correctivas
- `TM_AuthRecommendation` - Autorizaciones

### Gestión de Proyectos
- `TM_Project` - Proyectos de auditoría
- `TM_Schedule` - Cronogramas
- `TM_Issue` - Hallazgos
- `TM_Procedure` - Procedimientos
- `TM_Program` - Programas de auditoría
- `TM_ProjectToOrgHierarchy` - Relación proyectos-organización

### Controles y Riesgos
- `EWP_Control` - Controles
- `EWP_Risk` - Riesgos
- `EWP_RiskToControl` - Relación riesgos-controles
- `EWP_EntityToRisk` - Relación entidades-riesgos
- `EWP_Project` - Proyectos EWP

### Usuarios y Seguridad
- `TM_Auditor` - Auditores
- `TM_User` - Usuarios
- `TM_SecurityGroup` - Grupos de seguridad
- `TM_SecurityGroupToUser` - Relación grupos-usuarios

### Configuración
- `TM_CategoryValue` - Valores de categorías
- `TM_Browser` - Navegación
- `TM_Link` - Enlaces

### Listas de Valores
- `TM_List_RecommendationStatus` - Estados de recomendaciones
- `TM_List_RecActionType` - Tipos de acciones
- `TM_List_ProjectStatus` - Estados de proyectos
- `TM_List_AuthRecRole` - Roles de autorización

### Objetos y Acciones
- `TM_ObjectAction` - Acciones sobre objetos

## ⚙️ Funcionamiento del Proceso

### 1. Inicialización

```python
# Crear directorio si no existe
os.makedirs(BACKUP_DIR, exist_ok=True)

# Limpiar archivos CSV anteriores
for f in glob.glob(os.path.join(BACKUP_DIR, '*.csv')):
    os.remove(f)
```

### 2. Conexión a Base de Datos

```python
print("Conectando a SQL Server...")
cnxn = pyodbc.connect(CNXN_TIGA)
cursor = cnxn.cursor()
```

### 3. Exportación por Tabla

Para cada tabla en la lista, el proceso:

#### a) Obtiene la metadata de columnas

```python
cursor.execute(
    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
    "WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME=? "
    "ORDER BY ORDINAL_POSITION", tabla
)
columnas = [row[0] for row in cursor.fetchall()]
```

#### b) Crea el archivo CSV con encabezados

```python
csv_path = os.path.join(BACKUP_DIR, f"{tabla}.csv")
with open(csv_path, 'w', encoding='utf-8-sig', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', 
                       quoting=csv.QUOTE_ALL, lineterminator='\n')
    writer.writerow(columnas)  # Encabezados
```

#### c) Extrae datos en lotes de 10,000 filas

```python
select_sql = f"SELECT {', '.join(f'[{c}]' for c in columnas)} FROM dbo.{tabla}"
cursor.execute(select_sql)

while True:
    rows = cursor.fetchmany(10000)  # Lotes de 10K
    if not rows:
        break
    
    # Convertir valores a strings apropiados
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
```

### 4. Logging y Finalización

```python
print(f"✓ {tabla}.csv creado: {os.path.getsize(csv_path):,} bytes")

elapsed = time.time() - start_time
print(f"\nExportación completada en {elapsed:.2f} segundos.")
```

## 🚀 Ejecución

### Manual

```bash
python main.py
```

### Automatizada

Se recomienda configurar una tarea programada en Windows para ejecutar diariamente:

```batch
@echo off
cd /d "C:\ruta\a\Backup_Prima"
python main.py
```

## 📈 Características Técnicas

### Optimizaciones

1. **Procesamiento por Lotes**: Extrae datos en chunks de 10,000 filas para optimizar memoria
2. **Encoding UTF-8-BOM**: Usa `utf-8-sig` para compatibilidad con Excel
3. **Quote All**: Todos los campos entrecomillados para evitar problemas con caracteres especiales
4. **Limpieza Automática**: Elimina archivos antiguos antes de generar nuevos

### Manejo de Datos

- **Valores NULL**: Se convierten en strings vacíos
- **Fechas**: Formato estandarizado `YYYY-MM-DD HH:MM:SS`
- **Tipos de Datos**: Conversión automática a string para CSV

## 📝 Formato de Salida

### Ejemplo: TM_Recommendation.csv

```csv
"RecID","Title","Description","Status","Priority","DueDate",...
"1001","Implementar controles","Descripción detallada...","Abierta","Alta","2024-12-31 00:00:00",...
"1002","Revisión de procesos","Otra descripción...","En Progreso","Media","2025-01-15 00:00:00",...
```

## 🔗 Integración con Procesos Posteriores

Los archivos CSV generados son consumidos por:

1. **Levantamiento** - Lee los CSVs para cargarlos en la base de datos de integración
2. **ETL** - Procesa y transforma los datos
3. **scripts_produccion** - Genera reportes y dashboards

## ⏱️ Tiempo de Ejecución

El proceso típicamente toma entre **30-60 segundos** dependiendo del volumen de datos y la velocidad de red.

## 🛠️ Dependencias

```python
import pyodbc        # Conexión a SQL Server
import csv           # Generación de archivos CSV
import os            # Gestión de archivos y directorios
import glob          # Búsqueda de patrones de archivos
import datetime      # Manejo de fechas
import time          # Medición de tiempos
```

### Instalación

```bash
pip install pyodbc
```

> **Nota**: Requiere ODBC Driver 17 for SQL Server instalado en el sistema.

## ⚠️ Consideraciones Importantes

1. **Máquina Virtual Independiente**: Este proceso corre en una VM separada del resto del sistema
2. **Sincronización OneDrive**: Es crítico que la carpeta de destino esté correctamente sincronizada
3. **Conectividad**: Debe tener acceso de red al servidor `C35T01WPDB01`
4. **Credenciales**: Las credenciales están hardcodeadas (considerar variables de entorno en producción)
5. **Espacio en Disco**: Verificar que haya espacio suficiente en el directorio de destino

## 🔄 Flujo de Datos

```mermaid
graph LR
    A[TeamMate_Prima DB] --> B[main.py]
    B --> C[26 archivos CSV]
    C --> D[OneDrive Sync]
    D --> E[Proceso Levantamiento]
```

## 📞 Contacto y Soporte

Para consultas sobre este módulo, contactar al equipo de Analítica e Innovación en Auditoría.

---

**Última actualización**: Diciembre 2025  
**Versión**: 1.0  
**Autor**: Equipo Analítica e Innovación - Pacífico Seguros
