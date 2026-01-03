"""
Módulo con las reglas psicométricas y baremos del test D2
"""


def obtener_baremos_edad(edad):
    """
    Retorna los baremos apropiados según la edad
    Basado en las tablas A.1 a A.11 del manual
    """
    if 8 <= edad <= 10:
        return 'A1_8_10'
    elif 11 <= edad <= 12:
        return 'A2_11_12'
    elif 13 <= edad <= 14:
        return 'A3_13_14'
    elif 15 <= edad <= 16:
        return 'A4_15_16'
    elif 17 <= edad <= 18:
        return 'A5_17_18'
    elif 19 <= edad <= 23:
        return 'A6_19_23'
    elif 24 <= edad <= 29:
        return 'A7_24_29'
    elif 30 <= edad <= 39:
        return 'A8_30_39'
    elif edad >= 40:
        return 'A9_40_mas'
    else:
        return 'A10_adolescentes'  # Por defecto

def clasificar_TR(TR_total, edad):
    """
    Clasifica la velocidad de procesamiento (TR) en 5 niveles
    
    Niveles:
    - 'muy bajo': Pc < 20
    - 'bajo': Pc 20-40
    - 'normal': Pc 40-60
    - 'alto': Pc 60-80
    - 'muy alto': Pc 80-100
    """
    baremos = {
        'A1_8_10': {'pc20': 181, 'pc40': 220, 'pc60': 253, 'pc80': 273},
        'A2_11_12': {'pc20': 246, 'pc40': 284, 'pc60': 327, 'pc80': 354},
        'A3_13_14': {'pc20': 289, 'pc40': 330, 'pc60': 371, 'pc80': 409},
        'A4_15_16': {'pc20': 348, 'pc40': 387, 'pc60': 415, 'pc80': 460},
        'A5_17_18': {'pc20': 356, 'pc40': 400, 'pc60': 432, 'pc80': 472},
        'A6_19_23': {'pc20': 389, 'pc40': 443, 'pc60': 481, 'pc80': 522},
        'A7_24_29': {'pc20': 378, 'pc40': 449, 'pc60': 493, 'pc80': 547},
        'A8_30_39': {'pc20': 380, 'pc40': 435, 'pc60': 490, 'pc80': 529},
        'A9_40_mas': {'pc20': 248, 'pc40': 308, 'pc60': 408, 'pc80': 480}
    }
    
    grupo = obtener_baremos_edad(edad)
    if grupo not in baremos:
        return 'normal'
    
    if TR_total < baremos[grupo]['pc20']:
        return 'muy bajo'
    elif TR_total < baremos[grupo]['pc40']:
        return 'bajo'
    elif TR_total < baremos[grupo]['pc60']:
        return 'normal'
    elif TR_total < baremos[grupo]['pc80']:
        return 'alto'
    else:
        return 'muy alto'

def clasificar_TA(TA, edad):
    """
    Clasifica el índice de concentración (TA) en 5 niveles
    
    Niveles:
    - 'muy bajo': Pc < 20 (muy desconcentrado)
    - 'bajo': Pc 20-40 (desconcentrado)
    - 'normal': Pc 40-60 (concentración normal)
    - 'alto': Pc 60-80 (concentrado)
    - 'muy alto': Pc 80-100 (muy concentrado)
    """
    baremos = {
        'A1_8_10': {'pc20': 66, 'pc40': 88, 'pc60': 101, 'pc80': 112},
        'A2_11_12': {'pc20': 96, 'pc40': 111, 'pc60': 128, 'pc80': 140},
        'A3_13_14': {'pc20': 112, 'pc40': 129, 'pc60': 143, 'pc80': 159},
        'A4_15_16': {'pc20': 124, 'pc40': 147, 'pc60': 159, 'pc80': 174},
        'A5_17_18': {'pc20': 139, 'pc40': 152, 'pc60': 165, 'pc80': 180},
        'A6_19_23': {'pc20': 150, 'pc40': 168, 'pc60': 189, 'pc80': 211},
        'A7_24_29': {'pc20': 148, 'pc40': 167, 'pc60': 186, 'pc80': 220},
        'A8_30_39': {'pc20': 141, 'pc40': 168, 'pc60': 189, 'pc80': 208},
        'A9_40_mas': {'pc20': 79, 'pc40': 117, 'pc60': 149, 'pc80': 175}
    }
    
    grupo = obtener_baremos_edad(edad)
    if grupo not in baremos:
        return 'normal'
    
    if TA < baremos[grupo]['pc20']:
        return 'muy bajo'
    elif TA < baremos[grupo]['pc40']:
        return 'bajo'
    elif TA < baremos[grupo]['pc60']:
        return 'normal'
    elif TA < baremos[grupo]['pc80']:
        return 'alto'
    else:
        return 'muy alto'

