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
    elif 15 <= edad <= 18:
        return 'PT_15_a_18'
    elif 18 <= edad <= 20:
        return 'PT_18_a_20'
    elif 20 <= edad <= 25:
        return 'PT_20_a_25'
    elif 25 <= edad <= 30:
        return 'PT_25_a_30'
    elif 30 <= edad <= 35:
        return 'PT_30_a_35'
    elif 35 <= edad <= 40:
        return 'PT_35_a_40'
    elif 40 <= edad <= 45:
        return 'PT_40_a_45'
    elif 45 <= edad <= 50:
        return 'PT_45_a_50'
    elif 50 <= edad <= 55:
        return 'PT_50_a_55'
    elif 55 <= edad <= 60:
        return 'PT_55_a_60'
    elif 60 <= edad <= 65:
        return 'PT_60_a_65'
    elif edad >= 65:
        return 'PT_65_o_mas'
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
        'PT_6': {'pc5': 8, 'pc10': 9, 'pc25': 13, 'pc50': 20, 'pc75': 27, 'pc90': 32, 'pc95': 35},
        'PT_6.6': {'pc5': 9, 'pc10': 11, 'pc25': 15, 'pc50': 22, 'pc75': 29, 'pc90': 34, 'pc95': 37},
        'PT_7': {'pc5': 11, 'pc10': 13, 'pc25': 18, 'pc50': 25, 'pc75': 32, 'pc90': 36, 'pc95': 39},
        'PT_7.6': {'pc5': 12, 'pc10': 14, 'pc25': 21, 'pc50': 28, 'pc75': 36, 'pc90': 39, 'pc95': 41},
        'PT_8': {'pc5': 13, 'pc10': 15, 'pc25': 23, 'pc50': 30, 'pc75': 38, 'pc90': 42, 'pc95': 44},
        'PT_8.6': {'pc5': 13, 'pc10': 16, 'pc25': 25, 'pc50': 32, 'pc75': 39, 'pc90': 44, 'pc95': 46},
        'PT_9': {'pc5': 15, 'pc10': 19, 'pc25': 28, 'pc50': 35, 'pc75': 42, 'pc90': 46, 'pc95': 47},
        'PT_9.6': {'pc5': 16, 'pc10': 20, 'pc25': 30, 'pc50': 36, 'pc75': 43, 'pc90': 48, 'pc95': 50},
        'PT_10': {'pc5': 17, 'pc10': 20, 'pc25': 27, 'pc50': 34, 'pc75': 41, 'pc90': 47, 'pc95': 50},
        'PT_11': {'pc5': 22, 'pc10': 25, 'pc25': 31, 'pc50': 38, 'pc75': 44, 'pc90': 50, 'pc95': 52},
        'PT_12': {'pc5': 24, 'pc10': 27, 'pc25': 33, 'pc50': 40, 'pc75': 46, 'pc90': 52, 'pc95': 54},
        'PT_13': {'pc5': 31, 'pc10': 34, 'pc25': 38, 'pc50': 43, 'pc75': 49, 'pc90': 53, 'pc95': 56},
        'PT_14': {'pc5': 36, 'pc10': 38, 'pc25': 42, 'pc50': 46, 'pc75': 51, 'pc90': 55, 'pc95': 58},
        'PT_15_a_18': {'pc5': 38, 'pc10': 40, 'pc25': 44, 'pc50': 48, 'pc75': 52, 'pc90': 56, 'pc95': 59},
        'PT_18_a_20': {'pc5': 35, 'pc10': 37, 'pc25': 41, 'pc50': 46, 'pc75': 50, 'pc90': 54, 'pc95': 57},
        'PT_20_a_25': {'pc5': 23, 'pc10': 28, 'pc25': 37, 'pc50': 44, 'pc75': 49, 'pc90': 54, 'pc95': 55},
        'PT_25_a_30': {'pc5': 23, 'pc10': 28, 'pc25': 37, 'pc50': 44, 'pc75': 49, 'pc90': 54, 'pc95': 57},
        'PT_30_a_35': {'pc5': 23, 'pc10': 28, 'pc25': 34, 'pc50': 42, 'pc75': 47, 'pc90': 53, 'pc95': 54},
        'PT_35_a_40': {'pc5': 23, 'pc10': 28, 'pc25': 30, 'pc50': 40, 'pc75': 45, 'pc90': 51, 'pc95': 53},
        'PT_40_a_45': {'pc5': 23, 'pc10': 28, 'pc25': 27, 'pc50': 38, 'pc75': 43, 'pc90': 52, 'pc95': 52},
        'PT_45_a_50': {'pc5': 23, 'pc10': 28, 'pc25': 24, 'pc50': 35, 'pc75': 41, 'pc90': 47, 'pc95': 50},
        'PT_50_a_55': {'pc5': 23, 'pc10': 28, 'pc25': 21, 'pc50': 33, 'pc75': 39, 'pc90': 45, 'pc95': 48},
        'PT_55_a_60': {'pc5': 23, 'pc10': 28, 'pc25': 18, 'pc50': 30, 'pc75': 37, 'pc90': 43, 'pc95': 46},
        'PT_60_a_65': {'pc5': 23, 'pc10': 28, 'pc25': 15, 'pc50': 27, 'pc75': 35, 'pc90': 41, 'pc95': 44},
        'PT_165_o_mas': {'pc5': 23, 'pc10': 28, 'pc25': 12, 'pc50': 24, 'pc75': 33, 'pc90': 39, 'pc95': 42},
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
        'PD10': {'A': 6, 'B': 2, 'C': 1, 'D': 1, 'E': 0},
        'PD11': {'A': 7, 'B': 2, 'C': 2, 'D': 1, 'E': 0},
        'PD12': {'A': 8, 'B': 2, 'C': 2, 'D': 1, 'E': 0},
        'PD13': {'A': 8, 'B': 3, 'C': 2, 'D': 1, 'E': 0},
        'PD14': {'A': 8, 'B': 3, 'C': 1, 'D': 1, 'E': 1},
        'PD15': {'A': 8, 'B': 3, 'C': 2, 'D': 1, 'E': 1},
        'PD16': {'A': 8, 'B': 4, 'C': 2, 'D': 1, 'E': 1},
        'PD17': {'A': 9, 'B': 4, 'C': 2, 'D': 1, 'E': 1},
        'PD18': {'A': 9, 'B': 4, 'C': 2, 'D': 2, 'E': 1},
        'PD19': {'A': 9, 'B': 5, 'C': 2, 'D': 2, 'E': 1},
        'PD20': {'A': 9, 'B': 5, 'C': 3, 'D': 2, 'E': 1},
        'PD21': {'A': 9, 'B': 5, 'C': 4, 'D': 2, 'E': 1},
        'PD22': {'A': 9, 'B': 5, 'C': 4, 'D': 3, 'E': 1},
        'PD23': {'A': 9, 'B': 6, 'C': 4, 'D': 3, 'E': 1},
        'PD24': {'A': 9, 'B': 6, 'C': 5, 'D': 3, 'E': 1},
        'PD25': {'A': 9, 'B': 6, 'C': 5, 'D': 4, 'E': 1},
        'PD26': {'A': 9, 'B': 6, 'C': 5, 'D': 5, 'E': 1},
        'PD27': {'A': 9, 'B': 7, 'C': 5, 'D': 5, 'E': 1},
        'PD28': {'A': 10, 'B': 7, 'C': 5, 'D': 5, 'E': 1},
        'PD29': {'A': 10, 'B': 7, 'C': 6, 'D': 5, 'E': 1},
        'PD30': {'A': 10, 'B': 7, 'C': 6, 'D': 5, 'E': 2},
        'PD31': {'A': 10, 'B': 8, 'C': 6, 'D': 5, 'E': 2},
        'PD32': {'A': 10, 'B': 8, 'C': 6, 'D': 6, 'E': 2},
        'PD33': {'A': 10, 'B': 8, 'C': 7, 'D': 6, 'E': 2},
        'PD34': {'A': 10, 'B': 8, 'C': 7, 'D': 7, 'E': 2},
        'PD35': {'A': 10, 'B': 9, 'C': 7, 'D': 7, 'E': 2},
        'PD36': {'A': 11, 'B': 9, 'C': 7, 'D': 7, 'E': 2},
        'PD37': {'A': 11, 'B': 9, 'C': 7, 'D': 8, 'E': 2},
        'PD38': {'A': 11, 'B': 10, 'C': 7, 'D': 8, 'E': 2},
        'PD39': {'A': 11, 'B': 10, 'C': 8, 'D': 8, 'E': 2},
        'PD40': {'A': 11, 'B': 10, 'C': 8, 'D': 8, 'E': 3},
        'PD41': {'A': 11, 'B': 10, 'C': 8, 'D': 9, 'E': 3},
        'PD42': {'A': 11, 'B': 10, 'C': 8, 'D': 9, 'E': 4},
        'PD43': {'A': 11, 'B': 11, 'C': 8, 'D': 9, 'E': 4},
        'PD44': {'A': 11, 'B': 11, 'C': 9, 'D': 9, 'E': 4},
        'PD45': {'A': 12, 'B': 11, 'C': 9, 'D': 9, 'E': 4},
        'PD46': {'A': 12, 'B': 11, 'C': 9, 'D': 9, 'E': 5},
        'PD47': {'A': 12, 'B': 11, 'C': 9, 'D': 10, 'E': 5},
        'PD48': {'A': 12, 'B': 11, 'C': 9, 'D': 10, 'E': 6},
        'PD49': {'A': 12, 'B': 11, 'C': 10, 'D': 10, 'E': 6},
        'PD50': {'A': 12, 'B': 11, 'C': 10, 'D': 10, 'E': 7},
        'PD51': {'A': 12, 'B': 11, 'C': 10, 'D': 10, 'E': 8},
        'PD52': {'A': 12, 'B': 12, 'C': 10, 'D': 10, 'E': 8},
        'PD53': {'A': 12, 'B': 12, 'C': 11, 'D': 10, 'E': 8},
        'PD54': {'A': 12, 'B': 12, 'C': 11, 'D': 10, 'E': 9},
        'PD55': {'A': 12, 'B': 12, 'C': 11, 'D': 11, 'E': 9},
        'PD56': {'A': 12, 'B': 12, 'C': 11, 'D': 11, 'E': 10},
        'PD57': {'A': 12, 'B': 12, 'C': 12, 'D': 11, 'E': 10},
        'PD58': {'A': 12, 'B': 12, 'C': 12, 'D': 11, 'E': 11},
        'PD59': {'A': 12, 'B': 12, 'C': 12, 'D': 12, 'E': 11},
        'PD60': {'A': 12, 'B': 12, 'C': 12, 'D': 12, 'E': 12},
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
