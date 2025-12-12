select
Replace(TP.Codigo,' ','')Código,
ISNULL(IIF(CR.Nombre IS NULL, drt.Nombre, CR.Nombre),'') Calificativo, 
M2.Nombre Macroproceso
--isnull((case when M.Nombre is null then M2.Nombre else M.Nombre end),'')Macroproceso
from 
(SELECT * FROM TG_Proyecto WHERE Compañia = 'AIP') TP
left join  TG_Registro_Proyectos RP on TP.Codigo = RP.CodProy
LEFT JOIN TG_Riesgo_Del_Trabajo drt ON drt.IdRiesgoDelTrabajo = tp.IdRiesgoDelTrabajo 
left join TG_Riesgo CR on RP.IDR = CR.ID 
--LEFT JOIN TG_ProcesoEvaluado M ON RP.IDM = M.IdProcesoEvaluado 
LEFT JOIN TG_Proceso_Evaluado M2 ON TP.IdProcesoEvaluado = M2.IdProcesoEvaluado
