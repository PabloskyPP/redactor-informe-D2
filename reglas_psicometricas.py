"""
Módulo con las reglas psicométricas y baremos del test Raven
"""


def obtener_baremos_edad(edad):
    """
    Retorna los baremos apropiados según la edad
    Basado en las tablas A.1 a A.11 del manual
    """
    if 6 <= edad <= 6.6:
        return 'PT_6'
    elif 6.6  <= edad <= 7:
        return 'PT_6.6'
    elif 7 <= edad <= 7.6:
        return 'PT_7'
    elif 7.6 <= edad <= 8:
        return 'PT_7.6'
    elif 8 <= edad <= 8.6:
        return 'PT_8'
    elif 8.6 <= edad <= 9:
        return 'PT_8.6'
    elif 9 <= edad <= 9.6:
        return 'PT_9'
    elif 9.6 <= edad <= 10:
        return 'PT_9.6'
    elif 10 <= edad <= 11:
        return 'PT_10'
    elif 11 <= edad <= 12:
        return 'PT_11'
    elif 12 <= edad <= 13:
        return 'PT_12'
    elif 13 <= edad <= 14:
        return 'PT_13'
    elif 14 <= edad <= 15:
        return 'PT_14'
    elif 15 <= edad <= 16:
        return 'PT_15'
    elif 16 <= edad <= 17:
        return 'PT_16'
    elif 17 <= edad <= 18:
        return 'PT_17'
    elif 18 <= edad <= 19:
        return 'PT_18'
    elif edad >= 19:
        return 'PT_19_mas'
    else:
        return 'Error participante menor de 6 años, grupo sin baremo'

