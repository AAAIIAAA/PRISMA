EXCEL_PATH = r'E:\Sharepoint\Pacífico Compañía de Seguros y Reaseguros\Analítica e Innovación en Auditoría - 01. Resultados Scripts\apps_innovacion\Auditron - Calidad\Results Calidad'
EXCEL_IMAGENES_PATH = r'E:\Sharepoint\Pacífico Compañía de Seguros y Reaseguros\Analítica e Innovación en Auditoría - 01. Resultados Scripts\apps_innovacion\Auditron - GeneracionInforme\ResultInforme'
PEAS_PATH = r'E:\Sharepoint\Pacífico Compañía de Seguros y Reaseguros\Analítica e Innovación en Auditoría - 01. Resultados Scripts\apps_innovacion\Auditron - GeneracionPEA\Result'
FINAL_PATH_IMAGEN = r'E:\Sharepoint\Pacífico Compañía de Seguros y Reaseguros\Analítica e Innovación en Auditoría - 01. Resultados Scripts\apps_innovacion\Auditron - GeneracionInforme\OutputInforme'
PEAS_PATH_OUTPUT = r'E:\Sharepoint\Pacífico Compañía de Seguros y Reaseguros\Analítica e Innovación en Auditoría - 01. Resultados Scripts\apps_innovacion\Auditron - GeneracionPEA\output'


INFORME_PATH = r'E:\Sharepoint\Pacífico Compañía de Seguros y Reaseguros\Analítica e Innovación en Auditoría - 01. Resultados Scripts\apps_innovacion\Auditron - GeneracionInforme\ResultInforme'
PLANTILLAS_PS_PATH = r'E:\Proyectos\Calidad_Forma\plantillas_final\PACIFICO'
PLANTILLAS_PRI_PATH = r'E:\Proyectos\Calidad_Forma\plantillas_final\PRIMA'
PLANTILLAS_EPS_PATH = r'E:\Proyectos\Calidad_Forma\plantillas_final\SALUD'
PLANTILLAS_CRE_PATH = r'E:\Proyectos\Calidad_Forma\plantillas_final\CREDISEGURO'
PRUEBA_EXPORT= r'E:\Proyectos\Calidad_Forma\results'
CNXN_TIGA = r'Driver={ODBC Driver 17 for SQL Server};database=PROYECTOSIAV2;encrypt=no;integrated security=False;min_tls=1.0;port=1433;server=PSTMMPRD0300;trusted_connection=no;uid=USTEAM02;pwd=ZU4repezaGefraMu'
QUERIES_PATH = r'E:\Proyectos\Calidad_Forma\Querys'
RESULTS_PATH = r'E:\Sharepoint\Pacífico Compañía de Seguros y Reaseguros\Analítica e Innovación en Auditoría - 01. Resultados Scripts\apps_innovacion\Auditron - Calidad\Output Calidad'
FINAL_PATH = r'E:\Sharepoint\Pacífico Compañía de Seguros y Reaseguros'

MAPAYEVOLUTIVO_PATH=r'E:\Sharepoint\Pacífico Compañía de Seguros y Reaseguros\Analítica e Innovación en Auditoría - 01. Resultados Scripts\apps_innovacion\Auditron - GeneracionInforme\OutputInforme'

IMAGENES_PATH =r'E:\Proyectos\Calidad_Forma\IMAGENES'

MAPA_ASEGURAMIENTO_PATH = r'E:\Sharepoint\Pacífico Compañía de Seguros y Reaseguros\Auditoria Interna - Migración TeamStore'


memorando_list = [
        {"Nombre_evaluacion": "EVALUACION", "Codigo_evaluacion": "CODIGO"},
        {},
        {"Nombre_product_owner": "PRODUCT_OWNER", "Nombre_scrum_master": "SCRUM_MASTER", "Nombre_scrum_team_1": "SCRUM_TEAM_1", "Nombre_scrum_team_2": "SCRUM_TEAM_2"},
        {"Fecha_inicio_auditoria": "FECHA_INICIO", "Fecha_emisión_borrador_informe": "FECHA_BORRADOR", "Fecha_emisión_informe": "FECHA_EMISION_INFORME", "Fecha_fin_auditoria": "FECHA_FIN"}
    ]

primera_slide_dict = {"Nombre_evaluacion": "EVALUACION", "Codigo_evaluacion": "CODIGO"}

observaciones_list = [
        {"Unidad_auditada_n":"UNIDAD_RESPONSABLE","Titulo_observación_n": "TITULO", "Descripcion_observación_n": "OBSERVACION",
        "Recomendación_observación_n":"RECOMENDACION","Plan_de_acción_observación_n":"PLAN",
        "Responsable_observación_n":"PROPIETARIO","Estado_observación_n":"ESTADO",
        "Fecha_observación_n":"FECHA"},
        
    ]



