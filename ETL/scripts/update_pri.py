from scripts.funciones import *
from conection import *
import os
import pandas as pd
from datetime import datetime


columnas_insert = ["Identificador","Referencia_del_Proceso", "Descripción del Proceso", "Descripción del Subproceso",
        "N° Riesgo", "Causa", "Evento", "Consecuencia", "Categoría del Riesgo","Tipo de Riesgo",
        "Impacto", "Impacto (en US$ miles)", "Frecuencia","Frecuencia (veces por año)", "IFC (en US$ miles)","IFC",
        "N° Control", "Descripción del Control", "Objetivo Relacionado a la Unidad Auditada", "P4","P5", "P6", "P7",
        "P8", "P9","P10", "P11","P12","P13", "P14", "P15", "P16", "P17", "Control_Clave", "Control_Sox", "Control Regulatorio",
        "Nombre de la Herramienta/Sistema", "Unidad Responsable del Control","I","P", "V", "R", "EX", "IN", "VA", "PR",
        "DO","Tipo de Controles", "Naturaleza del Control", "Plan de Pruebas",  "Ponderado del Control","Evaluación del Control",
        "PP4", "PP5", "PP6", "PP7", "PP8", "PP9", "PP10", "PP11", "PP12", "PP13", "PP14", "PP15", "PP16", "PP17", "Referencia Deficiencias Observadas",
        "Impacto2", "Impacto (en US$ miles)2", "Frecuencia2", "Frecuencia (veces por año)2","IFC (en US$ miles)2", "IFC2",
        "Referencia del Proceso anterior", "Clasificación del Riesgo de Trabajo", "Código", "Título", "Status", "Fecha de Cambio",
        "ID Proyecto", "ID Riesgo", "ID Control","ID Procedimiento", "SubGerencia","FechaEmisión",  "Modificado", "Eliminado",
        "Macroproceso", "Negocio", "Adm_Riesgo", "Puntuación","Área Responsable", "Finalizado","CuentaContable"]
        
matriz = pd.DataFrame(columns=columnas_insert)



