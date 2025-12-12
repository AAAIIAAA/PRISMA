import re
import pandas as pd
import pyodbc
from conection import *
import os 


def strip_html(var1):
    try:
        adhoc_pattern0 = r"P {[^>]*}"
        adhoc_pattern1 = r"P {[^>]*}"
        adhoc_pattern2 = r"{[^>]*}"
        html_tag_pattern = r"<.*?>"

        res = re.sub(adhoc_pattern0, '', var1)
        res = re.sub(adhoc_pattern1, '', res)
        res = re.sub(adhoc_pattern2, '', res)
        res = re.sub(html_tag_pattern, '', res)
        res = re.sub(r"<[^>]*>", '', res)
        res = re.sub(r"\w+\s*{.*?}", '', res)
        res = re.sub(r"HTML><TITLE>", '', res)
        res = re.sub(r"HTML>", '', res)
        res = re.sub(r"TITLE>", '', res)

        return res
    except Exception as e:
        print(f"An error occurred: {e}")
        return var1



def clear_html_text(s):
    if len(s) > 0:
        s = strip_html(s)
        s = s.replace("\n", " ")
        s = s.replace(".   ", ".\n")
        s = s.replace(".  ", ".\n")
        s = s.replace("             ", " ")
        s = s.replace("            ", " ")
        s = s.replace("           ", " ")
        s = s.replace("          ", " ")
        s = s.replace("         ", " ")
        s = s.replace("        ", " ")
        s = s.replace("       ", " ")
        s = s.replace("      ", " ")
        s = s.replace("     ", " ")
        s = s.replace("    ", " ")
        s = s.replace("   ", " ")
        s = s.replace("  ", " ")
        s = s.replace("&#243;", "ó")
        s = s.replace("&#237;", "í")
        s = s.replace("&#225;", "á")
        s = s.replace("&#193;", "Á")
        s = s.replace("&#233;", "é")
        s = s.replace("&#250;", "ú")
        s = s.replace("&#241;", "ñ")
        s = s.replace("&nbsp;", "")
        s = s.replace("&aacute;", "á")
        s = s.replace("&eacute;", "é")
        s = s.replace("&iacute;", "í")
        s = s.replace("&oacute;", "ó")
        s = s.replace("&uacute;", "ú")
        s = s.replace("&ntilde;", "ñ")
        s = s.replace('"', "&quot;")
        s = s.strip()

        s = s.replace("P {", "")
        s = s.replace(" MARGIN: 0px }", "")

    return s



def causa_evento_consecuencia(val1, solicitud):
    causa = val1.find("Causa")
    evento = val1.find("Evento")
    consecuencia = val1.find("Consecuencia")
    total = len(val1)
    temp1 = temp2 = temp3 = ""

    if causa >= 0 and evento >= 0 and consecuencia >= 0:
        if solicitud == "Causa":
            if evento - causa - 5 > 0:
                temp1 = val1[causa + 6:evento].strip()
            temp1 = temp1.replace("\n", "").replace(":", "").strip()
            return temp1

        elif solicitud == "Evento":
            if consecuencia - evento - 6 > 0:
                temp2 = val1[evento + 6:consecuencia].strip()
            temp2 = temp2.replace("\n", "").replace(":", "").strip()
            return temp2

        elif solicitud == "Consecuencia":
            if total - consecuencia - 11 > 0:
                temp3 = val1[consecuencia + 12:].strip()
            temp3 = temp3.replace("\n", "").replace(":", "").strip()
            return temp3

    return ""


def cat_riesgo(valor, solicitud):
    clase = valor
    guion = clase.find("-")
    temp1 = clase[:guion - 1].strip()
    temp2 = clase[guion + 1:].strip()
    
    if solicitud == "Categoría":
        return temp1
    elif solicitud == "Tipo":
        return temp2



def categoría_pri(id):
    query = open(os.path.join(QUERIES_AUXILIARES_RIESGOS_CONTROLES_PATH, f'CCCategoria.sql'), 'r', encoding='utf-8-sig').read()
   
    query = query.replace("Valor", str(id))
    ds = obtener_query_teammate_pri(query)
    
    if not ds.empty and ds.shape[0] > 0:
        temp = ds.iloc[0, 0]
    else:
        temp = ""
    
    return temp



def categoría_ps(id):
    query = open(os.path.join(QUERIES_AUXILIARES_RIESGOS_CONTROLES_PATH, f'CCCategoria.sql'), 'r', encoding='utf-8-sig').read()
   
    query = query.replace("Valor", str(id))
    
    ds = obtener_query_teammate_ps(query)
    
    
    if not ds.empty and ds.shape[0] > 0:
        temp = ds.iloc[0, 0]
    else:
        temp = ""
    
    return temp




