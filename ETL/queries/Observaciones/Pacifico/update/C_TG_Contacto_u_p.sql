SET QUOTED_IDENTIFIER ON;
UPDATE C
SET C.Email = U.Email,
C.Nombre = U.FirstName,
C.Apellido = U.LastName

FROM (SELECT * FROM PROYECTOSIAV2.dbo.TG_Contacto WHERE ID LIKE '%PS%') C 
LEFT JOIN TeamMateR12.dbo.TM_User U ON C.ID = 'PS-'+CONVERT(VARCHAR,U.ID)
WHERE C.ID IS NOT NULL AND 
(
(C.Email COLLATE Modern_Spanish_CI_AS NOT LIKE U.Email COLLATE Modern_Spanish_CI_AS)
or
(C.Apellido COLLATE Modern_Spanish_CI_AS NOT LIKE U.LastName COLLATE Modern_Spanish_CI_AS)
or
(C.Nombre COLLATE Modern_Spanish_CI_AS NOT LIKE U.FirstName COLLATE Modern_Spanish_CI_AS)
)
Select 1 as flag