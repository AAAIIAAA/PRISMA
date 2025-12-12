USE [TeamMate_Prima]

SET ANSI_NULLS ON


SET QUOTED_IDENTIFIER ON


CREATE TABLE [dbo].[TM_ObjectAction](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[TMGUID] [char](32) NOT NULL,
	[ObjectID] [int] NOT NULL,
	[ObjectTypeLID] [int] NOT NULL,
	[TypeLID] [int] NOT NULL,
	[ActionDate] [datetime] NULL,
	[UserID] [int] NULL,
	[ReasonLID] [int] NOT NULL,
	[Flag] [int] NULL,
	[OldRID] [int] NULL,
	[LMG] [char](32) NOT NULL,
	[LMD] [datetime] NOT NULL,
	[LMU] [nvarchar](100) NOT NULL,
	[FollowedByEdit] [tinyint] NOT NULL,
 CONSTRAINT [PK_TM_ObjectAction_ID] PRIMARY KEY NONCLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = OFF) ON [PRIMARY]
) ON [PRIMARY]


ALTER TABLE [dbo].[TM_ObjectAction] SET (LOCK_ESCALATION = DISABLE)


ALTER TABLE [dbo].[TM_ObjectAction] ADD  CONSTRAINT [df_TM_ObjectAction_ActionDate]  DEFAULT (getutcdate()) FOR [ActionDate]


ALTER TABLE [dbo].[TM_ObjectAction] ADD  DEFAULT ((0)) FOR [ReasonLID]


ALTER TABLE [dbo].[TM_ObjectAction] ADD  DEFAULT ((0)) FOR [FollowedByEdit]


ALTER TABLE [dbo].[TM_ObjectAction]  WITH NOCHECK ADD  CONSTRAINT [FK_TM_ObjectAction_03] FOREIGN KEY([UserID])
REFERENCES [dbo].[TM_User] ([ID])


ALTER TABLE [dbo].[TM_ObjectAction] NOCHECK CONSTRAINT [FK_TM_ObjectAction_03]


ALTER TABLE [dbo].[TM_ObjectAction]  WITH NOCHECK ADD  CONSTRAINT [FK_TM_ObjectAction_04] FOREIGN KEY([UserID])
REFERENCES [dbo].[TM_User] ([ID])


ALTER TABLE [dbo].[TM_ObjectAction] NOCHECK CONSTRAINT [FK_TM_ObjectAction_04]


ALTER TABLE [dbo].[TM_ObjectAction]  WITH NOCHECK ADD  CONSTRAINT [CK_TM_ObjectAction_01] CHECK  (([ObjectTypeLID]=(4) OR [ObjectTypeLID]=(6) OR [ObjectTypeLID]=(11)))


ALTER TABLE [dbo].[TM_ObjectAction] NOCHECK CONSTRAINT [CK_TM_ObjectAction_01]


ALTER TABLE [dbo].[TM_ObjectAction]  WITH NOCHECK ADD  CONSTRAINT [CK_TM_ObjectAction_02] CHECK  (([ObjectTypeLID]=(4) OR [ObjectTypeLID]=(6) OR [ObjectTypeLID]=(11)))


ALTER TABLE [dbo].[TM_ObjectAction] NOCHECK CONSTRAINT [CK_TM_ObjectAction_02]


ALTER TABLE [dbo].[TM_ObjectAction]  WITH NOCHECK ADD  CONSTRAINT [CK_TM_ObjectAction_03] CHECK  (([FollowedByEdit]=(0) OR [FollowedByEdit]=(1)))


ALTER TABLE [dbo].[TM_ObjectAction] NOCHECK CONSTRAINT [CK_TM_ObjectAction_03]



