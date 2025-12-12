SELECT *
FROM PROYECTOSIAV2.dbo.fn_TG_TMP_Obtener_Cambios_insertar_prima()

INSERT INTO TG_TMP_LOG (identificador, negocio, fecha_registro)
SELECT Identificador, 'PRI', GETDATE()
FROM PROYECTOSIAV2.dbo.fn_TG_TMP_Obtener_Cambios_insertar();