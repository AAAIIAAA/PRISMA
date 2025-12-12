DELETE FROM PROYECTOSIAV2.dbo.TG_Proyecto_Riesgo_Control
WHERE 'PRI-'+ CONVERT(VARCHAR,[Referencia_del_proceso])+'-'+CONVERT(VARCHAR,[NroControl])+'-'+
CONVERT(VARCHAR,[NroRiesgo])  IN 
(SELECT Identificador FROM PROYECTOSIAV2.dbo.fn_TG_RC_Obtener_Cambios_eliminar_to_compare_prima());