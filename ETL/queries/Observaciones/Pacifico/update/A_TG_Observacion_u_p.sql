SET QUOTED_IDENTIFIER ON;
UPDATE C
SET
[NOMBRE PROYECTO] = B.[NOMBRE PROYECTO],
[TITULO OBSERVACION] = B.[TITULO OBSERVACION],
[OBSERVACION] = PROYECTOSIAV2.dbo.Clear_HTML(B.OBSERVACION),
[RECOMENDACION] = PROYECTOSIAV2.dbo.Clear_HTML(B.RECOMENDACION),
[PRIMERA RESPUESTA] = PROYECTOSIAV2.dbo.Clear_HTML(B.[PRIMERA RESPUESTA]),
[UNIDAD RESPONSABLE] = B.[UNIDAD RESPONSABLE],
[PROPIETARIO] = PROYECTOSIAV2.dbo.[InitCap](B.PROPIETARIO),
[EMAIL PROPIETARIO] = B.[EMAIL PROPIETARIO],
[OBSERVADOR] = PROYECTOSIAV2.dbo.[InitCap](B.OBSERVADOR),
[COLABORADOR] = PROYECTOSIAV2.dbo.[InitCap](B.COLABORADOR),
[FECHA EMISIÓN] = B.[FECHA EMISIÓN],
RIESGO = B.RIESGO,
[FECHA ESTIMADA] = B.[FECHA ESTIMADA],
[FECHA REVISADA] = B.[FECHA REVISADA],
[FECHA DE VENCIMIENTO] = B.[FECHA DE VENCIMIENTO],
COORDINADOR = B.COORDINADOR,
[TIPO OBSERVACIÓN] = B.[TIPO OBSERVACIÓN],
OFICINA = B.OFICINA


