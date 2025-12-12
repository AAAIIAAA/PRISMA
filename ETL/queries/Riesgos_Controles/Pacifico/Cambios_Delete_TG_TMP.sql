DELETE FROM PROYECTOSIAV2.dbo.TG_TMP
WHERE Identificador IN 
(SELECT Identificador FROM PROYECTOSIAV2.dbo.fn_TG_TMP_Obtener_Cambios_eliminar_to_compare());
