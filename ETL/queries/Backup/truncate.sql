
DECLARE @TablasATruncar TABLE (NombreTabla NVARCHAR(255))
INSERT INTO @TablasATruncar VALUES ('TM_Recommendation'),
 ('TM_RecommendationAction'), ('TM_Issue'), ('TM_Schedule'), 
 ('TM_Project'),('TM_CategoryValue'),('TM_SecurityGroup'),('TM_Auditor'),
 ('TM_SecurityGroupToUser'), ('TM_ProjectToOrgHierarchy'), ('TM_Program'), 
 ('TM_Procedure'), ('TM_List_RecommendationStatus'), ('TM_List_RecActionType'),
  ('TM_List_ProjectStatus'), ('TM_List_AuthRecRole'), ('TM_Link'), 
  ('EWP_RiskToControl'), ('TM_Browser'),('EWP_Risk'), ('EWP_Project'), 
  ('EWP_EntityToRisk'), ('EWP_Control'),('TM_AuthRecommendation'),
  ('TM_ObjectAction'),('TM_User')


DECLARE @sqlDisableConstraints NVARCHAR(MAX) = ''
SELECT @sqlDisableConstraints += 'ALTER TABLE ' + NombreTabla + ' NOCHECK CONSTRAINT all;' FROM @TablasATruncar
EXEC sp_executesql @sqlDisableConstraints


DECLARE @sqlTruncateTables NVARCHAR(MAX) = ''
SELECT @sqlTruncateTables += 'TRUNCATE TABLE ' + NombreTabla + ';' FROM @TablasATruncar
EXEC sp_executesql @sqlTruncateTables


DECLARE @sqlEnableConstraints NVARCHAR(MAX) = ''
SELECT @sqlEnableConstraints += 'ALTER TABLE ' + NombreTabla + ' WITH CHECK CHECK CONSTRAINT all;' FROM @TablasATruncar
EXEC sp_executesql @sqlEnableConstraints
