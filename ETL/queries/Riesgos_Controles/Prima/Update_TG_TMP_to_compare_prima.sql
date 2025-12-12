
SELECT * 
INTO #TempTable2 
FROM PROYECTOSIAV2.dbo.fn_TG_TMP_Obtener_Cambios_actualizar_to_compare_prima()

UPDATE T 
SET


T.[Descripcion] = Tabla.[Descripcion],
T.[UserCategory1CID] = Tabla.[UserCategory1CID],


T.[Descripción del Control] = Tabla.[Descripción del Control],
T.[Objetivo Relacionado a la Unidad Auditada] = Tabla.[Objetivo Relacionado a la Unidad Auditada],
T.[x1] = Tabla.[x1],
T.[x2] = Tabla.[x2],
T.[x3] = Tabla.[x3],
T.[x4] = Tabla.[x4],
T.[x5] = Tabla.[x5],
T.[x6] = Tabla.[x6],
T.[Control_Sox] = Tabla.[Control_Sox],
T.[Control Regulatorio] = Tabla.[Control Regulatorio],
T.[Nombre de la Herramienta/Sistema] = Tabla.[Nombre de la Herramienta/Sistema],
T.[Unidad Responsable del Control] = Tabla.[Unidad Responsable del Control],
T.[I-P-V-R] = Tabla.[I-P-V-R],
T.[EX-IN-VA-PR-DO] = Tabla.[EX-IN-VA-PR-DO],
T.[Tipo de Controles] = Tabla.[Tipo de Controles],
T.[Naturaleza del Control] = Tabla.[Naturaleza del Control],
T.[Plan de Pruebas] = Tabla.[Plan de Pruebas],
T.[Ponderado del Control] = Tabla.[Ponderado del Control],
T.[Emisión] = Tabla.[Emisión],
T.[Área Responsable] = Tabla.[Área Responsable],
T.[Finalizado] = Tabla.[Finalizado],
T.[CuentaContable] = Tabla.[CuentaContable]

 

FROM PROYECTOSIAV2.dbo.TG_TMP_TO_COMPARE T
JOIN #TempTable2 AS Tabla
ON T.Identificador = Tabla.Identificador;

DROP TABLE #TempTable2