def clasificar_O(O_total, edad):
    """
    Clasifica los errores de omisión (O) en 5 niveles
    NOTA: Interpretación INVERSA (menos errores = mejor)
    
    Niveles:
    - 'muy bajo': Pc 80-100 (muy pocos errores = muy atento)
    - 'bajo': Pc 60-80 (pocos errores = atento)
    - 'normal': Pc 40-60 (errores normales)
    - 'alto': Pc 20-40 (bastantes errores = despistado)
    - 'muy alto': Pc < 20 (muchos errores = muy despistado)
    """
    baremos = {
        'A1_8_10': {'pc20': 9, 'pc40': 5, 'pc60': 3, 'pc80': 1},
        'A2_11_12': {'pc20': 14, 'pc40': 8, 'pc60': 5, 'pc80': 2},
        'A3_13_14': {'pc20': 18, 'pc40': 11, 'pc60': 6, 'pc80': 3},
        'A4_15_16': {'pc20': 27, 'pc40': 15, 'pc60': 9, 'pc80': 5},
        'A5_17_18': {'pc20': 23, 'pc40': 13, 'pc60': 9, 'pc80': 5},
        'A6_19_23': {'pc20': 17, 'pc40': 12, 'pc60': 8, 'pc80': 4},
        'A7_24_29': {'pc20': 23, 'pc40': 16, 'pc60': 9, 'pc80': 5},
        'A8_30_39': {'pc20': 26, 'pc40': 15, 'pc60': 9, 'pc80': 5},
        'A9_40_mas': {'pc20': 28, 'pc40': 16, 'pc60': 11, 'pc80': 5}
    }
    
    grupo = obtener_baremos_edad(edad)
    if grupo not in baremos:
        return 'normal'
    
    # Interpretación inversa: menos errores = mejor clasificación
    if O_total > baremos[grupo]['pc20']:
        return 'muy alto'  # Muchos errores
    elif O_total > baremos[grupo]['pc40']:
        return 'alto'  # Bastantes errores
    elif O_total > baremos[grupo]['pc60']:
        return 'normal'
    elif O_total > baremos[grupo]['pc80']:
        return 'bajo'  # Pocos errores
    else:
        return 'muy bajo'  # Muy pocos errores


def clasificar_C(C_total, edad):
    """
    Clasifica los errores de comisión (C) en 5 niveles
    NOTA: Interpretación INVERSA (menos errores = mejor)
    
    Niveles:
    - 'muy bajo': Pc 80-100 (muy pocos errores = muy preciso)
    - 'bajo': Pc 60-80 (pocos errores = preciso)
    - 'normal': Pc 40-60 (errores normales)
    - 'alto': Pc 20-40 (bastantes errores = impreciso)
    - 'muy alto': Pc < 20 (muchos errores = muy impreciso)
    """
    baremos = {
        'A1_8_10': {'pc20': 9, 'pc40': 5, 'pc60': 3, 'pc80': 1},
        'A2_11_12': {'pc20': 4, 'pc40': 2, 'pc60': 1, 'pc80': 0},
        'A3_13_14': {'pc20': 3, 'pc40': 1, 'pc60': 0, 'pc80': 0},
        'A4_15_16': {'pc20': 4, 'pc40': 2, 'pc60': 0, 'pc80': 0},
        'A5_17_18': {'pc20': 4, 'pc40': 1, 'pc60': 0, 'pc80': 0},
        'A6_19_23': {'pc20': 1, 'pc40': 0, 'pc60': 0, 'pc80': 0},
        'A7_24_29': {'pc20': 1, 'pc40': 0, 'pc60': 0, 'pc80': 0},
        'A8_30_39': {'pc20': 2, 'pc40': 1, 'pc60': 0, 'pc80': 0},
        'A9_40_mas': {'pc20': 5, 'pc40': 2, 'pc60': 0, 'pc80': 0}
    }
    
    grupo = obtener_baremos_edad(edad)
    if grupo not in baremos:
        return 'normal'
    
    # Interpretación inversa: menos errores = mejor clasificación
    if C_total > baremos[grupo]['pc20']:
        return 'muy alto'  # Muchos errores
    elif C_total > baremos[grupo]['pc40']:
        return 'alto'  # Bastantes errores
    elif C_total > baremos[grupo]['pc60']:
        return 'normal'
    elif C_total > baremos[grupo]['pc80']:
        return 'bajo'  # Pocos errores
    else:
        return 'muy bajo'  # Muy pocos errores