def update_pri():
    
    
    
    ds1, ds2, ds3, ds4, ds5, ds6, ds7 = [pd.DataFrame() for _ in range(7)]
    
    cot_controles_clave = 0
    cot_controles_sox = 0
    solicitud = ""
    avance = 0
    i = 0
    temp, temp1, temp2, temp3 = "", "", "", ""
    valoradm = 0.0
    cont = 0
    avance = 20
    
    print(f"Progreso: {avance}%")
    ds1 = obtener_query_TIGA(os.path.join(QUERIES_PRIMA_RIESGOS_CONTROLES_PATH, 'Cambios_update_prima.sql'))

    
    for idx, rd in ds1.iterrows():
       

        cont += 1
        modificado = 0
        
        temp, temp1, temp2, temp3 = "", "", "", ""
        
        matriz.at[i, "Identificador"] = rd["Identificador"]
        matriz.at[i, "SubGerencia"] = rd["SubGerencia"]
        matriz.at[i, "Referencia_del_Proceso"] = rd["Referencia_del_Proceso"]
        matriz.at[i, "Descripción del Proceso"] = rd["Descripción del proceso"]
        print(rd["Referencia_del_Proceso"])
        matriz.at[i, "Descripción del Subproceso"] = rd["Descripción del subproceso"]
        matriz.at[i, "N° Riesgo"] = rd["N° Riesgo"]

        matriz.at[i, "Causa"] = causa_evento_consecuencia(rd["Descripcion"], "Causa")
        matriz.at[i, "Evento"] = causa_evento_consecuencia(rd["Descripcion"], "Evento")
        matriz.at[i, "Consecuencia"] = causa_evento_consecuencia(rd["Descripcion"], "Consecuencia")
        

        if not pd.isnull(rd["UserCategory1CID"]) and rd["UserCategory1CID"]!='N/A':
            
            temp = categoría_pri(rd["UserCategory1CID"])

            if temp:
                matriz.at[i, "Categoría del Riesgo"] = cat_riesgo(temp, "Categoría")
                matriz.at[i, "Tipo de Riesgo"] = cat_riesgo(temp, "Tipo")
        else:
            matriz.at[i, "Categoría del Riesgo"] = ""
            matriz.at[i, "Tipo de Riesgo"] = ""
    

        matriz.at[i, "ID Proyecto"] = rd["ID Proyecto"]
        matriz.at[i, "ID Riesgo"] = rd["ID Riesgo"]
        matriz.at[i, "ID Control"] = rd["ID Control"]
        matriz.at[i, "ID Procedimiento"] = rd["ID Procedimiento"]

        temp = open(os.path.join(QUERIES_PRIMA_RIESGOS_CONTROLES_PATH, f'PRI_CCModificaciones.sql'), 'r', encoding='utf-8-sig').read()
   
        temp = temp.replace("'ValorPR'", str(rd["ID Proyecto"])).replace("'ValorR'", str(rd["ID Riesgo"])).replace("'ValorC'", str(rd["ID Control"])).replace("'ValorPC'", str(rd["ID Procedimiento"]))
        temp1 = temp
        temp2 = temp
        temp3 = temp
        temp += " And ValorModificado = 'Impacto' order by ID desc"
        ds5 = obtener_query_tiga(temp)

        if not ds5.empty:
            matriz.at[i, "Impacto (en US$ miles)"] = ds5.iloc[0, 9]
            matriz.at[i, "Impacto"] = cálculo_editar_pri(matriz.at[i, "Impacto (en US$ miles)"], "Impacto",rd["IdPlan"])
            modificado = 1
        else:
            matriz.at[i, "Impacto"] = riesgo_inherente_pri(rd["ID Proyecto"], rd["ID Riesgo"], rd["ID Control"], "Impacto")
            matriz.at[i, "Impacto (en US$ miles)"] = cálculo_riesgo_pri(matriz.at[i, "Impacto"], "Impacto", rd["IdPlan"])

        temp1 += " And ValorModificado = 'Frecuencia' order by ID desc"
        ds5 = obtener_query_tiga(temp1)

        if not ds5.empty:
            matriz.at[i, "Frecuencia (veces por año)"] = ds5.iloc[0, 9]
            matriz.at[i, "Frecuencia"] = cálculo_editar_pri(matriz.at[i, "Frecuencia (veces por año)"], "Frecuencia",rd["IdPlan"])
            modificado = 1
        else:
            matriz.at[i, "Frecuencia"] = riesgo_inherente_pri(rd["ID Proyecto"], rd["ID Riesgo"], rd["ID Control"], "Frecuencia")
            matriz.at[i, "Frecuencia (veces por año)"] = cálculo_riesgo_pri(matriz.at[i, "Frecuencia"], "Frecuencia", rd["IdPlan"])

        temp2 += " And ValorModificado = 'Referencia a Proyecto Anterior' order by ID desc"
        ds5 = obtener_query_tiga(temp2)

        if not ds5.empty:
            matriz.at[i, "Referencia del Proceso anterior"] = ds5.iloc[0, 9]
            modificado = 1
        else:
            matriz.at[i, "Referencia del Proceso anterior"] = ""

        matriz.at[i, "Modificado"] = 1 if modificado > 0 else 0

        matriz.at[i, "IFC (en US$ miles)"] = float(matriz.at[i, "Frecuencia (veces por año)"]) * float(matriz.at[i, "Impacto (en US$ miles)"])
        
        matriz.at[i, "IFC"] = ifc_pri(matriz.at[i, "IFC (en US$ miles)"])

        if matriz.at[i, "IFC (en US$ miles)"] == 0:
            matriz.at[i, "IFC (en US$ miles)"] = ""

        if not pd.isnull(rd["N° Control"]) and rd["N° Control"]!='N/A':
            matriz.at[i, "N° Control"] = rd["N° Control"]

        if not pd.isnull(rd["Descripción del Control"]) and rd["Descripción del Control"]!='N/A':
            matriz.at[i, "Descripción del Control"] = rd["Descripción del Control"]

        if not pd.isnull(rd["Objetivo Relacionado a la Unidad Auditada"]) and rd["Objetivo Relacionado a la Unidad Auditada"]!='N/A':
            matriz.at[i, "Objetivo Relacionado a la Unidad Auditada"] = rd["Objetivo Relacionado a la Unidad Auditada"]

        for j in range(15, 21):
            if not pd.isnull(rd.iloc[j]) and rd.iloc[j]!='N/A':
                
                temp = categoría_pri(rd.iloc[j])
                
                temp = principios_c(temp)
                if temp != 0:
                    matriz.at[i, f"P{temp}"] = "X"

        if str(matriz.at[i, "IFC (en US$ miles)"]) != "":
            matriz.at[i, "Control_Clave"] = cont_clave_pri(matriz.at[i, "IFC (en US$ miles)"], matriz.at[i, "Impacto (en US$ miles)"],rd["IdPlan"])

        matriz.at[i, "Control_Sox"] = rd["Control_Sox"]
        matriz.at[i, "Control Regulatorio"] = rd["Control Regulatorio"]
        

        if not pd.isnull(rd["Nombre de la Herramienta/Sistema"]) and rd["Nombre de la Herramienta/Sistema"]!='N/A':
            matriz.at[i, "Nombre de la Herramienta/Sistema"] = categoría_pri(rd["Nombre de la Herramienta/Sistema"])
        
        if not pd.isnull(rd["Unidad Responsable del Control"]) and rd["Unidad Responsable del Control"]!='N/A':
            matriz.at[i, "Unidad Responsable del Control"] = categoría_pri(rd["Unidad Responsable del Control"])

        if not pd.isnull(rd["I-P-V-R"]) and rd["I-P-V-R"]!='N/A':
            temp = categoría_pri(rd["I-P-V-R"])
            matriz.at[i, "I"] = control_apl(temp, "C")

        if not pd.isnull(rd["I-P-V-R"]) and rd["I-P-V-R"]!='N/A':
            temp = categoría_pri(rd["I-P-V-R"])
            matriz.at[i, "P"] = control_apl(temp, "A")

        if not pd.isnull(rd["I-P-V-R"]) and rd["I-P-V-R"]!='N/A':
            temp = categoría_pri(rd["I-P-V-R"])
            matriz.at[i, "V"] = control_apl(temp, "V")

        if not pd.isnull(rd["I-P-V-R"]) and rd["I-P-V-R"]!='N/A':
            temp = categoría_pri(rd["I-P-V-R"])
            matriz.at[i, "R"] = control_apl(temp, "R")

        if not pd.isnull(rd["EX-IN-VA-PR-DO"]) and rd["EX-IN-VA-PR-DO"]!='N/A':
            temp = categoría_pri(rd["EX-IN-VA-PR-DO"])
            matriz.at[i, "EX"] = aseveraciones(temp, "EX")

        if not pd.isnull(rd["EX-IN-VA-PR-DO"]) and rd["EX-IN-VA-PR-DO"]!='N/A':
            temp = categoría_pri(rd["EX-IN-VA-PR-DO"])
            matriz.at[i, "IN"] = aseveraciones(temp, "IN")

        if not pd.isnull(rd["EX-IN-VA-PR-DO"]) and rd["EX-IN-VA-PR-DO"]!='N/A':
            temp = categoría_pri(rd["EX-IN-VA-PR-DO"])
            matriz.at[i, "VA"] = aseveraciones(temp, "VA")

        if not pd.isnull(rd["EX-IN-VA-PR-DO"]) and rd["EX-IN-VA-PR-DO"]!='N/A':
            temp = categoría_pri(rd["EX-IN-VA-PR-DO"])
            matriz.at[i, "PR"] = aseveraciones(temp, "PR")

        if not pd.isnull(rd["EX-IN-VA-PR-DO"]) and rd["EX-IN-VA-PR-DO"]!='N/A':
            temp = categoría_pri(rd["EX-IN-VA-PR-DO"])
            matriz.at[i, "DO"] = aseveraciones(temp, "DO")

        if not pd.isnull(rd["Tipo de Controles"]) and rd["Tipo de Controles"]!='N/A':
            matriz.at[i, "Tipo de Controles"] = categoría_pri(rd["Tipo de Controles"])

        if not pd.isnull(rd["Naturaleza del Control"]) and rd["Naturaleza del Control"]!='N/A':
            matriz.at[i, "Naturaleza del Control"] = categoría_pri(rd["Naturaleza del Control"])

        if not pd.isnull(rd["Plan de Pruebas"]) and rd["Plan de Pruebas"]!='N/A':
            temp = remove_html2(rd["Plan de Pruebas"])
            matriz.at[i, "Plan de Pruebas"] = clear_html_text(temp)
        
        

        if not pd.isnull(rd["Ponderado del Control"]) and rd["Ponderado del Control"]!='N/A':
            matriz.at[i, "Ponderado del Control"] = categoría_pri(rd["Ponderado del Control"])
            matriz.at[i, "Ponderado del Control"] = matriz.at[i, "Ponderado del Control"][:2].strip()
            matriz.at[i, "Evaluación del Control"] = categoría_pri(rd["Ponderado del Control"])
            temp = len(matriz.at[i, "Evaluación del Control"])
            matriz.at[i, "Evaluación del Control"] = matriz.at[i, "Evaluación del Control"][4:temp].strip()
        else:
            matriz.at[i, "Ponderado del Control"] = 0
            matriz.at[i, "Evaluación del Control"] = ""

        ds2 = observaciones_pri(rd["ID Procedimiento"])
        
        for k in range(6):
            if not ds2.empty:
                if not pd.isnull(ds2.iloc[0, k]) and ds2.iloc[0, k]!='N/A':
                    temp = categoría_pri(ds2.iloc[0, k])
                    temp = principios_c(temp)
                    if temp != 0:
                        matriz.at[i, f"PP{temp}"] = "X"

        temp = ""
        
        if not ds2.empty:
            
            for index, row in ds2.iterrows():
                
              
                temp += "," + str(row['id'])

        matriz.at[i, "Referencia Deficiencias Observadas"] = temp.strip()[1:]
        matriz.at[i, "Impacto2"] = matriz.at[i, "Impacto"]
        matriz.at[i, "Impacto (en US$ miles)2"] = matriz.at[i, "Impacto (en US$ miles)"]
        matriz.at[i, "Frecuencia (veces por año)2"] = riesgo_res(matriz.at[i, "Frecuencia (veces por año)"], matriz.at[i, "Ponderado del Control"])
        matriz.at[i, "Frecuencia2"] = frecuencia_r(matriz.at[i, "Frecuencia (veces por año)2"])
        matriz.at[i, "IFC (en US$ miles)2"] = float(matriz.at[i, "Frecuencia (veces por año)2"]) * float(matriz.at[i, "Impacto (en US$ miles)2"])
        matriz.at[i, "IFC2"] = ifc_pri(matriz.at[i, "IFC (en US$ miles)2"])

        
        
        matriz.at[i, "FechaEmisión"] = rd["Emisión"].strftime("%d/%m/%Y")
        
        if matriz.at[i, "Referencia_del_Proceso"].startswith(("AIP")):
            matriz.at[i, "Negocio"] = "Negocio de Pensiones"
        
        else:
            matriz.at[i, "Negocio"] = "Negocio de Prestación"

        temp3 += " And ValorModificado = 'Eliminado' order by ID desc"
        ds5 = obtener_query_tiga(temp3)
        if not ds5.empty:
            matriz.at[i, "Eliminado"] = ds5.iloc[0, 9]
        else:
            matriz.at[i, "Eliminado"] = 0

        query2 = open(os.path.join(QUERIES_PRIMA_RIESGOS_CONTROLES_PATH, f'PRI_CITipoRiesgo.sql'), 'r', encoding='utf-8-sig').read()
        ds6 = obtener_query_tiga(query2)

        for rd2 in ds6.itertuples():
            if matriz.at[i, "Referencia_del_Proceso"] == rd2[1]:
                matriz.at[i, "Clasificación del Riesgo de Trabajo"] = rd2[2]
                matriz.at[i, "Macroproceso"] = rd2[3]

        
        tmp = open(os.path.join(QUERIES_PRIMA_RIESGOS_CONTROLES_PATH, f'PRI_CC_Proceso.sql'), 'r', encoding='utf-8-sig').read()
        tmp = tmp.replace("Val1", str(matriz.at[i, "ID Proyecto"]))
        tmp = tmp.replace("Val2", str(matriz.at[i, "ID Riesgo"]))
        tmp = tmp.replace("Val3", str(matriz.at[i, "ID Control"]))
        tmp = tmp.replace("Val4", str(matriz.at[i, "ID Procedimiento"]))
        ds_proceso = obtener_query_tiga(tmp)

        for rd2 in ds_proceso.itertuples():
            matriz.at[i, "Macroproceso"] = rd2[1]

        valoradm = 0
        
        if float(matriz.at[i, "Ponderado del Control"]) == 1:
            valoradm = 1
        elif float(matriz.at[i, "Ponderado del Control"]) == 2:
            valoradm = 0.75
        elif float(matriz.at[i, "Ponderado del Control"]) == 3:
            valoradm = 0.5
        elif float(matriz.at[i, "Ponderado del Control"]) == 4:
            valoradm = 0.25
        

        if float(matriz.at[i, "Control_Sox"]) == 1 and valoradm == 1:
            matriz.at[i, "Adm_Riesgo"] = 1
        elif float(matriz.at[i, "Control_Sox"]) == 1 and float(matriz.at[i, "Ponderado del Control"]) > 1:
            matriz.at[i, "Adm_Riesgo"] = 0
        else:
            matriz.at[i, "Adm_Riesgo"] = valoradm

        if str(matriz.at[i, "IFC (en US$ miles)"]) == "":
            matriz.at[i, "IFC (en US$ miles)"] = 0.0

        matriz.at[i, "Puntuación"] = float(matriz.at[i, "IFC (en US$ miles)"]) * float(matriz.at[i, "Adm_Riesgo"])
        matriz.at[i, "Área Responsable"] = categoría_pri(rd["Área Responsable"])
        matriz.at[i, "Finalizado"] = rd["Finalizado"]

        if not pd.isnull(rd["CuentaContable"]) and rd["CuentaContable"]!='N/A':
            temp = remove_html2(rd["CuentaContable"])
            matriz.at[i, "CuentaContable"] = clear_html_text(temp)
        
        i+=1

        
    filas , columnas = matriz.shape
    print("filas a insertar o actulizar: ", filas)
    
    avance = 40
    print(f"Progreso: {avance}%")



    conexion_tiga = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};'
        'Database=PROYECTOSIAV2;'
        'Encrypt=no;'
        'Integrated Security=False;'
        'Min_TLS=1.0;'
        'Port=1433;'
        'Server=PSTMMPRD0300;'
        'Trusted_Connection=no;'
        'UID=USTEAM02;'
        'PWD=ZU4repezaGefraMu'
    )
    cursor = conexion_tiga.cursor()
    

    with open("log.txt", "a") as log_file:
        for idx, dr in matriz.iterrows():
            print("fila afectada en TG_TMP")
            
            
            log_file.write(f"Referencia del proceso actualizada: {dr['Referencia_del_Proceso']}\n")
            
            update_query = f"""
            SET LANGUAGE SPANISH;
            UPDATE dbo.TG_TMP SET {get_update_values(dr, matriz.columns)} WHERE [Identificador] = '{dr["Identificador"]}'
            """
            cursor.execute(update_query)
            cursor.commit()

    

   
    avance = 60
    print(f"Progreso: {avance}%")

    rows_update_tmp_to_compare_pri = execute_query_TIGA(os.path.join(QUERIES_PRIMA_RIESGOS_CONTROLES_PATH, 'Update_TG_TMP_to_compare_prima.sql'))
    print("filas afectadas:",rows_update_tmp_to_compare_pri)

    conexion_tiga.close()
    print("Proceso completado")



