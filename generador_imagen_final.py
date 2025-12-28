"""
Módulo para generar la imagen final grafico_D2_final.png con superposiciones gráficas

Este módulo toma como base grafico_D2.png y genera una versión final con:
- Textos rotados de puntuaciones globales (TR_total, TA_total, O_total, C_total)
- Cuadros de texto por fila para cada índice (TR, TA, O, C)
- Puntos negros en posiciones donde selected != 'FALSE' (items seleccionados)
- Líneas conectando últimos puntos de filas consecutivas

Nota: El Excel usa el valor 'FALSE' en inglés, no 'FALSO'
"""

import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd


# ============================================================================
# CONFIGURACIÓN DE COORDENADAS Y DIMENSIONES
# ============================================================================

# Dimensiones de la imagen base (estas se detectan automáticamente)
# grafico_D2.png tiene 562x804 pixels

# Configuración del grid de la imagen D2
# El test D2 tiene 14 filas y aproximadamente 47 posiciones por fila
FILAS = 14
COLUMNAS_MAX = 47

# Márgenes y área útil del gráfico (ajustar según la imagen real)
# Estos valores mapean el área donde están dibujadas las filas del test
MARGEN_SUPERIOR = 80  # Píxeles desde el top hasta la primera fila
MARGEN_INFERIOR = 40  # Píxeles desde la última fila hasta el bottom
MARGEN_IZQUIERDO = 40  # Píxeles desde el left hasta la primera columna
MARGEN_DERECHO = 40  # Píxeles desde la última columna hasta el right

# Posiciones para textos rotados de totales (ajustables)
# Formato: (x, y) en píxeles desde la esquina superior izquierda
POSICIONES_TOTALES = {
    'TR_total': (20, 350),
    'TA_total': (50, 350),
    'O_total': (480, 350),
    'C_total': (510, 350),
}

# Tamaño de fuente para textos
FUENTE_TOTALES_TAMANIO = 16
FUENTE_INDICES_TAMANIO = 12

# Configuración de puntos y líneas
RADIO_PUNTO = 4  # Radio de los puntos negros en píxeles
COLOR_PUNTO = (0, 0, 0, 255)  # Negro
GROSOR_LINEA = 2  # Grosor de las líneas conectoras en píxeles
COLOR_LINEA = (0, 0, 0, 255)  # Negro


# ============================================================================
# FUNCIONES DE MAPEO DE COORDENADAS
# ============================================================================

def calcular_dimensiones_grid(img_width, img_height):
    """
    Calcula las dimensiones útiles del grid en la imagen
    
    Args:
        img_width: Ancho de la imagen en píxeles
        img_height: Alto de la imagen en píxeles
        
    Returns:
        tuple: (area_util_width, area_util_height, x_inicio, y_inicio)
    """
    area_util_width = img_width - MARGEN_IZQUIERDO - MARGEN_DERECHO
    area_util_height = img_height - MARGEN_SUPERIOR - MARGEN_INFERIOR
    x_inicio = MARGEN_IZQUIERDO
    y_inicio = MARGEN_SUPERIOR
    
    return area_util_width, area_util_height, x_inicio, y_inicio


def mapear_fila_columna_a_coordenadas(row, column, img_width, img_height):
    """
    Mapea una posición (fila, columna) del test D2 a coordenadas (x, y) en la imagen
    
    Args:
        row: Número de fila (1-14)
        column: Número de columna/letra (1-47)
        img_width: Ancho de la imagen en píxeles
        img_height: Alto de la imagen en píxeles
        
    Returns:
        tuple: (x, y) coordenadas en píxeles
    """
    area_util_width, area_util_height, x_inicio, y_inicio = calcular_dimensiones_grid(img_width, img_height)
    
    # Calcular espaciado entre filas y columnas
    espaciado_vertical = area_util_height / (FILAS - 1) if FILAS > 1 else area_util_height
    espaciado_horizontal = area_util_width / (COLUMNAS_MAX - 1) if COLUMNAS_MAX > 1 else area_util_width
    
    # Convertir de índices 1-based a 0-based
    fila_idx = row - 1
    columna_idx = column - 1
    
    # Calcular coordenadas
    x = x_inicio + (columna_idx * espaciado_horizontal)
    y = y_inicio + (fila_idx * espaciado_vertical)
    
    return int(x), int(y)


