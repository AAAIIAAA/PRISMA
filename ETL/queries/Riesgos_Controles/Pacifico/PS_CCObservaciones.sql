 SELECT distinct ISS.LocationCID, 
 ISS.CategoryCID,ISS.UserCategory1CID,
 ISS.UserCategory2CID,ISS.UserCategory3CID,
 ISS.UserCategory4CID, RE.id, SS.Title, RE.Title, 
 LRS.Name, ISNULL( CAST(RA.ActionDate AS date), 
 CAST(EWPP.FinalizeDate AS date)) AS 'FechaCambio' 
 FROM EWP_Project EWPP INNER JOIN TM_Project P 
 ON EWPP.Projectid = P.id INNER JOIN TM_Schedule S 
 ON P.ID=S.ProjectID INNER JOIN TM_Program PR 
 ON PR.ScheduleID=S.ID INNER JOIN  TM_Procedure PC  
 ON PC.ProgramID=PR.id INNER JOIN TM_Link L 
 ON L.TargetObjectID=PC.id AND L.TargetObjectTypeLID = 4 
 INNER JOIN TM_Schedule SS ON L.SourceObjectID=SS.ID  
 AND SS.ObjectTypeLID = 2 AND L.SourceObjectTypeLID = 11 
 JOIN TM_Issue ISS ON ISS.ScheduleID = SS.ID 
 JOIN TM_Recommendation RE ON RE.IssueID = ISS.ID 
 LEFT JOIN TM_CategoryValue CV ON CV.CategoryID = RE.PriorityCID 
 AND CV.Culture LIKE 'es-Es' INNER JOIN TM_List_RecommendationStatus LRS 
 ON LRS.ID = RE.StatusLID LEFT JOIN TM_RecommendationAction RA 
 ON RA.RecommendationID = RE.ID AND RA.StatusLID = RE.StatusLID 
 AND RA.TypeLID IN (14,15,16,17) 
 WHERE RE.TrackFlag = 1 and CV.Name NOT LIKE '%Oportunidad%' AND L.targetObjectID = 'Valor'
 union
 Select tis.LocationCID,tis.CategoryCID,tis.UserCategory1CID,tis.UserCategory2CID,tis.UserCategory3CID,tis.UserCategory4CID,
 tr.id,tsc.Title,tr.Title,tlr.Name,ISNULL( CAST(tra.ActionDate AS date), 
 CAST(tra.ActionDate AS date)) AS 'FechaCambio' 
  from (
   SELECT TS.Title,SourceObjectID,TargetObjectTypeLID,ltrim(Rtrim(Replace(x.codigo,'#IDOBSANT','')))Codigo,targetObjectID
   FROM TM_Link TL 
   INNER JOIN TM_Schedule TS ON TL.TargetObjectID = TS.ID
   INNER JOIN TM_Issue TI ON TS.id = TI.ScheduleID
      Outer Apply (select datos as codigo from [PROYECTOSIAV2].dbo.[Split]([PROYECTOSIAV2].dbo.[Clear_HTML](ti.IssueText1),',')) x
   WHERE Ti.IssueText1 LIKE '%#IDOBSANT%')w
   INNER JOIN TM_Recommendation tr on tr.ID = cast(w.Codigo as integer)
   INNER JOIN TM_Issue tis on tis.ID =tr.IssueID
   INNER JOIN TM_Schedule tsc on tsc.ID = tis.ScheduleID
   INNER JOIN TM_List_RecommendationStatus TLR ON TLR.ID = TR.StatusLID
   LEFT JOIN TM_RecommendationAction TRA ON TR.ID=TRA.RecommendationID AND TRA.StatusLID = TR.StatusLID AND TRA.TypeLID IN (2,14,15,16,17)
   LEFT JOIN TM_CategoryValue CV ON CV.CategoryID = TR.PriorityCID AND CV.Culture LIKE 'es-ES'
	WHERE tr.TrackFlag = 1 and CV.Name NOT LIKE '%Oportunidad%' AND w.targetObjectID = 'Valor'


