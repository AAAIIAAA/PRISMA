import os
import time
#from pptx import Presentation
from params import *
from functions import *
#from creaciones import *
from PEAS import *

def main():
    file_path = os.path.join(EXCEL_PATH, "base_creacion_ppts.xlsx")
    file_path_v2 = os.path.join(EXCEL_PATH, "base_creacion_ppts_v2.xlsx")
    
    file_path_informe = os.path.join(EXCEL_IMAGENES_PATH, "informe_insertar.xlsx")
    file_path_informe_v2 = os.path.join(EXCEL_IMAGENES_PATH, "informe_insertar_v2.xlsx")

    file_path_pea = os.path.join(PEAS_PATH, "base_creacion_peas.xlsx")
    file_path_pea_v2 = os.path.join(PEAS_PATH, "base_creacion_peas_v2.xlsx")

    excel_file_count, excel_file_paths = count_and_store_excel_files(MAPA_ASEGURAMIENTO_PATH, list_ruta_negocio)


    '''

#------------------------------------- IMAGENES
    try:
        if os.path.exists(file_path_informe_v2):
            print("----------- IMAGENES ----------")
            df_efectivos_mapa = pd.DataFrame()
            df_cantidades_mapa = pd.DataFrame()
            df_encontrado_evaluacion = pd.DataFrame()
            time.sleep(5)
            
            negocio = obtener_tipo_de_Excel_informe(file_path_informe_v2)
            codigo = obtener_codigo_de_Excel_informe(file_path_informe_v2)

          
            df_efectivos_mapa = obtenerDatosDe2("efectivos_mapa_calor")
            df_cantidades_mapa = obtenerDatosDe2("cantidades_mapa_calor")
            df_encontrado_evaluacion = obtenerDatosDe2("encontrar_evaluacion")
            df_filtrado = df_encontrado_evaluacion[df_encontrado_evaluacion['Codigo'] == codigo]
            id_evaluacion = 'NUL'
            if not df_filtrado.empty:
                id_evaluacion = df_filtrado['ID_Evaluacion_Plan'].iloc[0]
                print(f"ID de evaluación encontrado: {id_evaluacion}")
            else:
                print("No se encontró el código del proyecto en el DataFrame.")

            
            #create_mapa_calor(negocio,codigo,df_efectivos_mapa,df_cantidades_mapa)
            #create_evolutivo(id_evaluacion)
            print("aca irian las creaciones de imagenes")
        

            os.remove(file_path_informe_v2)
        else:
            print("base_creacion_imagenes_2 no existe.")
            
        time.sleep(10)


    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)


    
    
#------------------------------------------ PLANTILLAS


    try:
        if os.path.exists(file_path_v2):
            
            
            print("------ PLANTILLAS ------")
            df_datos = pd.DataFrame()
            df_calificativo_total = pd.DataFrame()
            df_calificativo_unidad_responsable = pd.DataFrame()
            df_cantidad_controles = pd.DataFrame()
            df_observaciones_informe = pd.DataFrame()
            time.sleep(5)
            tipo,negocio = obtener_tipo_de_Excel(file_path_v2)
            codigo = obtener_codigo_de_Excel(file_path_v2)

            if tipo == 'Sprint Planning':
                df_datos = obtenerDatosDe("memorando")
                
                create_memorando(tipo,negocio,codigo,df_datos)
                os.remove(file_path_v2)

            elif tipo == 'Informe Final' or tipo == 'Informe Borrador':

                df_datos = obtenerDatosDe("memorando")
                df_calificativo_total = obtenerDatosDe("calificativo_total")
                df_calificativo_unidad_responsable = obtenerDatosDe("calificativo_unidad_responsable")
                df_cantidad_controles=obtenerDatosDe("cantidad_controles")
                df_observaciones_informe = obtenerDatosDe("observaciones_informe")

                
                create_informe_ppt(tipo,negocio,codigo,df_datos,df_calificativo_total,df_calificativo_unidad_responsable,df_cantidad_controles,df_observaciones_informe)
                os.remove(file_path_v2)

            elif tipo == 'Observaciones Final' or tipo == 'Observaciones Borrador':

                df_datos = obtenerDatosDe('Observaciones')
                
                create_observaciones_ppt(tipo,negocio,codigo,df_datos)
                os.remove(file_path_v2)
            else:
                print("no se encontro tipo")

            
        
            
        else:
            print("base_creacion_ppts_2 no existe.")
            
        time.sleep(10)
    
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
'''

#--------------------------- MAPA ASEGURAMIENTO
    try:
        if excel_file_count > 0:
            print("---------- MAPA ASEGURAMIENTO -----------")
            print(excel_file_count)
            data_matrix = read_excel_sheets(excel_file_paths)
            delete_exists_asegurate_map(excel_file_paths,CNXN_TIGA)
            print(data_matrix)
            print(CNXN_TIGA)

            simulate_procedure_call(data_matrix,CNXN_TIGA)

            delete_analyzed_files(excel_file_paths)

        else:
            print("Error al generar inserts en sql - Mapa Aseguramiento")

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
#--------------------------- MAPA ASEGURAMIENTO - ACTUALIZACIÓN DE CAMPOS FALTANTES
    '''try:
        excel_file_count_update, excel_file_paths_update = count_and_store_excel_files_original(MAPA_ASEGURAMIENTO_PATH, list_ruta_negocio)

        if excel_file_count_update > 0:
            print("---------- MAPA ASEGURAMIENTO (ACTUALIZACIÓN) -----------")
            print(f"Archivos encontrados: {excel_file_count_update}")

            data_matrix = read_excel_sheets(excel_file_paths_update)
            print(f"Registros leídos: {len(data_matrix)}")

            simulate_update_call(data_matrix, CNXN_TIGA)

            print("Proceso de actualización completado con éxito.")
        else:
            print("No se encontraron archivos sin '_v2' para actualizar campos faltantes.")

    except Exception as e:
        print(f"Error durante la actualización del Mapa de Aseguramiento: {e}")
        time.sleep(10)'''
#-------------------------------------------PEAS  



    try:
        if os.path.exists(file_path_pea_v2):
            print("----- PEAS -----")
            proyecto = obtener_proyecto_peas(file_path_pea_v2)
            negocio = obtener_NEGOCIO_peas(file_path_pea_v2)
            proyecto_limpio = proyecto.replace(' ','')

            df_datos = pd.DataFrame()

            
           
            
            df_datos = obtenerDatosDe3('info_peas')
            df_procesada = pd.read_excel(os.path.join(PEAS_PATH_OUTPUT,f'PEAS_{proyecto_limpio}.xlsx'))
            

            if not df_procesada.empty:
               
                print("Se leyo correctamente")
            else:
                print("Fuente de proyecto sin sincronizar")
           
            generar_informes(df_datos,df_procesada,proyecto,negocio)
            time.sleep(5)
            
            
            
            print(proyecto_limpio)
            print("Eliminar")
            print(PEAS_PATH_OUTPUT)
            os.remove(file_path_pea_v2)
            file_to_remove = os.path.join(PEAS_PATH_OUTPUT,f'PEAS_{proyecto_limpio}.xlsx')
            os.remove(file_to_remove)

           # os.remove(os.path.join(PEAS_PATH_OUTPUT,f'PEAS_{proyecto_limpio}.xlsx'))
        else:
            print("base de creacion peas no existe")
            
        time.sleep(10)


    except Exception as e:
        print(f"Error: {e}")
        time.sleep(20)




if __name__ == "__main__":
    main()