def clasificar_TOT(TOT, edad):
    """
    Clasifica el índice de (TOT) en 5 niveles
    
    Niveles:
    - 'muy bajo': Pc < 20
    - 'bajo': Pc 20-40 
    - 'normal': Pc 40-60 
    - 'alto': Pc 60-80 
    - 'muy alto': Pc 80-100 
    """
    baremos = {
        'A1_8_10': {'pc20': 161, 'pc40': 211, 'pc60': 237, 'pc80': 264},
        'A2_11_12': {'pc20': 240, 'pc40': 271, 'pc60': 309, 'pc80': 341},
        'A3_13_14': {'pc20': 277, 'pc40': 318, 'pc60': 356, 'pc80': 392},
        'A4_15_16': {'pc20': 319, 'pc40': 372, 'pc60': 400, 'pc80': 436},
        'A5_17_18': {'pc20': 340, 'pc40': 384, 'pc60': 413, 'pc80': 443},
        'A6_19_23': {'pc20': 370, 'pc40': 421, 'pc60': 462, 'pc80': 508},
        'A7_24_29': {'pc20': 364, 'pc40': 422, 'pc60': 470, 'pc80': 523},
        'A8_30_39': {'pc20': 359, 'pc40':414, 'pc60': 471, 'pc80': 506},
        'A9_40_mas': {'pc20':204, 'pc40': 290, 'pc60': 381, 'pc80': 445}
    }
    
    grupo = obtener_baremos_edad(edad)
    if grupo not in baremos:
        return 'normal'
    
    if TOT < baremos[grupo]['pc20']:
        return 'muy bajo'
    elif TOT < baremos[grupo]['pc40']:
        return 'bajo'
    elif TOT < baremos[grupo]['pc60']:
        return 'normal'
    elif TOT < baremos[grupo]['pc80']:
        return 'alto'
    else:
        return 'muy alto'

def clasificar_CON(CON, edad):
    """
    Clasifica el índice de concentración (CON) en 5 niveles
    
    Niveles:
    - 'muy bajo': Pc < 20 (muy desconcentrado)
    - 'bajo': Pc 20-40 (desconcentrado)
    - 'normal': Pc 40-60 (concentración normal)
    - 'alto': Pc 60-80 (concentrado)
    - 'muy alto': Pc 80-100 (muy concentrado)
    """
    baremos = {
        'A1_8_10': {'pc20': 61, 'pc40': 83, 'pc60': 99, 'pc80': 110},
        'A2_11_12': {'pc20': 92, 'pc40': 109, 'pc60': 126, 'pc80': 138},
        'A3_13_14': {'pc20': 109, 'pc40': 126, 'pc60': 139, 'pc80': 157},
        'A4_15_16': {'pc20': 118, 'pc40': 144, 'pc60': 158, 'pc80': 171},
        'A5_17_18': {'pc20': 134, 'pc40': 150, 'pc60': 163, 'pc80': 177},
        'A6_19_23': {'pc20': 148, 'pc40': 167, 'pc60': 188, 'pc80': 211},
        'A7_24_29': {'pc20': 144, 'pc40': 166, 'pc60': 185, 'pc80': 219},
        'A8_30_39': {'pc20': 140, 'pc40': 167, 'pc60': 187, 'pc80': 206},
        'A9_40_mas': {'pc20': 74, 'pc40': 110, 'pc60': 134, 'pc80': 173}
    }
    
    grupo = obtener_baremos_edad(edad)
    if grupo not in baremos:
        return 'normal'
    
    if CON < baremos[grupo]['pc20']:
        return 'muy bajo'
    elif CON < baremos[grupo]['pc40']:
        return 'bajo'
    elif CON < baremos[grupo]['pc60']:
        return 'normal'
    elif CON < baremos[grupo]['pc80']:
        return 'alto'
    else:
        return 'muy alto'


