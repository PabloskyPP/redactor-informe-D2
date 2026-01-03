"""
Módulo para leer datos del test D2 desde archivos Excel

Este módulo proporciona funciones para:
- Leer datos del Excel del test D2
- Calcular puntuaciones directas por fila y totales
- Identificar explícitamente celdas seleccionadas y no seleccionadas
- Proporcionar estructuras de datos claras y accesibles para análisis posterior
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
        # Verificar que sub_num es válido (no None, no NaN, no cadena vacía)
        import math
        if sub_num and not (isinstance(sub_num, float) and math.isnan(sub_num)):
            nombre_completo = str(sub_num).strip()
            # Obtener solo el primer token (antes del primer espacio)
            # Verificar que hay contenido antes de dividir
            if nombre_completo:
                tokens = nombre_completo.split()
                nombre = tokens[0] if tokens else nombre_completo
            else:
                nombre = nombre_completo
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


def identificar_celdas_seleccionadas(df):
    """
    Identifica las celdas seleccionadas y no seleccionadas de forma explícita
    
    Args:
        df: DataFrame con los datos del test D2
        
    Returns:
        dict: Diccionario con dos estructuras:
            - 'seleccionadas': set de tuplas (row, column) para celdas seleccionadas
            - 'no_seleccionadas': set de tuplas (row, column) para celdas no seleccionadas
            - 'mapa_seleccion': dict {(row, column): bool} para consulta rápida
    """
    seleccionadas = set()
    no_seleccionadas = set()
    
    for _, fila in df.iterrows():
        row = int(fila['row'])
        column = int(fila['letter_num'])
        celda = (row, column)
        
        if fila['selected'] == True:
            seleccionadas.add(celda)
        else:
            no_seleccionadas.add(celda)
    
    # Crear mapa de selección para consulta rápida: True si está seleccionada, False si no
    mapa_seleccion = {}
    for celda in seleccionadas:
        mapa_seleccion[celda] = True
    for celda in no_seleccionadas:
        mapa_seleccion[celda] = False
    
    return {
        'seleccionadas': seleccionadas,
        'no_seleccionadas': no_seleccionadas,
        'mapa_seleccion': mapa_seleccion
    }


def calcular_puntuaciones_directas(datos):
    """
    Calcula las puntuaciones directas del test D2
    
    Args:
        datos: Dict con 'edad' y 'datos_d2'
        
    Returns:
        dict: Diccionario con todas las puntuaciones directas y por fila.
              Incluye estructuras explícitas para:
              - indices_por_fila: dict con TR, TA, O, C para cada fila (1-14)
              - celdas_seleccionadas: estructura para consultar selección de celdas
              - índices globales: TR_total, TA_total, O_total, C_total, E_total, TOT, CON, VAR
    """
    df = datos['datos_d2']
    
    # Agrupar por fila (row)
    rows = df['row'].unique()
    rows = sorted(rows)
    
    # Identificar celdas seleccionadas de forma explícita
    celdas_seleccionadas = identificar_celdas_seleccionadas(df)
    
    resultados = {
        'edad': datos['edad'],
        'sub_num': datos.get('sub_num'),
        'nombre_completo': datos.get('nombre_completo'),
        'nombre': datos.get('nombre'),
        'datos_d2': df,  # Incluir DataFrame para generador_imagen_final
        
        # Estructura explícita de celdas seleccionadas
        'celdas_seleccionadas': celdas_seleccionadas,
        
        # Índices por fila (listas, compatibilidad hacia atrás)
        'TR_por_fila': [],
        'TA_por_fila': [],
        'O_por_fila': [],
        'C_por_fila': [],
        
        # Estructura explícita de índices por fila (diccionario por row)
        'indices_por_fila': {},
        
        # Índices totales
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
        
        # TR: letter_num del último elemento con selected == True
        df_seleccionados = df_row[df_row['selected'] == True]
        if len(df_seleccionados) > 0:
            TR = df_seleccionados['letter_num'].max()
        else:
            TR = 0
        resultados['TR_por_fila'].append(TR)
        
        # TA: casos con target='si' y selected == True
        TA = len(df_row[(df_row['target'] == 'si') & (df_row['selected'] == True)])
        resultados['TA_por_fila'].append(TA)
        
        # O: casos después del último selected == True con target='si' y selected == False
        if len(df_seleccionados) > 0:
            ultimo_letter_num = df_seleccionados['letter_num'].max()
            df_posteriores = df_row[df_row['letter_num'] <= ultimo_letter_num]
            O = len(df_posteriores[(df_posteriores['target'] == 'si') & 
                                   (df_posteriores['selected'] == False)])
        else:
            O = 0
        resultados['O_por_fila'].append(O)
        
        # C: casos con target='no' y selected == True
        C = len(df_row[(df_row['target'] == 'no') & (df_row['selected'] == True)])
        resultados['C_por_fila'].append(C)
        
        # Añadir índices a la estructura explícita por fila
        resultados['indices_por_fila'][row] = {
            'TR': TR,
            'TA': TA,
            'O': O,
            'C': C
        }
    
    # Calcular totales
    resultados['TR_total'] = sum(resultados['TR_por_fila'])
    resultados['TA_total'] = sum(resultados['TA_por_fila'])
    resultados['O_total'] = sum(resultados['O_por_fila'])
    resultados['C_total'] = sum(resultados['C_por_fila'])
    resultados['E_total'] = resultados['O_total'] + resultados['C_total']
    
    # TOT = TR_total - E_total (rendimiento neto)
    resultados['TOT'] = resultados['TR_total'] - resultados['E_total']
    
    # CON = TA_total - C_total (índice de concentración)
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


# ============================================================================
# FUNCIONES DE UTILIDAD PARA CONSULTAR RESULTADOS
# ============================================================================

def esta_celda_seleccionada(resultados, row, column):
    """
    Consulta si una celda específica está seleccionada
    
    Args:
        resultados: Dict devuelto por calcular_puntuaciones_directas
        row: Número de fila (1-14)
        column: Número de columna (1-47)
        
    Returns:
        bool: True si la celda está seleccionada, False si no
    """
    return resultados['celdas_seleccionadas']['mapa_seleccion'].get((row, column), False)


def obtener_indices_fila(resultados, row):
    """
    Obtiene los índices (TR, TA, O, C) de una fila específica
    
    Args:
        resultados: Dict devuelto por calcular_puntuaciones_directas
        row: Número de fila (1-14)
        
    Returns:
        dict: {'TR': valor, 'TA': valor, 'O': valor, 'C': valor} o None si la fila no existe
    """
    return resultados['indices_por_fila'].get(row)


def obtener_celdas_seleccionadas(resultados):
    """
    Obtiene el conjunto de todas las celdas seleccionadas
    
    Args:
        resultados: Dict devuelto por calcular_puntuaciones_directas
        
    Returns:
        set: Conjunto de tuplas (row, column) para todas las celdas seleccionadas
    """
    return resultados['celdas_seleccionadas']['seleccionadas']


def obtener_celdas_no_seleccionadas(resultados):
    """
    Obtiene el conjunto de todas las celdas no seleccionadas
    
    Args:
        resultados: Dict devuelto por calcular_puntuaciones_directas
        
    Returns:
        set: Conjunto de tuplas (row, column) para todas las celdas no seleccionadas
    """
    return resultados['celdas_seleccionadas']['no_seleccionadas']


def obtener_resumen_indices(resultados):
    """
    Obtiene un resumen legible de todos los índices calculados
    
    Args:
        resultados: Dict devuelto por calcular_puntuaciones_directas
        
    Returns:
        str: Texto con resumen formateado de todos los índices
    """
    lineas = []
    lineas.append("=" * 70)
    lineas.append("RESUMEN DE ÍNDICES DEL TEST D2")
    lineas.append("=" * 70)
    lineas.append("")
    
    # Índices globales
    lineas.append("ÍNDICES GLOBALES:")
    lineas.append(f"  TR_total (Total intentado): {resultados['TR_total']}")
    lineas.append(f"  TA_total (Total aciertos): {resultados['TA_total']}")
    lineas.append(f"  O_total (Omisiones): {resultados['O_total']}")
    lineas.append(f"  C_total (Comisiones): {resultados['C_total']}")
    lineas.append(f"  E_total (Errores totales O+C): {resultados['E_total']}")
    lineas.append(f"  TOT (Rendimiento neto TR-E): {resultados['TOT']}")
    lineas.append(f"  CON (Concentración TA-C): {resultados['CON']}")
    lineas.append(f"  TR_max (TR máximo): {resultados['TR_max']}")
    lineas.append(f"  TR_min (TR mínimo): {resultados['TR_min']}")
    lineas.append(f"  VAR (Variabilidad): {resultados['VAR']}")
    lineas.append("")
    
    # Índices por fila
    lineas.append("ÍNDICES POR FILA:")
    for row in sorted(resultados['indices_por_fila'].keys()):
        indices = resultados['indices_por_fila'][row]
        lineas.append(f"  Fila {row:2d}: TR={indices['TR']:2d}, TA={indices['TA']:2d}, "
                     f"O={indices['O']:2d}, C={indices['C']:2d}")
    lineas.append("")
    
    # Estadísticas de selección
    total_celdas = len(resultados['celdas_seleccionadas']['seleccionadas']) + \
                   len(resultados['celdas_seleccionadas']['no_seleccionadas'])
    lineas.append("ESTADÍSTICAS DE SELECCIÓN:")
    lineas.append(f"  Total de celdas: {total_celdas}")
    lineas.append(f"  Celdas seleccionadas: {len(resultados['celdas_seleccionadas']['seleccionadas'])}")
    lineas.append(f"  Celdas no seleccionadas: {len(resultados['celdas_seleccionadas']['no_seleccionadas'])}")
    lineas.append("")
    lineas.append("=" * 70)
    
    return "\n".join(lineas)


def mostrar_celdas_seleccionadas(resultados):
    """
    Muestra en la terminal las celdas seleccionadas.

    Args:
        resultados: Dict devuelto por calcular_puntuaciones_directas
    """
    celdas = obtener_celdas_seleccionadas(resultados)
    print("Celdas seleccionadas:")
    for celda in sorted(celdas):
        print(f"  Fila: {celda[0]}, Columna: {celda[1]}")