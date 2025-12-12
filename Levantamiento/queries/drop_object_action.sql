USE [TeamMate_Prima]

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[TM_ObjectAction]') AND type in (N'U'))
DROP TABLE [dbo].[TM_ObjectAction]
