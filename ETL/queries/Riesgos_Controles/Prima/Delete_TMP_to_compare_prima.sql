DELETE FROM PROYECTOSIAV2.dbo.TG_TMP_TO_COMPARE
WHERE Identificador IN 
(SELECT Identificador FROM PROYECTOSIAV2.dbo.fn_TG_TMP_Obtener_Cambios_eliminar_to_compare_prima());