def riesgo_inherente_ps(id_pro, id_r, id_c, solicitud):
    temp = open(os.path.join(QUERIES_AUXILIARES_RIESGOS_CONTROLES_PATH, f'CCRiesgoInherente.sql'), 'r', encoding='utf-8-sig').read()

    temp = temp.replace("Valor1", str(id_pro))
    temp = temp.replace("Valor2", str(id_r))
    temp = temp.replace("Valor3", str(id_c))
    
    ds = obtener_query_teammate_ps(temp)
    
    if not ds.empty and ds.shape[0] > 0 and not ds.isnull().all().all():
        if solicitud == "Impacto":
            temp = str(ds.iloc[0, 0])
        elif solicitud == "Frecuencia":
            temp = str(ds.iloc[0, 1])
    else:
        temp = ""
    
    return temp




def riesgo_inherente_pri(id_pro, id_r, id_c, solicitud):
    temp = open(os.path.join(QUERIES_AUXILIARES_RIESGOS_CONTROLES_PATH, f'CCRiesgoInherente.sql'), 'r', encoding='utf-8-sig').read()

    temp = temp.replace("Valor1", str(id_pro))
    temp = temp.replace("Valor2", str(id_r))
    temp = temp.replace("Valor3", str(id_c))
    
    ds = obtener_query_teammate_pri(temp)


    
    if not ds.empty and ds.shape[0] > 0 and not ds.isnull().all().all():
        if solicitud == "Impacto" and len(ds.iloc[0, 0]) > 0:
            temp = ds.iloc[0, 0]
        elif solicitud == "Frecuencia" and len(ds.iloc[0, 1]) > 0:
            temp = ds.iloc[0, 1]
        else:
            temp = ""
    else:
        temp = ""
    
    return temp


def cálculo_riesgo_ps(nombre, solicitud, id_plan):
    try:
        id_plan = int(id_plan)
    except ValueError:
        return 14
    temp = 0
    if id_plan > 5:
        if solicitud == "Impacto":
            if nombre == "Bajo":
                temp = 3
            elif nombre == "Moderado":
                temp = 12
            elif nombre == "Relevante":
                temp = 108
            elif nombre == "Alto":
                temp = 243
            elif nombre == "Critico":
                temp = 300
            else:
                temp = 0
        elif solicitud == "Frecuencia":
            if nombre == "Muy raro":
                temp = "0.2"
            elif nombre == "Raro":
                temp = "0.33"
            elif nombre == "Eventual":
                temp = "1"
            elif nombre == "Frecuente":
                temp = "2"
            elif nombre == "Muy frecuente":
                temp = "12"
            else:
                temp = "0"
    else:
        if solicitud == "Impacto":
            if nombre == "Bajo":
                temp = 5
            elif nombre == "Moderado":
                temp = 20
            elif nombre == "Relevante":
                temp = 180
            elif nombre == "Alto":
                temp = 405
            elif nombre == "Critico":
                temp = 500
            else:
                temp = 0
        elif solicitud == "Frecuencia":
            if nombre == "Muy raro":
                temp = "0.2"
            elif nombre == "Raro":
                temp = "0.33"
            elif nombre == "Eventual":
                temp = "1"
            elif nombre == "Frecuente":
                temp = "2"
            elif nombre == "Muy frecuente":
                temp = "12"
            else:
                temp = "0"
    return temp



def cálculo_riesgo_pri(nombre, solicitud, id_plan):
    #id_plan=int(id_plan)
    try:
        id_plan = int(id_plan)
    except ValueError:
        return 14
    temp = 0
    if id_plan > 5:
        if solicitud == "Impacto":
            if nombre == "Bajo":
                temp = 1
            elif nombre == "Moderado":
                temp = 4
            elif nombre == "Relevante":
                temp = 36
            elif nombre == "Alto":
                temp = 81
            elif nombre == "Critico":
                temp = 100
            else:
                temp = 0
        elif solicitud == "Frecuencia":
            if nombre == "Muy raro":
                temp = "0.2"
            elif nombre == "Raro":
                temp = "0.33"
            elif nombre == "Eventual":
                temp = "1"
            elif nombre == "Frecuente":
                temp = "2"
            elif nombre == "Muy Frecuente":
                temp = "12"
            else:
                temp = "0"
    else:
        if solicitud == "Impacto":
            if nombre == "Bajo":
                temp = 5
            elif nombre == "Moderado":
                temp = 20
            elif nombre == "Relevante":
                temp = 180
            elif nombre == "Alto":
                temp = 405
            elif nombre == "Critico":
                temp = 500
            else:
                temp = 0
        elif solicitud == "Frecuencia":
            if nombre == "Muy raro":
                temp = "0.2"
            elif nombre == "Raro":
                temp = "0.33"
            elif nombre == "Eventual":
                temp = "1"
            elif nombre == "Frecuente":
                temp = "2"
            elif nombre == "Muy Frecuente":
                temp = "12"
            else:
                temp = "0"
    return temp



