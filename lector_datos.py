"""
Módulo para leer datos del test Raven desde archivos Excel

Este módulo proporciona funciones para:
- Leer datos del Excel del test Raven
- Calcular puntuaciones directas por fila y totales
- Identificar explícitamente celdas seleccionadas y no seleccionadas
- Proporcionar estructuras de datos claras y accesibles para análisis posterior
"""
import pandas as pd


def leer_datos_excel(ruta_archivo):
    """
    Lee los datos del archivo Excel del test Raven
    
    Args:
        ruta_archivo: Ruta al archivo Excel
        
    Returns:
        dict: Diccionario con 'edad', 'sub_num', 'nombre_completo', 'nombre' y 'datos_Raven'
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
        
        # Leer hoja 'Ravens Matrices' con los datos del test
        df_raven = pd.read_excel(ruta_archivo, sheet_name='Ravens Matrices')
        
        return {
            'edad': edad,
            'sub_num': sub_num,
            'nombre_completo': nombre_completo,
            'nombre': nombre,
            'datos_raven': df_raven
        }
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        raise


def calcular_puntuaciones_directas(datos):
    """
    Calcula las puntuaciones directas del test Raven
    
    Args:
        datos: Dict con 'edad' y 'datos_raven'
        
    Returns:
        dict: Diccionario con todas las puntuaciones directas y por fila.
              Incluye estructuras explícitas para:
                - Respuestas dadas
                - Respuestas  correctas
    """
    df = datos['datos_raven']
    
    # Agrupar por fila (row)
    rows = df['row'].unique()
    rows = sorted(rows)
    
    
    resultados = {
        'edad': datos['edad'],
        'sub_num': datos.get('sub_num'),
        'nombre_completo': datos.get('nombre_completo'),
        'nombre': datos.get('nombre'),
        'datos_raven': df,  # Incluir DataFrame para generador_imagen_final
        
        # Índices totales
        'PD_A': 0,
        'PD_B': 0,
        'PD_C': 0,
        'PD_D': 0,
        'PD_E': 0,
        'PD_total': 0,
        'Indice_discrepancia_A': 0,
        'Indice_discrepancia_B': 0,
        'Indice_discrepancia_C': 0,
        'Indice_discrepancia_D': 0,
        'Indice_discrepancia_E': 0,
    }
    
    for row in rows:
        df_row = df[df['row'] == row]
        
    
    # Calcular totales
    resultados['PD_total'] = sum(resultados['PD_por_fila'])

    # TOT = TR_total - E_total (rendimiento neto)
    resultados['Discrepancia'] = resultados['PD_dada_por_fila'] - resultados['PD_esperada_por_fila']
    
    return resultados


# ============================================================================
# FUNCIONES DE UTILIDAD PARA CONSULTAR RESULTADOS
# ============================================================================

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
    lineas.append("RESUMEN DE ÍNDICES DEL TEST RAVENS MATRICES")
    lineas.append("=" * 70)
    lineas.append("")
    
    # Índices globales
    lineas.append("ÍNDICES GLOBALES:")
    lineas.append(f"  PD_total: {resultados['PD_total']}")
    lineas.append(f"  Discrepancia: {resultados['Discrepancia']}")
    lineas.append("")
    
    # Índices por fila
    lineas.append("ÍNDICES POR FILA:")
    for row in sorted(resultados['indices_por_fila'].keys()):
        indices = resultados['indices_por_fila'][row]
        lineas.append(f"  Fila {row:2d}: PD={indices['PD']:2d}, Discrepancia={indices['Discrepancia']:2d}, ")
    lineas.append("")    

    
    return "\n".join(lineas)