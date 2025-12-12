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
 AND RA.TypeLID IN (14,15,16,17) WHERE 
 RE.TrackFlag = 1 and CV.Name NOT LIKE '%Oportunidad%' AND L.targetObjectID = Valor
