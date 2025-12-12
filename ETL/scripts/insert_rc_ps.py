from scripts.funciones import *
from conection import *
import os
import pandas as pd
from datetime import datetime


columnas_insert = ["Referencia_del_proceso",
        "NroRiesgo",
        "NroControl",
        "1eraLinea",
        "2daLinea",
        "3eraLinea",
        "Riesgo_1eraLinea",
        "Riesgo_2daLinea",
        "Control_1eraLinea",
        "Control_2daLinea"
 
       ]
        
matriz = pd.DataFrame(columns=columnas_insert)




def insertar_ps_rc():
    print("insertar RC ps")
    
    
    
    avance = 0
    i = 0
    
    cont = 0
    avance = 20
    
    print(f"Progreso: {avance}%")
    ds1 = obtener_query_TIGA(os.path.join(QUERIES_PACIFICO_RIESGOS_CONTROLES_PATH, 'Cambios_Insert_RC.sql'))

    
    for idx, rd in ds1.iterrows():
        

        cont += 1
      

        matriz.at[i, "Referencia_del_proceso"] = rd["Referencia_del_Proceso"]
       
        

        if not pd.isnull(rd["N° Riesgo"]) and rd["N° Riesgo"]!='N/A':
            matriz.at[i, "NroRiesgo"] = rd["N° Riesgo"]

        if not pd.isnull(rd["N° Control"]) and rd["N° Control"]!='N/A':
            matriz.at[i, "NroControl"] = rd["N° Control"]

       
       
        
        matriz.at[i, "1eraLinea"] = 0
        matriz.at[i, "2daLinea"] = 0
        matriz.at[i, "3eraLinea"] = 0
        matriz.at[i, "Riesgo_1eraLinea"] = 0
        matriz.at[i, "Riesgo_2daLinea"] = 0
        matriz.at[i, "Control_1eraLinea"] = 0
        matriz.at[i, "Control_2daLinea"] = 0

        i+=1

        

    filas , columnas = matriz.shape
    print("filas a insertar o actulizar: ", filas)
    

    

   
    avance = 40
    print(f"Progreso: {avance}%")


    # Insertar datos en TG_Proyecto_Riesgo_Control
    columnas = "INSERT INTO dbo.TG_Proyecto_Riesgo_Control (" + ",".join([f"[{col}]" for col in matriz.columns]) + ") VALUES "

    conexion_tiga = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};database=PROYECTOSIAV2;encrypt=no;integrated security=False;min_tls=1.0;port=1433;server=PSTMMPRD0300;trusted_connection=no;uid=USTEAM02;pwd=ZU4repezaGefraMu')
    cursor = conexion_tiga.cursor()

    for idx, dr in matriz.iterrows():
        
        valores = []
        
        for col in matriz.columns:
            valor = str(dr[col])
            if valor == 'nan':
                valor = ''
            valor_sin_comillas = valor.replace('\'', '')
            valores.append(f"'{valor_sin_comillas}'")
        
        valores_con_comas = ",".join(valores)
        registro = "(" + valores_con_comas + ")"
        insert = columnas + registro
        
        cursor.execute("SET LANGUAGE Spanish " + insert)
        cursor.commit()



    avance = 70
    

    
    print(f"Progreso: {avance}%")
    rows_delete_tmp_ps =  execute_query_TIGA(os.path.join(QUERIES_PACIFICO_RIESGOS_CONTROLES_PATH, 'Cambios_Delete_TG_RC.sql'))
    print("Filas afectadas en delete tg_rc: ",rows_delete_tmp_ps)

   
    avance = 90

    conexion_tiga.close()
    print("Proceso completado")



