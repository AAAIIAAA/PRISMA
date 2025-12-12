SELECT 
	REPLACE(TP.Codigo,' ','') Código,
	ISNULL(IIF(CR.Nombre IS NULL, drt.Nombre, CR.Nombre),'') Calificativo, 
	M2.Nombre Macroproceso
	--ISNULL(IIF(M.Nombre IS NULL, M2.Nombre, M.Nombre),'') Macroproceso
FROM (SELECT * FROM TG_Proyecto WHERE Compañia != 'AIP') TP 
LEFT JOIN  TG_Registro_Proyectos RP ON TP.Codigo = RP.CodProy
	LEFT JOIN TG_Riesgo CR ON RP.IDR = CR.ID
	LEFT JOIN TG_Riesgo_Del_Trabajo drt ON drt.IdRiesgoDelTrabajo = tp.IdRiesgoDelTrabajo 
--	LEFT JOIN TG_ProcesoEvaluado M ON RP.IDM = M.IdProcesoEvaluado 
	LEFT JOIN TG_Proceso_Evaluado M2 ON TP.IdProcesoEvaluado = M2.IdProcesoEvaluado