def ifc_ps(valor, id_plan):
    
    valor = int(valor)
    try:
        id_plan = int(id_plan)
    except ValueError:
        return 14
    temp = ""
    
    if id_plan > 5:
        if 0 < valor <= 12:
            temp = "Bajo"
        elif 12 < valor <= 36:
            temp = "Moderado"
        elif 36 < valor <= 144:
            temp = "Relevante"
        elif 144 < valor <= 486:
            temp = "Alto"
        elif valor > 486:
            temp = "Critico"
        else:
            temp = ""
    else:
        if 0 < valor <= 35:
            temp = "Bajo"
        elif 35 < valor <= 80:
            temp = "Moderado"
        elif 80 < valor <= 359:
            temp = "Relevante"
        elif 359 < valor <= 999:
            temp = "Alto"
        elif valor > 486:
            temp = "Critico"
        else:
            temp = ""
    return temp





def ifc_pri(valor):
    valor = int(valor)

    if 0 < valor <= 4:
        temp = "Bajo"
    elif 4 < valor <= 12:
        temp = "Moderado"
    elif 12 < valor <= 48:
        temp = "Relevante"
    elif 48 < valor <= 162:
        temp = "Alto"
    elif valor > 162:
        temp = "Critico"
    else:
        temp = ""
    return temp






def principios_c(nombre):
    mapping = {
        "Principio 4": 4,
        "Principio 5": 5,
        "Principio 6": 6,
        "Principio 7": 7,
        "Principio 8": 8,
        "Principio 9": 9,
        "Principio 10": 10,
        "Principio 11": 11,
        "Principio 12": 12,
        "Principio 13": 13,
        "Principio 14": 14,
        "Principio 15": 15,
        "Principio 16": 16,
        "Principio 17": 17
    }
    return mapping.get(nombre, 0)


def cont_clave_ps(valor1, valor2):
    valor1=int(valor1)
    valor2=int(valor2)
    if valor1 >= 108 or valor2 >= 300:
        temp = "Clave"
    else:
        temp = "No Clave"
    return temp





def cont_clave_pri(valor1, valor2, id_plan):
    try:
        id_plan = int(id_plan)
    except ValueError:
        return 14
    valor1=int(valor1)
    valor2=int(valor2)
    if id_plan <= 5:
        if valor1 >= 180 or valor2 >= 500:
            temp = "Clave"
        else:
            temp = "No Clave"
    else:
        if valor1 >= 36 or valor2 >= 100:
            temp = "Clave"
        else:
            temp = "No Clave"
    return temp



def control_apl(valor1, valor2):
    if valor2 in valor1:
        if valor2 in ["C", "A", "V", "R"]:
            return "X"
        else:
            return ""
    else:
        return ""


def aseveraciones(valor1, valor2):
    if valor2 in valor1:
        if valor2 in ["EX", "IN", "VA", "PR", "DO"]:
            return "X"
        else:
            return ""
    else:
        return ""



import re

def remove_html2(input_str):
    patterns = [
        "</[^>]>", "<html[^>]>", "<BODY[^>]>", "<body[^>]>", "<SPAN[^>]>", "<span[^>]>", "<HEAD[^>]*>",
        "<head[^>]>", "&[^;];", "<OL[^>]>", "<DIV[^>]>", "<META[^>]>", "<STRONG[^>]>", "<A contentEditable[^>]*>",
        "<CODE id[^>]>", "<FONT[^>]>", "<P[^>]>", "<p[^>]>", "<BR[^>]>", "<LI[^>]>", "P[^}]*}", "HTML><TITLE>"
    ]

    temp_str = input_str
    for pattern in patterns:
        temp_str = re.sub(pattern, '', temp_str, flags=re.IGNORECASE)

    temp_str = temp_str.strip().replace("\n", "")
    temp_str = re.sub(r"<P[^>]*>", "\n", temp_str, flags=re.IGNORECASE)
    temp_str = re.sub(r"<BR[^>]*>", "\n", temp_str, flags=re.IGNORECASE)
    temp_str = re.sub(r"<LI[^>]*>", "\n", temp_str, flags=re.IGNORECASE)

    match = re.search(r"[A-Za-z0-9\-]+", temp_str)
    if match:
        start = match.start()
        temp_str = temp_str[start:]

    return temp_str




def observaciones_ps(id):
    temp = open(os.path.join(QUERIES_PACIFICO_RIESGOS_CONTROLES_PATH, f'PS_CCObservaciones.sql'), 'r', encoding='utf-8-sig').read()
    
    temp = temp.replace("Valor", str(id))
    

    ds2 = obtener_query_teammate_ps(temp)
    return ds2



