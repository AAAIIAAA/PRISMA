UPDATE CC
SET CC.Analítico = ISNULL(CV.Name,'')
FROM (select * from TG_TMP where SUBSTRING(Identificador, 1, 2) = 'PS' ) CC LEFT JOIN TeamMateR12.dbo.V_TM_Procedure PR ON PR.ProjectID = CC.[ID Proyecto] AND PR.ID = CC.[ID Procedimiento]
	LEFT JOIN TeamMateR12.dbo.TM_CategoryValue CV ON CV.CategoryID = PR.ControlEffectivenessCID AND CV.Culture = 'es-ES'