def obtener_posicion_cuadro_texto_fila(row, indice, img_width, img_height):
    """
    Obtiene la posición para un cuadro de texto de índice en una fila específica
    
    Args:
        row: Número de fila (1-14)
        indice: Nombre del índice ('TR', 'TA', 'O', 'C')
        img_width: Ancho de la imagen
        img_height: Alto de la imagen
        
    Returns:
        tuple: (x, y) coordenadas en píxeles para el cuadro de texto
    """
    # Posición base: a la izquierda de la fila
    _, _, _, y_inicio = calcular_dimensiones_grid(img_width, img_height)
    area_util_height = img_height - MARGEN_SUPERIOR - MARGEN_INFERIOR
    espaciado_vertical = area_util_height / (FILAS - 1) if FILAS > 1 else area_util_height
    
    fila_idx = row - 1
    y = y_inicio + (fila_idx * espaciado_vertical)
    
    # Offset horizontal según el índice
    offsets = {
        'TR': 5,
        'TA': 20,
        'O': img_width - 50,
        'C': img_width - 25,
    }
    
    x = offsets.get(indice, 5)
    
    return int(x), int(y - 8)  # Ajuste vertical para centrar texto


# ============================================================================
# FUNCIONES DE DIBUJO
# ============================================================================

def cargar_fuente(tamanio):
    """
    Carga una fuente TrueType o usa fuente por defecto
    
    Args:
        tamanio: Tamaño de la fuente en puntos
        
    Returns:
        ImageFont: Objeto fuente
    """
    try:
        # Intentar cargar fuente TrueType del sistema
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", tamanio)
    except:
        try:
            # Alternativa: fuente arial
            return ImageFont.truetype("arial.ttf", tamanio)
        except:
            # Si falla, usar fuente por defecto
            return ImageFont.load_default()


def dibujar_textos_rotados_totales(draw, resultados, img_width, img_height):
    """
    Dibuja los textos rotados verticalmente con las puntuaciones totales
    
    Args:
        draw: Objeto ImageDraw
        resultados: Dict con puntuaciones (TR_total, TA_total, O_total, C_total)
        img_width: Ancho de la imagen
        img_height: Alto de la imagen
    """
    fuente = cargar_fuente(FUENTE_TOTALES_TAMANIO)
    
    textos = {
        'TR_total': f"TR: {resultados['TR_total']}",
        'TA_total': f"TA: {resultados['TA_total']}",
        'O_total': f"O: {resultados['O_total']}",
        'C_total': f"C: {resultados['C_total']}",
    }
    
    for clave, texto in textos.items():
        x, y = POSICIONES_TOTALES[clave]
        
        # Crear imagen temporal para el texto rotado
        # Calcular tamaño del texto
        bbox = draw.textbbox((0, 0), texto, font=fuente)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Crear imagen temporal con el texto
        txt_img = Image.new('RGBA', (text_width + 10, text_height + 10), (255, 255, 255, 0))
        txt_draw = ImageDraw.Draw(txt_img)
        txt_draw.text((5, 5), texto, font=fuente, fill=(0, 0, 0, 255))
        
        # Rotar la imagen 90 grados (vertical)
        txt_img_rotated = txt_img.rotate(90, expand=True)
        
        # Pegar la imagen rotada en la imagen principal
        # Usar la imagen original como máscara para transparencia
        draw._image.paste(txt_img_rotated, (x, y), txt_img_rotated)


def dibujar_cuadros_texto_por_fila(draw, resultados, img_width, img_height):
    """
    Dibuja cuadros de texto para cada índice en cada fila
    
    Args:
        draw: Objeto ImageDraw
        resultados: Dict con puntuaciones por fila (TR_por_fila, TA_por_fila, O_por_fila, C_por_fila)
        img_width: Ancho de la imagen
        img_height: Alto de la imagen
    """
    fuente = cargar_fuente(FUENTE_INDICES_TAMANIO)
    
    for row in range(1, FILAS + 1):
        idx = row - 1  # Índice 0-based en las listas
        
        # Obtener valores de esta fila
        tr_val = resultados['TR_por_fila'][idx] if idx < len(resultados['TR_por_fila']) else 0
        ta_val = resultados['TA_por_fila'][idx] if idx < len(resultados['TA_por_fila']) else 0
        o_val = resultados['O_por_fila'][idx] if idx < len(resultados['O_por_fila']) else 0
        c_val = resultados['C_por_fila'][idx] if idx < len(resultados['C_por_fila']) else 0
        
        valores = {
            'TR': tr_val,
            'TA': ta_val,
            'O': o_val,
            'C': c_val,
        }
        
        for indice, valor in valores.items():
            x, y = obtener_posicion_cuadro_texto_fila(row, indice, img_width, img_height)
            texto = str(valor)
            draw.text((x, y), texto, font=fuente, fill=(0, 0, 0, 255))