calificativo_total_list = [
    {},
    {},
        {"Calificativo_p":"CALIFICATIVO","Efectividad_p": "PORCENTAJE_CALIFICATIVO", "Nro_control_p": "CONTROLES"},
        {"valor_ifc_total_inicial":"IFC_INHERENTE","valor_ifc_total_residual":"IFC_RESIDUAL"}
        
    ]

calificativo_unidad_responsable_list = [
    {},
    {},
        {"Unidad_auditada":"UNIDAD_RESPONSABLE","Calificativo":"CALIFICATIVO","Efectividad": "PORCENTAJE_CALIFICATIVO", "Nro_control": "CONTROLES"}
       
        
    ]

cantidad_controles_list = [
    {},
    {},
        {
            "E_c":"EFECTIVOS_CRITICO","E_a":"EFECTIVOS_ALTO","E_r": "EFECTIVOS_RELEVANTE", "E_m": "EFECTIVOS_MODERADO","E_b":"EFECTIVOS_BAJO","T_efec":"EFECTIVOS_TOTAL",
            "Enf_c":"EFECTIVO_NO_FORMALIZADO_CRITICO","Enf_a":"EFECTIVO_NO_FORMALIZADO_ALTO","Enf_r": "EFECTIVO_NO_FORMALIZADO_RELEVANTE", "Enf_m": "EFECTIVO_NO_FORMALIZADO_MODERADO","Enf_b":"EFECTIVO_NO_FORMALIZADO_BAJO","T_efe_n":"EFECTIVO_NO_FORMALIZADO_TOTAL",
            "Ip_c":"INEFECTIVO_PRUEBA_CRITICO","Ip_a":"INEFECTIVO_PRUEBA_ALTO","Ip_r": "INEFECTIVO_PRUEBA_RELEVANTE", "Ip_m": "INEFECTIVO_PRUEBA_MODERADO","Ip_b":"INEFECTIVO_PRUEBA_BAJO","T_inef_p":"INEFECTIVO_PRUEBA_TOTAL",
            "Id_c":"INEFECTIVO_DISEÑO_CRITICO","Id_a":"INEFECTIVO_DISEÑO_ALTO","Id_r": "INEFECTIVO_DISEÑO_RELEVANTE", "Id_m": "INEFECTIVO_DISEÑO_MODERADO","Id_b":"INEFECTIVO_DISEÑO_BAJO","T_inef_d":"INEFECTIVO_DISEÑO_TOTAL",
            "Ci_c":"CONTROL_INEXISTENTE_CRITICO","Ci_a":"CONTROL_INEXISTENTE_ALTO","Ci_r": "CONTROL_INEXISTENTE_RELEVANTE", "Ci_m": "CONTROL_INEXISTENTE_MODERADO","Ci_b":"CONTROL_INEXISTENTE_BAJO","T_inex":"CONTROL_INEXISTENTE_TOTAL",
            "T_critico":"CONTROL_CRITICO_TOTAL","T_alto":"CONTROL_ALTO_TOTAL","T_relevante": "CONTROL_RELEVANTE_TOTAL", "T_mode": "CONTROL_MODERADO_TOTAL","T_bajo":"CONTROL_BAJO_TOTAL","T_contr":"TOTAL_CONTROLES"
        }  
    ]

observaciones_informe_list = [
    {},
    {},
        {
            "Titulo_observación":"TITULO_OBSERVACION","Criticidad_obs":"RIESGO"
            
        }  
    ]

memorando_list = [
    {"Nombre_evaluacion":"EVALUACION","Codigo_evaluacion":"CODIGO"},
    {},
        {},
        {"valor_fecha_inicio":"FECHA_INICIO","valor_fecha_fin":"FECHA_FIN","valor_fecha_emision":"FECHA_BORRADOR","valor_fecha_de_emisión_final":"FECHA_EMISION_INFORME"
        
        },{},{},{},{"Nombre_de_product_owner":"PRODUCT_OWNER","Nombre_de_scrum_master":"SCRUM_MASTER",
        "Nombre_de_scrum_team_1":"SCRUM_TEAM_1","Nombre_de_scrum_team_2":"SCRUM_TEAM_2"}
    ]

#MAPA DE ASEGURAMIENTO

list_ruta_negocio = [
    "01. Pacífico Seguros",
    "02. Prima AFP",
    "03. Pacífico Salud",
    "04. Crediseguro"
    ]
