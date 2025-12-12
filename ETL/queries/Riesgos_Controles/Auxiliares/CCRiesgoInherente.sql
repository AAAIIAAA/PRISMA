SELECT CV3.Name IMP_INH, CV4.Name FRE_INH 
FROM EWP_RiskToControl RTC JOIN EWP_EntityToRisk ETR 
ON ETR.RiskID = RTC.RiskID JOIN EWP_Risk R
 ON R.ID = RTC.RiskID  JOIN EWP_Control C 
 ON C.ID = RTC.ControlID JOIN TM_ProjectToOrgHierarchy PTOH 
 ON PTOH.ID = ETR.ProjectToOrgHierarchyID  LEFT JOIN TM_CategoryValue CV3 
 ON CV3.CategoryID = R.UserCategory3CID 
 AND CV3.Culture LIKE 'es-ES' LEFT JOIN TM_CategoryValue CV4 
 ON CV4.CategoryID = R.UserCategory4CID AND CV4.Culture LIKE 'es-ES' 
 WHERE PTOH.ProjectID  = Valor1 And R.ID = Valor2 And C.ID = Valor3