def dibujar_puntos_seleccionados(draw, datos_d2, img_width, img_height):
    """
    Dibuja puntos negros en las posiciones donde selected != 'FALSE'
    
    Nota: El Excel usa 'FALSE' (inglés) para items no seleccionados.
    Esta función dibuja puntos para todos los items donde selected != 'FALSE'.
    
    Args:
        draw: Objeto ImageDraw
        datos_d2: DataFrame con los datos del test D2
        img_width: Ancho de la imagen
        img_height: Alto de la imagen
        
    Returns:
        dict: Diccionario con {row: [(x, y), ...]} de puntos dibujados por fila
    """
    puntos_por_fila = {}
    
    # Filtrar filas donde selected != 'FALSE'
    df_seleccionados = datos_d2[datos_d2['selected'] != 'FALSE'].copy()
    
    for _, fila in df_seleccionados.iterrows():
        row = int(fila['row'])
        column = int(fila['letter_num'])
        
        # Mapear a coordenadas
        x, y = mapear_fila_columna_a_coordenadas(row, column, img_width, img_height)
        
        # Dibujar punto (círculo relleno)
        draw.ellipse(
            [(x - RADIO_PUNTO, y - RADIO_PUNTO), 
             (x + RADIO_PUNTO, y + RADIO_PUNTO)],
            fill=COLOR_PUNTO
        )
        
        # Guardar punto para posterior conexión
        if row not in puntos_por_fila:
            puntos_por_fila[row] = []
        puntos_por_fila[row].append((x, y))
    
    return puntos_por_fila


def conectar_puntos_entre_filas(draw, puntos_por_fila):
    """
    Dibuja líneas conectando el último punto de cada fila con el último de la siguiente
    
    Args:
        draw: Objeto ImageDraw
        puntos_por_fila: Dict con {row: [(x, y), ...]} de puntos por fila
    """
    # Ordenar filas
    filas_ordenadas = sorted(puntos_por_fila.keys())
    
    for i in range(len(filas_ordenadas) - 1):
        fila_actual = filas_ordenadas[i]
        fila_siguiente = filas_ordenadas[i + 1]
        
        # Obtener último punto de cada fila
        if puntos_por_fila[fila_actual] and puntos_por_fila[fila_siguiente]:
            # El último punto es el que tiene mayor coordenada X
            ultimo_actual = max(puntos_por_fila[fila_actual], key=lambda p: p[0])
            ultimo_siguiente = max(puntos_por_fila[fila_siguiente], key=lambda p: p[0])
            
            # Dibujar línea
            draw.line(
                [ultimo_actual, ultimo_siguiente],
                fill=COLOR_LINEA,
                width=GROSOR_LINEA
            )


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def generar_imagen_final(resultados, datos_d2, ruta_grafico_base='grafico_D2.png', 
                        ruta_salida='grafico_D2_final.png'):
    """
    Genera la imagen final grafico_D2_final.png con todas las superposiciones
    
    Args:
        resultados: Dict con puntuaciones directas y por fila
        datos_d2: DataFrame con los datos del test D2
        ruta_grafico_base: Ruta a la imagen base grafico_D2.png
        ruta_salida: Ruta donde guardar grafico_D2_final.png
        
    Returns:
        bool: True si se generó correctamente, False en caso contrario
    """
    try:
        # 1. Cargar imagen base
        if not os.path.exists(ruta_grafico_base):
            print(f"Error: No se encuentra la imagen base en {ruta_grafico_base}")
            return False
        
        img = Image.open(ruta_grafico_base)
        
        # Convertir a RGBA si no lo está (para soportar transparencia)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        img_width, img_height = img.size
        
        # 2. Crear objeto de dibujo
        draw = ImageDraw.Draw(img)
        
        # 3. Dibujar textos rotados de totales
        dibujar_textos_rotados_totales(draw, resultados, img_width, img_height)
        
        # 4. Dibujar cuadros de texto por fila
        dibujar_cuadros_texto_por_fila(draw, resultados, img_width, img_height)
        
        # 5. Dibujar puntos donde selected != FALSO
        puntos_por_fila = dibujar_puntos_seleccionados(draw, datos_d2, img_width, img_height)
        
        # 6. Conectar puntos entre filas
        conectar_puntos_entre_filas(draw, puntos_por_fila)
        
        # 7. Guardar imagen final
        img.save(ruta_salida, 'PNG')
        
        print(f" Imagen final generada exitosamente: {ruta_salida}")
        return True
        
    except Exception as e:
        print(f" Error al generar imagen final: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# FUNCIÓN DE UTILIDAD PARA INTEGRACIÓN
# ============================================================================

def generar_desde_resultados(resultados, script_dir=None):
    """
    Función de conveniencia para generar la imagen desde resultados ya calculados
    
    Args:
        resultados: Dict con puntuaciones y datos_d2 DataFrame
        script_dir: Directorio donde están los archivos (opcional)
        
    Returns:
        bool: True si se generó correctamente
    """
    if script_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    ruta_base = os.path.join(script_dir, 'grafico_D2.png')
    ruta_salida = os.path.join(script_dir, 'grafico_D2_final.png')
    
    # Los resultados deben incluir el DataFrame datos_d2
    if 'datos_d2' not in resultados:
        print("Error: Se necesita el DataFrame 'datos_d2' en resultados")
        return False
    
    return generar_imagen_final(
        resultados, 
        resultados['datos_d2'],
        ruta_base,
        ruta_salida
    )
