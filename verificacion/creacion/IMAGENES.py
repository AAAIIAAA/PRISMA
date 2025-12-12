import os
import time
from pptx import Presentation
from params import *
from functions import *
from creaciones import *
import matplotlib.patches as mpatches
import pandas as pd
import matplotlib.pyplot as plt

def get_color_for_value(value):
    if value < 0.55:
        return 'red'
    elif value < 0.70:
        return 'orange'
    elif value < 0.85:
        return 'green'
    else:
        return 'darkgreen'

def create_evolutivo(evaluation_name, negocio,codigo):
    file_path = os.path.join(PLANTILLAS_PS_PATH, "Input_PlanAnual.xlsx")
    df = pd.read_excel(file_path)
    
    
    filtered_df = df[(df['Evaluacion'] == evaluation_name) & (df['Negocio'] == negocio)]
    if filtered_df.empty:
        print("No se encontró la evaluación y negocio especificados:", evaluation_name, negocio)
        return
    
    
    row = filtered_df.iloc[0]
    
    
    year_columns = ['2019', '2020', '2021', '2022', '2023', '2024']
    years_available = []
    effective_values = [] 
    display_values = []   

    for col in year_columns:
        if col in row:
            val = row[col]
            if pd.notnull(val):
                
                if isinstance(val, str) and val.strip().upper() == "S/C":
                    years_available.append(int(col))
                    effective_values.append(1.0)
                    display_values.append("S/C")
                else:
                    try:
                        numeric_val = float(val)
                        years_available.append(int(col))
                        effective_values.append(numeric_val)
                        display_values.append(f'{numeric_val:.2f}')
                    except ValueError:
                        
                        pass
    
    if not effective_values:
        print("No hay calificativos disponibles para la evaluación:", evaluation_name, "y negocio:", negocio)
        return
    
    
    if len(effective_values) >= 3:
        sel_years = years_available[-3:]
        sel_effective = effective_values[-3:]
        sel_display = display_values[-3:]
    elif len(effective_values) == 2:
        sel_years = years_available[-2:]
        sel_effective = effective_values[-2:]
        sel_display = display_values[-2:]
    else:
        sel_years = years_available[-1:]
        sel_effective = effective_values[-1:]
        sel_display = display_values[-1:]
    
    
    plt.figure(figsize=(8, 5))
    ax = plt.gca()
    
   
    plt.plot(sel_years, sel_effective, color='gray', linewidth=2, zorder=1)

    
    
   
    for year, eff_val, disp_val in zip(sel_years, sel_effective, sel_display):
        color = get_color_for_value(eff_val)
        plt.scatter(year, eff_val, color=color, s=80, zorder=2)
        
        plt.text(year, eff_val + 0.02, disp_val, ha='center', va='bottom', fontsize=9, color=color, zorder=3)
    
   
    plt.axhspan(0, 0.55, color='red', alpha=0.1)
    plt.axhspan(0.55, 0.70, color='orange', alpha=0.1)
    plt.axhspan(0.70, 0.85, color='green', alpha=0.1)
    plt.axhspan(0.85, 1.0, color='lightgreen', alpha=0.2)
    
   
    plt.ylim(0, 1.05)
    plt.xlim(min(sel_years) - 0.5, max(sel_years) + 0.5)
    plt.xticks(sel_years)
   
    plt.xlabel('Año')
    plt.ylabel('Calificativo (decimal)')

  
    patch_deficiente     = mpatches.Patch(color='red', label='Deficiente (< 0.55)')
    patch_regular       = mpatches.Patch(color='orange', label='Regular (0.55 - 0.70)')
    patch_aceptable     = mpatches.Patch(color='green', label='Aceptable (0.70 - 0.85)')
    patch_satisfactorio = mpatches.Patch(color='darkgreen', label='Satisfactorio (>= 0.85)')
    
  
    plt.legend(
        handles=[patch_deficiente, patch_regular, patch_aceptable, patch_satisfactorio],
        loc='lower center',
        bbox_to_anchor=(0.5, -0.2),
        ncol=4,
        frameon=False,
        fontsize=8,
        handlelength=1,
        handletextpad=0.4,
        columnspacing=0.5
    )
    
    plt.tight_layout()

    filename = f'evolucion_{codigo}.png'
    
    try:
        final_path = obtenerpath_imagen(negocio,codigo,filename)
        plt.savefig(final_path, dpi=300, bbox_inches='tight')
        
        print(f"IMAGEN guardado en {final_path}")
    except Exception as e:
        print(f"Error al guardar el archivo IMAGEN: {e}")


   



def main():
    file_path_informe = os.path.join(EXCEL_IMAGENES_PATH, "informe_insertar.xlsx")
    file_path_informe_v2 = os.path.join(EXCEL_IMAGENES_PATH, "informe_insertar_v2.xlsx")
  
    try:
        if os.path.exists(file_path_informe_v2):
            print("----------- IMAGENES ----------")
            df_efectivos_mapa = pd.DataFrame()
            df_cantidades_mapa = pd.DataFrame()
            df_encontrado_evaluacion = pd.DataFrame()
            time.sleep(5)
            
            negocio = obtener_tipo_de_Excel_informe(file_path_informe_v2)
            codigo = obtener_codigo_de_Excel_informe(file_path_informe_v2)

          
            
            df_encontrado_evaluacion = obtenerDatosDe2("encontrar_evaluacion")
            df_filtrado = df_encontrado_evaluacion
            nombre_evaluacion = 'NUL'
            if not df_filtrado.empty:
                nombre_evaluacion = df_filtrado['Evaluacion'].iloc[0]
                print(f"ID de evaluación encontrado: {nombre_evaluacion}")
            else:
                print("No se encontró el código del proyecto en el DataFrame.")

            
            
            create_evolutivo(nombre_evaluacion, negocio, codigo)
            print("aca irian las creaciones de imagenes")
        

            os.remove(file_path_informe_v2)
        else:
            print("base_creacion_imagenes_2 no existe.")
            
        time.sleep(10)


    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
    
  
   

if __name__ == "__main__":
    main()