FROM PROYECTOSIAV2.dbo.TG_Observacion C with (NOLOCK) 
INNER JOIN  PROYECTOSIAV2.dbo.[fn_TG_Observacion_Obtener_Cambios]() U ON C.Identificador = U.Identificador
INNER JOIN 
(
SELECT 
		R.ID [ID], 
		P.Code [PROYECTO],
		P.Title [NOMBRE PROYECTO], 
		S.Title [TITULO OBSERVACION], 
		I.Finding [OBSERVACION],
		R.RecommendationText [RECOMENDACION],
		R.ResponseText [PRIMERA RESPUESTA],
		CAT1.Name [UNIDAD RESPONSABLE],
		ISNULL((SELECT U.FirstName + ' ' + U.LastName 
				FROM (SELECT TOP 1 UserID FROM TeamMateR12.dbo.TM_AuthRecommendation UR WITH(NOLOCK) 
				WHERE RecommendationID = R.ID and UR.RoleLID = 256) AS A
						JOIN TeamMateR12.dbo.TM_User U on A.UserID = U.ID),'')  [PROPIETARIO],
		LOWER(ISNULL((SELECT U.Email FROM 
				(SELECT TOP 1  UserID FROM TeamMateR12.dbo.TM_AuthRecommendation UR WITH (NOLOCK) 
				WHERE UR.RecommendationID = R.ID and UR.RoleLID = 256) as A 
				JOIN TeamMateR12.dbo.TM_User U on A.UserID = U.ID),''))     [EMAIL PROPIETARIO],
		ISNULL(STUFF((SELECT '; ' + U.FirstName + ' ' + U.LastName FROM 
				(SELECT UserID FROM TeamMateR12.dbo.TM_AuthRecommendation UR WITH (NOLOCK)
				WHERE UR.RecommendationID = R.ID and UR.RoleLID = 32) as A 
				LEFT JOIN TeamMateR12.dbo.TM_User U 
					on A.UserID = U.ID FOR XML PATH(''),TYPE).value('(./text())[1]','VARCHAR(MAX)'),1,2,''),'') [OBSERVADOR],
		ISNULL(STUFF((SELECT '; ' + U.FirstName + ' ' + U.LastName FROM 
				(SELECT UserID FROM TeamMateR12.dbo.TM_AuthRecommendation UR WITH (NOLOCK)
				WHERE UR.RecommendationID = R.ID and UR.RoleLID = 128) as A 
					LEFT JOIN TeamMateR12.dbo.TM_User U 
					on A.UserID = U.ID FOR XML PATH(''),TYPE).value('(./text())[1]','VARCHAR(MAX)'),1,2,''),'') [COLABORADOR],
		IIF(PFE.[Fecha Emisión] IS NOT NULL, 
		CONVERT(DATE,PFE.[Fecha Emisión]), 
		CONVERT(DATE,FE.FechaEmision)) [FECHA EMISIÓN],
		 
		--CONVERT(DATE,PFE.[Fecha Emisión])[FECHA EMISIÓN],
		ISNULL(CAT2.Name,'') [RIESGO],
		CONVERT (DATE,R.EstimatedImplDate) [FECHA ESTIMADA],	
		CONVERT (DATE,R.RevisedImplDate) [FECHA REVISADA],
		CONVERT(DATE,isnull(R.RevisedImplDate,R.EstimatedImplDate)) [FECHA DE VENCIMIENTO],	
		SG.Name [COORDINADOR],
		ISNULL(CAT3.Name,'') [TIPO OBSERVACIÓN], 
		ISNULL(CAT4.Name,'') [OFICINA]
	FROM TeamMateR12.dbo.TM_Recommendation R WITH (NOLOCK) 
		LEFT JOIN TeamMateR12.dbo.TM_Issue I WITH (NOLOCK) ON R.IssueID = I.ID
		LEFT JOIN TeamMateR12.dbo.TM_Schedule S WITH (NOLOCK) ON I.ScheduleID = S.ID
		LEFT JOIN TeamMateR12.dbo.TM_Project P WITH (NOLOCK) ON S.ProjectID = P.ID
		LEFT JOIN TeamMateR12.dbo.TM_CategoryValue CAT1 WITH (NOLOCK) ON CAT1.CategoryID = R.UserCat2CID AND CAT1.Culture = 'ES-ES'
		LEFT JOIN TeamMateR12.dbo.TM_CategoryValue CAT2 WITH (NOLOCK) ON CAT2.CategoryID = R.PriorityCID AND CAT2.Culture = 'ES-ES'
		LEFT JOIN TeamMateR12.dbo.TM_CategoryValue CAT3 WITH (NOLOCK) ON CAT3.CategoryID = I.TypeCID AND CAT3.Culture = 'ES-ES'
		LEFT JOIN TeamMateR12.dbo.TM_CategoryValue CAT4 WITH (NOLOCK) ON CAT4.CategoryID = R.UserCat1CID AND CAT4.Culture = 'ES-ES'
		LEFT JOIN TeamMateR12.dbo.TM_SecurityGroup SG WITH (NOLOCK) ON R.SecurityGroupID = SG.ID	
		LEFT JOIN (SELECT * FROM PROYECTOSIAV2.dbo.View_TG_Proyecto_FechaEmisión WHERE Compañia != 'AIP') PFE ON REPLACE(PFE.[Código],' ','') = REPLACE(P.Code,' ','') COLLATE Modern_Spanish_CI_AS
		LEFT JOIN (
			SELECT S9.ProjectID IDPROJECT, MAX(IIF(O9.Flag = 1, DATEADD(HOUR,-5, O9.ActionDate), O9.ActionDate)) FechaEmision 
			FROM TeamMateR12.dbo.TM_ObjectAction O9 INNER JOIN TeamMateR12.dbo.TM_Schedule S9 ON O9.ObjectID = S9.ID 
			WHERE O9.ObjectTypeLID = 11 AND O9.TypeLID = 4 AND O9.UserID IN (7) GROUP BY S9.ProjectID
		) AS FE ON FE.IDPROJECT  = P.ID
	WHERE R.StatusLID IN (2,3,13,9,10,11,12) AND R.TrackFlag = 1 AND (P.StatusLID = 8 OR P.Code  = 'PRE - 001')
	)as B ON C.Identificador ='PS-'+CONVERT(VARCHAR,B.ID)

Select 1 as flag



