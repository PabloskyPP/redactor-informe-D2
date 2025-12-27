"""
Módulo para leer datos del test D2 desde archivos Excel
"""
import pandas as pd


def leer_datos_excel(ruta_archivo):
    """
    Lee los datos del archivo Excel del test D2
    
    Args:
        ruta_archivo: Ruta al archivo Excel
        
    Returns:
        dict: Diccionario con 'edad', 'sub_num', 'nombre_completo', 'nombre' y 'datos_d2'
    """
    try:
        # Leer hoja 'info' para obtener la edad y sub_num
        df_info = pd.read_excel(ruta_archivo, sheet_name='info')
        edad = df_info['age'].iloc[0] if 'age' in df_info.columns else None
        
        # Extraer sub_num y procesarlo
        sub_num = df_info['sub_num'].iloc[0] if 'sub_num' in df_info.columns else None
        
        # Procesar nombre completo y nombre (primer token)
        if sub_num:
            nombre_completo = str(sub_num).strip()
            # Obtener solo el primer token (antes del primer espacio)
            nombre = nombre_completo.split()[0] if nombre_completo else nombre_completo
        else:
            nombre_completo = None
            nombre = None
        
        # Leer hoja 'D2' con los datos del test
        df_d2 = pd.read_excel(ruta_archivo, sheet_name='D2')
        
        return {
            'edad': edad,
            'sub_num': sub_num,
            'nombre_completo': nombre_completo,
            'nombre': nombre,
            'datos_d2': df_d2
        }
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        raise


def calcular_puntuaciones_directas(datos):
    """
    Calcula las puntuaciones directas del test D2
    
    Args:
        datos: Dict con 'edad' y 'datos_d2'
        
    Returns:
        dict: Diccionario con todas las puntuaciones directas y por fila
    """
    df = datos['datos_d2']
    
    # Agrupar por fila (row)
    rows = df['row'].unique()
    rows = sorted(rows)
    
    resultados = {
        'edad': datos['edad'],
        'sub_num': datos.get('sub_num'),
        'nombre_completo': datos.get('nombre_completo'),
        'nombre': datos.get('nombre'),
        'TR_por_fila': [],
        'TA_por_fila': [],
        'O_por_fila': [],
        'C_por_fila': [],
        'TR_total': 0,
        'TA_total': 0,
        'O_total': 0,
        'C_total': 0,
        'E_total': 0,
        'TOT': 0,
        'CON': 0,
        'TR_max': 0,
        'TR_min': float('inf'),
        'VAR': 0
    }
    
    for row in rows:
        df_row = df[df['row'] == row]
        
        # TR: letter_num del último elemento con selected != FALSE
        df_seleccionados = df_row[df_row['selected'] != 'FALSE']
        if len(df_seleccionados) > 0:
            TR = df_seleccionados['letter_num'].max()
        else:
            TR = 0
        resultados['TR_por_fila'].append(TR)
        
        # TA: casos con target='si' y selected != 'FALSE'
        TA = len(df_row[(df_row['target'] == 'si') & (df_row['selected'] != 'FALSE')])
        resultados['TA_por_fila'].append(TA)
        
        # O: casos después del último selected != FALSE con target='si' y selected='FALSE'
        if len(df_seleccionados) > 0:
            ultimo_letter_num = df_seleccionados['letter_num'].max()
            df_posteriores = df_row[df_row['letter_num'] <= ultimo_letter_num]
            O = len(df_posteriores[(df_posteriores['target'] == 'si') & 
                                   (df_posteriores['selected'] == 'FALSE')])
        else:
            O = 0
        resultados['O_por_fila'].append(O)
        
        # C: casos con target='no' y selected != 'FALSE'
        C = len(df_row[(df_row['target'] == 'no') & (df_row['selected'] != 'FALSE')])
        resultados['C_por_fila'].append(C)
    
    # Calcular totales
    resultados['TR_total'] = sum(resultados['TR_por_fila'])
    resultados['TA_total'] = sum(resultados['TA_por_fila'])
    resultados['O_total'] = sum(resultados['O_por_fila'])
    resultados['C_total'] = sum(resultados['C_por_fila'])
    resultados['E_total'] = resultados['O_total'] + resultados['C_total']
    
    # TOT = TR_total - E_total
    resultados['TOT'] = resultados['TR_total'] - resultados['E_total']
    
    # CON = TA_total - C_total
    resultados['CON'] = resultados['TA_total'] - resultados['C_total']
    
    # TR_max y TR_min con sus posiciones (índices de fila)
    if resultados['TR_por_fila']:
        resultados['TR_max'] = max(resultados['TR_por_fila'])
        resultados['TR_min'] = min(resultados['TR_por_fila'])
        resultados['VAR'] = resultados['TR_max'] - resultados['TR_min']
        
        # Guardar las posiciones (índices) de TR_max y TR_min
        resultados['TR_max_pos'] = resultados['TR_por_fila'].index(resultados['TR_max'])
        resultados['TR_min_pos'] = resultados['TR_por_fila'].index(resultados['TR_min'])
    
    return resultados
