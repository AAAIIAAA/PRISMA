
SET QUOTED_IDENTIFIER ON;
INSERT INTO PROYECTOSIAV2.dbo.TG_Observacion_Historial
SELECT 
'PRI-'+CONVERT(VARCHAR,B.ID), 
'PRI-' + CONVERT(VARCHAR, B.RecommendationID) [ID_Observación],
'PRI-'+ CONVERT(VARCHAR,B.UserID) [ContactoID],
PROYECTOSIAV2.dbo.Clear_HTML( B.ActionText) [Texto],
 B.ActionDate [Fecha],B.PrePostDate [Fecha_Revisada],
	(CASE 
	WHEN B.TypeLID IN (2,9,14) THEN 'Actualización de Estado'
	WHEN B.TypeLID = 15 THEN 'Implementación'
	WHEN B.TypeLID = 17 THEN 'Cierre'
	WHEN B.TypeLID = 3 THEN 'Comentario' 
	WHEN B.TypeLID = 5 THEN 'ReleasedToTC' 
	WHEN B.TypeLID = 13 THEN 'UnreleasedToTC' 
	WHEN B.TypeLID = 8 THEN 'Rejected'
	ELSE 'Otro'
	END) [Acción],
	B.StatusLID [ID_Estado],
	B.Progress
FROM PROYECTOSIAV2.dbo.TG_Observacion_Historial A
RIGHT JOIN ( select RA.* , R.Progress from TeamMate_Prima.dbo.TM_RecommendationAction RA 
inner join TeamMate_Prima.dbo.TM_Recommendation R
on RA.RecommendationID = r.ID) B
ON A.Identificador = 'PRI-'+CONVERT(VARCHAR,B.ID)
WHERE B.TypeLID IN (5,13,2,9,14,15,17,3,8) AND A.Identificador IS NULL
AND (  B.ActionText not IN ( 'State change to ''Started''' ,'El estado se cambió a "Iniciado"') 
or   B.ActionText  is null)
Select 1 as flag