def observaciones_pri(id):
    temp = open(os.path.join(QUERIES_PRIMA_RIESGOS_CONTROLES_PATH, f'PRI_CCObservaciones.sql'), 'r', encoding='utf-8-sig').read()
    
    temp = temp.replace("Valor", str(id))
    
    ds2 = obtener_query_teammate_pri(temp)
    return ds2


def riesgo_res(frec, vcontrol):
    frec=float(frec)
    print(vcontrol)
   
    if isinstance(vcontrol, str) and (vcontrol == '' or not vcontrol.isdigit()):
        vcontrol = 0
    else:
        vcontrol = int(vcontrol)
    
    if frec == 12:
        variable1 = frec / 6
    elif frec == 2:
        variable1 = frec / 2
    elif frec == 1:
        variable1 = 0.33 / frec
    elif frec == 0.33:
        variable1 = frec / 1.65
    else:
        variable1 = 0.2

    
    if frec == 0.2:
        variable2 = 1
    elif frec == 0.33:
        variable2 = 1 / 1.65
    elif frec == 1:
        variable2 = 0.33
    elif frec == 2:
        variable2 = 0.5
    elif frec == 12:
        variable2 = 1 / 6
    else:
        variable2 = 0

    
    if vcontrol == 1:
        variable3 = variable2
    elif vcontrol == 2:
        variable3 = (variable2 + (1 - variable2) / 4)
    elif vcontrol == 3:
        variable3 = (variable2 + (2 * (1 - variable2) / 4))
    elif vcontrol == 4:
        variable3 = (variable2 + (3 * (1 - variable2) / 4))
    elif vcontrol == 5:
        variable3 = (variable2 + (4 * (1 - variable2) / 4))
    else:
        variable3=0

    
    if vcontrol == 1:
        temp = variable1
    elif vcontrol == 5:
        temp = frec
    else:
        temp = frec * variable3

    return temp



def frecuencia_r(valor):
    if valor is None or valor ==0:
        temp = ""
    elif valor <= 0.2:
        temp = "Muy raro"
    elif 0.2 < valor <= 0.33:
        temp = "Raro"
    elif 0.33 < valor <= 1:
        temp = "Eventual"
    elif 1 < valor <= 2:
        temp = "Frecuente"
    elif valor > 2:
        temp = "Muy Frecuente"
    return temp



def cálculo_editar_ps(nombre, solicitud):
    temp = ""
    if solicitud == "Impacto":
        if nombre == 3:
            temp = "Bajo"
        elif nombre == 12:
            temp = "Moderado"
        elif nombre == 108:
            temp = "Relevante"
        elif nombre == 243:
            temp = "Alto"
        elif nombre == 300:
            temp = "Critico"
    elif solicitud == "Frecuencia":
        if nombre == "0.2":
            temp = "Muy raro"
        elif nombre == "0.33":
            temp = "Raro"
        elif nombre == "1":
            temp = "Eventual"
        elif nombre == "2":
            temp = "Frecuente"
        elif nombre == "12":
            temp = "Muy frecuente"
    return temp


def cálculo_editar_pri(nombre, solicitud, id_plan):
    temp = ""
    try:
        id_plan = int(id_plan)
    except ValueError:
        return 14
    if id_plan > 5:
        if solicitud == "Impacto":
            if nombre == 1:
                temp = "Bajo"
            elif nombre == 4:
                temp = "Moderado"
            elif nombre == 36:
                temp = "Relevante"
            elif nombre == 81:
                temp = "Alto"
            elif nombre == 100:
                temp = "Critico"
        elif solicitud == "Frecuencia":
            if nombre == "0.2":
                temp = "Muy raro"
            elif nombre == "0.33":
                temp = "Raro"
            elif nombre == "1":
                temp = "Eventual"
            elif nombre == "2":
                temp = "Frecuente"
            elif nombre == "12":
                temp = "Muy Frecuente"
    else:
        if solicitud == "Impacto":
            if nombre == 5:
                temp = "Bajo"
            elif nombre == 20:
                temp = "Moderado"
            elif nombre == 180:
                temp = "Relevante"
            elif nombre == 405:
                temp = "Alto"
            elif nombre == 500:
                temp = "Critico"
        elif solicitud == "Frecuencia":
            if nombre == "0.2":
                temp = "Muy raro"
            elif nombre == "0.33":
                temp = "Raro"
            elif nombre == "1":
                temp = "Eventual"
            elif nombre == "2":
                temp = "Frecuente"
            elif nombre == "12":
                temp = "Muy Frecuente"
    return temp


def get_update_values(dr, columns):
    update_values = []
    for col in columns:
        if col != "Identificador":
            value = str(dr[col]).replace("'", "''") if pd.notna(dr[col]) else ""
            update_values.append(f"[{col}] = '{value}'")
    return ", ".join(update_values)