def clasificar_TR(PD_total, edad):
    """
    Clasifica la PD_total en 5 niveles
    
    Niveles:
    - 'muy bajo': Pc < 20
    - 'bajo': Pc 20-40
    - 'normal': Pc 40-60
    - 'alto': Pc 60-80
    - 'muy alto': Pc 80-100
    """
    baremos = {
        'A1_8_10': {'pc5': 273, 'pc10': 273, 'pc25': 181, 'pc50': 220, 'pc75': 253, 'pc90': 273, 'pc95': 273},
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



def detectar_discrepancia_significativa(resultados):
    """
    Detecta si se cumple la condición especial de índice de discrepancia > 2, y por tanto significativo
    
    Args:
        resultados: Dict con puntuaciones directas y edad
        
    Returns:
        bool: True si se cumple la condición especial
    """
    puntuaciones_esperadas = {
        'PD10': {'A': 6,'B': 2,'C': 1,'D': 1,'E': 0}
        'PD11': {'A': 7, 'B': 3, 'C': 2, 'D': 1, 'E': 0},
        'PD12': {'A': 8, 'B': 4, 'C': 2, 'D': 1, 'E': 0},
        'PD13': {'A': 9, 'B': 5, 'C': 3, 'D': 2, 'E': 1},
        'PD14': {'A': 10, 'B': 6, 'C': 3, 'D': 2, 'E': 1},
        'PD15': {'A': 11, 'B': 7, 'C': 4, 'D': 2, 'E': 1},
        'PD16': {'A': 12, 'B': 8, 'C': 4, 'D': 3, 'E': 1},
        'PD17': {'A': 13, 'B': 9, 'C': 5, 'D': 3, 'E': 2},
        'PD18': {'A': 14, 'B': 10, 'C': 5, 'D': 3, 'E': 2},
        'PD19': {'A': 15, 'B': 11, 'C': 6, 'D': 4, 'E': 2},
        'PD20': {'A': 16, 'B': 12, 'C': 6, 'D': 4, 'E': 2},
        'PD21': {'A': 17, 'B': 13, 'C': 7, 'D': 4, 'E': 3},
        'PD22': {'A': 18, 'B': 14, 'C': 7, 'D': 5, 'E': 3},
        'PD23': {'A': 19, 'B': 15, 'C': 8, 'D': 5, 'E': 3},
        'PD24': {'A': 20, 'B': 16, 'C': 8, 'D': 5, 'E': 3},
        'PD25': {'A': 21, 'B': 17, 'C': 9, 'D': 6, 'E': 4},
        'PD26': {'A': 22, 'B': 18, 'C': 9, 'D': 6, 'E': 4},
        'PD27': {'A': 23, 'B': 19, 'C': 10, 'D': 6, 'E': 4},
        'PD28': {'A': 24, 'B': 20, 'C': 10, 'D': 7, 'E': 4},
        'PD29': {'A': 25, 'B': 21, 'C': 11, 'D': 7, 'E': 5},
        'PD30': {'A': 26, 'B': 22, 'C': 11, 'D': 7, 'E': 5},
        'PD31': {'A': 27, 'B': 23, 'C': 12, 'D': 8, 'E': 5},
        'PD32': {'A': 28, 'B': 24, 'C': 12, 'D': 8, 'E': 5},
        'PD33': {'A': 29, 'B': 25, 'C': 13, 'D': 8, 'E': 6},
        'PD34': {'A': 30, 'B': 26, 'C': 13, 'D': 9, 'E': 6},
        'PD35': {'A': 31, 'B': 27, 'C': 14, 'D': 9, 'E': 6},
        'PD36': {'A': 32, 'B': 28, 'C': 14, 'D': 9, 'E': 6},
        'PD37': {'A': 33, 'B': 29, 'C': 15, 'D': 10, 'E': 7},
        'PD38': {'A': 34, 'B': 30, 'C': 15, 'D': 10, 'E': 7},
        'PD39': {'A': 35, 'B': 31, 'C': 16, 'D': 10, 'E': 7},
        'PD40': {'A': 36, 'B': 32, 'C': 16, 'D': 11, 'E': 7},
        'PD41': {'A': 37, 'B': 33, 'C': 17, 'D': 11, 'E': 8},
        'PD42': {'A': 38, 'B': 34, 'C': 17, 'D': 11, 'E': 8},
        'PD43': {'A': 39, 'B': 35, 'C': 18, 'D': 12, 'E': 8},
        'PD44': {'A': 40, 'B': 36, 'C': 18, 'D': 12, 'E': 8},
        'PD45': {'A': 41, 'B': 37, 'C': 19, 'D': 12, 'E': 9},
        'PD46': {'A': 42, 'B': 38, 'C': 19, 'D': 13, 'E': 9},
        'PD47': {'A': 43, 'B': 39, 'C': 20, 'D': 13, 'E': 9},
        'PD48': {'A': 44, 'B': 40, 'C': 20, 'D': 13, 'E': 9},
        'PD49': {'A': 45, 'B': 41, 'C': 21, 'D': 14, 'E': 10},
        'PD50': {'A': 46, 'B': 42, 'C': 21, 'D': 14, 'E': 10},
        'PD51': {'A': 47, 'B': 43, 'C': 22, 'D': 14, 'E': 10},
        'PD52': {'A': 48, 'B': 44, 'C': 22, 'D': 15, 'E': 10},
        'PD53': {'A': 49, 'B': 45, 'C': 23, 'D': 15, 'E': 11},
        'PD54': {'A': 50, 'B': 46, 'C': 23, 'D': 15, 'E': 11},
        'PD55': {'A': 51, 'B': 47, 'C': 24, 'D': 16, 'E': 11},
        'PD56': {'A': 52, 'B': 48, 'C': 24, 'D': 16, 'E': 11},
        'PD57': {'A': 53, 'B': 49, 'C': 25, 'D': 16, 'E': 12},
        'PD58': {'A': 54, 'B': 50, 'C': 25, 'D': 17, 'E': 12},
        'PD59': {'A': 55, 'B': 51, 'C': 26, 'D': 17, 'E': 12},
        'PD60': {'A': 56, 'B': 52, 'C': 26, 'D': 17, 'E': 12},
    }
    
                              
    discrepancia_significativa = detectar_discrepancia_significativa(resultados['discrepancia'], edad)
    
    # Verificar si discrepancia es significativa
    if discrepancia_significativa:
        return True    # discrepancia debe ser menor que 3 en todas las series: A, B, C, D, E

    else:
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
        'PT': clasificar_PD(resultados['PD_total'], edad),
    }
    
    return clasificaciones
