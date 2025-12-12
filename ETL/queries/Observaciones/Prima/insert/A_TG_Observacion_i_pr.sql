SET QUOTED_IDENTIFIER ON;
INSERT INTO PROYECTOSIAV2.dbo.TG_Observacion 
SELECT 
'PRI-' + CONVERT(VARCHAR,B.ID),
B.PROYECTO,
B.[NOMBRE PROYECTO],
B.[TÍTULO OBSERVACIÓN] ,
PROYECTOSIAV2.dbo.Clear_HTML(B.OBSERVACIÓN) [OBSERVACION],
PROYECTOSIAV2.dbo.Clear_HTML(B.RECOMENDACIÓN) [RECOMENDACION],
PROYECTOSIAV2.dbo.Clear_HTML(B.[PRIMERA RESPUESTA]) [PRIMERA RESPUESTA],
B.[UNIDAD RESPONSABLE],
PROYECTOSIAV2.dbo.[InitCap](B.PROPIETARIO) [PROPIETARIO],
B.[EMAIL PROPIETARIO],
PROYECTOSIAV2.dbo.[InitCap](B.OBSERVADOR) [OBSERVADOR],
PROYECTOSIAV2.dbo.[InitCap](B.COLABORADOR) [COLABORADOR],
B.[FECHA EMISIÓN],
B.RIESGO,
B.[FECHA ESTIMADA],
B.[FECHA REVISADA],
B.[FECHA DE VENCIMIENTO],
B.COORDINADOR,
B.[TIPO OBSERVACIÓN],
B.OFICINA
FROM (select Identificador from PROYECTOSIAV2.dbo.TG_Observacion with (NOLOCK)) A 
RIGHT JOIN 
(
SELECT 
	
	R.ID [ID],
	REPLACE(P.CODE_AJUST,'-','-') [PROYECTO],
	P.Title [NOMBRE PROYECTO],
	S.Title [TÍTULO OBSERVACIÓN],
	I.Finding [OBSERVACIÓN],
	R.RecommendationText [RECOMENDACIÓN],
	R.ResponseText [PRIMERA RESPUESTA],
	CAT1.Name [UNIDAD RESPONSABLE],
	
	ISNULL((SELECT U.FirstName + ' ' + U.LastName
    FROM (SELECT TOP 1  UserID FROM TeamMate_Prima.dbo.TM_AuthRecommendation UR with (NOLOCK) 
    WHERE RecommendationID = R.ID and UR.RoleLID = 256) as A 
    JOIN TeamMate_Prima.dbo.TM_User U on A.UserID = U.ID),'')  [PROPIETARIO],
    
	LOWER(ISNULL((SELECT U.Email
    FROM (SELECT TOP 1  UserID FROM TeamMate_Prima.dbo.TM_AuthRecommendation UR with (NOLOCK)
    WHERE UR.RecommendationID = R.ID and UR.RoleLID = 256) as A 
    JOIN TeamMate_Prima.dbo.TM_User U on A.UserID = U.ID),''))  [EMAIL PROPIETARIO],
    
    ISNULL(STUFF((SELECT '; ' + U.FirstName + ' ' + U.LastName 
    FROM (SELECT UserID FROM TeamMate_Prima.dbo.TM_AuthRecommendation UR with (NOLOCK)
    WHERE UR.RecommendationID = R.ID and UR.RoleLID = 32) as A 
    LEFT JOIN TeamMate_Prima.dbo.TM_User U 
	on A.UserID = U.ID FOR XML PATH(''),TYPE).value('(./text())[1]','VARCHAR(MAX)'),1,2,''),'') [OBSERVADOR],
    
    ISNULL(STUFF((SELECT '; ' + U.FirstName + ' ' + U.LastName 
    FROM (SELECT UserID FROM TeamMate_Prima.dbo.TM_AuthRecommendation UR with (NOLOCK)
    WHERE UR.RecommendationID = R.ID and UR.RoleLID = 128) as A 
    LEFT JOIN TeamMate_Prima.dbo.TM_User U 
	on A.UserID = U.ID FOR XML PATH(''),TYPE).value('(./text())[1]','VARCHAR(MAX)'),1,2,''),'') [COLABORADOR],
    
(CASE WHEN PFE.[Fecha Emisión] IS NOT NULL THEN CONVERT(DATE,PFE.[Fecha Emisión]) 
ELSE CONVERT(DATE,FE.FechaEmision) END) [FECHA EMISIÓN],

--CONVERT(DATE,PFE.[Fecha Emisión]) [FECHA EMISIÓN],

	ISNULL(CAT2.Name,'') [RIESGO],
	CONVERT (DATE,R.EstimatedImplDate) [FECHA ESTIMADA],
	CONVERT (DATE,R.RevisedImplDate) [FECHA REVISADA],
	CONVERT (DATE,isnull(R.RevisedImplDate,R.EstimatedImplDate)) [FECHA DE VENCIMIENTO],
	SG.Name [COORDINADOR],
	ISNULL(CAT3.Name,'') [TIPO OBSERVACIÓN],
	ISNULL(CAT4.Name,'') [OFICINA]
	FROM TeamMate_Prima.dbo.TM_Recommendation R with (NOLOCK)
	LEFT JOIN TeamMate_Prima.dbo.TM_Issue I with (NOLOCK) ON R.IssueID = I.ID
	LEFT JOIN TeamMate_Prima.dbo.TM_Schedule S with (NOLOCK) ON I.ScheduleID = S.ID
	LEFT JOIN  (
		select (case when (code not like '%2020%' and code not like '%2021%' 
		and code not like '%2022%' and code not like '%2023%'and code not like '%2024%'
		and code not like '%2025%' and code not like '%2026%' ) 
		then ISNULL(PARSENAME(REPLACE(CODE,'-','.'),4)+ ' - '+
			 PARSENAME(REPLACE(CODE,'-','.'),3)+ ' - '+
				RIGHT('000'+PARSENAME(REPLACE(CODE,'-','.'),2),3)+ ' - '+
		(CASE WHEN LEN(PARSENAME(replace(code,'-','.'),1)) = 2 THEN '20'+PARSENAME(replace(code,'-','.'),1) 
		ELSE PARSENAME(replace(code,'-','.'),1) END),CODE) else code end)CODE_AJUST,x.*
			FROM TeamMate_PRima.dbo.TM_Project X with (NOLOCK)) P ON S.ProjectID = P.ID
	LEFT JOIN TeamMate_Prima.dbo.TM_CategoryValue CAT1 with (NOLOCK) ON CAT1.CategoryID = R.UserCat2CID AND CAT1.Culture = 'ES-ES'
	LEFT JOIN TeamMate_Prima.dbo.TM_CategoryValue CAT2 with (NOLOCK) ON CAT2.CategoryID = R.PriorityCID AND CAT2.Culture = 'ES-ES'
    LEFT JOIN TeamMate_Prima.dbo.TM_CategoryValue CAT3 with (NOLOCK) ON CAT3.CategoryID = I.TypeCID AND CAT3.Culture = 'ES-ES'
	LEFT JOIN TeamMate_Prima.dbo.TM_CategoryValue CAT4 with (NOLOCK) ON CAT4.CategoryID = R.UserCat1CID AND CAT4.Culture = 'ES-ES'    
    LEFT JOIN TeamMate_Prima.dbo.TM_SecurityGroup SG with (NOLOCK)	ON R.SecurityGroupID = SG.ID	
	LEFT JOIN (Select * from PROYECTOSIAV2.dbo.View_TG_Proyecto_FechaEmisión WHERE Compañia ='AIP') PFE ON REPLACE(PFE.[Código],' ','') = REPLACE(P.Code,' ','') COLLATE Modern_Spanish_CI_AS
	LEFT JOIN (SELECT S9.ProjectID IDPROJECT, 
				MAX(CASE O9.Flag WHEN 1 THEN DATEADD(HOUR,-5, O9.ActionDate) ELSE O9.ActionDate END) FechaEmision 
				FROM TeamMate_Prima.dbo.TM_ObjectAction O9
					INNER JOIN TeamMate_Prima.dbo.TM_Schedule S9 ON O9.ObjectID = S9.ID 
					WHERE O9.ObjectTypeLID = 11 AND O9.TypeLID = 4 AND O9.UserID IN (7) 
					GROUP BY S9.ProjectID) AS FE ON FE.IDPROJECT  = P.ID
    
	WHERE R.StatusLID IN (2,3,13,9,10,11,12) AND R.TrackFlag = 1 AND (P.StatusLID = 8 OR P.Code  = 'PRE - 001')AND (P.CODE_AJUST NOT LIKE '%CAL%' AND P.CODE_AJUST NOT LIKE '%ROP%' AND P.CODE_AJUST NOT LIKE '%IRAM%' AND P.CODE_AJUST NOT LIKE '%Prueba%')
)
B
ON A.Identificador = 'PRI-'+convert(varchar,B.ID)
WHERE A.Identificador IS NULL

Select 1 as flag