def clasificar_VAR(VAR, edad):
    """
    Clasifica la variabilidad (VAR) en 5 niveles
    NOTA: Interpretación especial (baja variabilidad = estable = mejor)
    
    Niveles:
    - 'muy bajo': Pc < 20 (muy estable)
    - 'bajo': Pc 20-40  (estable)
    - 'normal': Pc 40-60 (variabilidad normal)
    - 'alto': Pc 60-80 (variable)
    - 'muy alto': Pc 80-100(muy variable)
    """
    baremos = {
        'A1_8_10': {'pc20': 10, 'pc40': 12, 'pc60': 15, 'pc80': 19},
        'A2_11_12': {'pc20': 10, 'pc40': 13, 'pc60': 16, 'pc80': 20},
        'A3_13_14': {'pc20': 13, 'pc40': 16, 'pc60': 19, 'pc80': 23},
        'A4_15_16': {'pc20': 12, 'pc40': 15, 'pc60': 19, 'pc80': 24},
        'A5_17_18': {'pc20': 16, 'pc40': 20, 'pc60': 24, 'pc80': 26},
        'A6_19_23': {'pc20': 10, 'pc40': 12, 'pc60': 14, 'pc80': 17},
        'A7_24_29': {'pc20': 9, 'pc40': 12, 'pc60': 15, 'pc80': 17},
        'A8_30_39': {'pc20': 10, 'pc40': 13, 'pc60': 16, 'pc80': 19},
        'A9_40_mas': {'pc20': 6, 'pc40': 14, 'pc60': 19, 'pc80': 24}
    }
    
    grupo = obtener_baremos_edad(edad)
    if grupo not in baremos:
        return 'normal'
    
    # Interpretación inversa: menos variabilidad = mejor (más estable)
    if VAR < baremos[grupo]['pc20']:
        return 'muy bajo'  # Muy variable
    elif VAR < baremos[grupo]['pc40']:
        return 'bajo'  # Variable
    elif VAR < baremos[grupo]['pc60']:
        return 'normal'
    elif VAR < baremos[grupo]['pc80']:
        return 'alto'  # Estable
    else:
        return 'muy alto'  # Muy estable


def detectar_condicion_var_especial(resultados):
    """
    Detecta si se cumple la condición especial de VAR:
    - VAR es alto o muy alto
    - Y la serie con TR_max está 7 filas o más por detrás de la serie con TR_min
    
    Args:
        resultados: Dict con puntuaciones directas y edad
        
    Returns:
        bool: True si se cumple la condición especial
    """
    edad = resultados['edad']
    clasificacion_var = clasificar_VAR(resultados['VAR'], edad)
    
    # Verificar si VAR es alto o muy alto
    if clasificacion_var not in ['alto', 'muy alto']:
        return False
    
    # Verificar separación de filas
    # TR_max debe estar 7 o más filas POR DETRÁS (después) de TR_min
    if 'TR_max_pos' in resultados and 'TR_min_pos' in resultados:
        separacion = resultados['TR_max_pos'] - resultados['TR_min_pos']
        return separacion >= 7
    
    return False


def obtener_puntuaciones_tipicas(resultados):
    """
    Obtiene las puntuaciones típicas basadas en las puntuaciones directas
    
    Args:
        resultados: Dict con puntuaciones directas y edad
        
    Returns:
        dict: Diccionario con clasificaciones en 5 niveles
    """
    edad = resultados['edad']
    
    clasificaciones = {
        'TR': clasificar_TR(resultados['TR_total'], edad),
        'TA': clasificar_TA(resultados['TA_total'], edad),
        'O': clasificar_O(resultados['O_total'], edad),
        'C': clasificar_C(resultados['C_total'], edad),
        'TOT': clasificar_TOT(resultados['TOT'], edad),
        'CON': clasificar_CON(resultados['CON'], edad),
        'VAR': clasificar_VAR(resultados['VAR'], edad),
        'VAR_especial': detectar_condicion_var_especial(resultados)
    }
    
    return clasificaciones