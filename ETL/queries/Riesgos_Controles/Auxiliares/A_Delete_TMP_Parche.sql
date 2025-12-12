
delete from TG_TMP where Referencia_del_Proceso in(
select distinct Referencia_del_Proceso from TG_TMP where Referencia_del_Proceso in (
SELECT DISTINCT REPLACE(LTRIM(RTRIM(tgp.Codigo)), ' ', '') AS CodigoSinEspacios
FROM TG_Proyecto TGP
LEFT JOIN TG_Proyecto_Actividad_Informe TGPA ON TGPA.IdProyecto = TGP.IdProyecto
WHERE TGP.IdPlanAnual = 14
  AND (
    TGPA.FechaRevisado IS NOT NULL
    OR TGP.IdProyecto NOT IN (
      SELECT IdProyecto
      FROM TG_Proyecto_Actividad_Informe
      WHERE IdActividad = 15
    )
  )
)
);

delete from TG_TMP_TO_COMPARE where Referencia_del_Proceso in(
select distinct Referencia_del_Proceso from TG_TMP where Referencia_del_Proceso in (
SELECT DISTINCT REPLACE(LTRIM(RTRIM(tgp.Codigo)), ' ', '') AS CodigoSinEspacios
FROM TG_Proyecto TGP
LEFT JOIN TG_Proyecto_Actividad_Informe TGPA ON TGPA.IdProyecto = TGP.IdProyecto
WHERE TGP.IdPlanAnual = 14
  AND (
    TGPA.FechaRevisado IS NOT NULL
    OR TGP.IdProyecto NOT IN (
      SELECT IdProyecto
      FROM TG_Proyecto_Actividad_Informe
      WHERE IdActividad = 15
    )
  )
)
)
