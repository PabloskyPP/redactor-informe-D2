"""
Módulo para generar el informe en formato DOCX
"""
import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from textos import (
    PARRAFOS_FIJOS, PARRAFOS_VAR, PARRAFOS_TR, 
    PARRAFOS_O, PARRAFOS_C, PARRAFOS_CON,
    SINTESIS_INTRO, obtener_parrafo_cierre, normalizar_nivel
)


def crear_informe_docx(resultados, clasificaciones, nombre_caso="caso"):
    """
    Crea el documento Word con el informe del test D2
    
    Args:
        resultados: Dict con puntuaciones directas
        clasificaciones: Dict con clasificaciones (PT)
        nombre_caso: Nombre del evaluado
        
    Returns:
        Document: Documento Word generado
    """
    doc = Document()
    
    # Configurar márgenes
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
    
    # ========================================================================
    # TÍTULO
    # ========================================================================
    titulo = doc.add_paragraph()
    titulo.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = titulo.add_run(PARRAFOS_FIJOS['titulo'])
    run.bold = True
    run.font.size = Pt(16)
    doc.add_paragraph()  # Espacio
    
    # ========================================================================
    # INTRODUCCIÓN
    # ========================================================================
    doc.add_paragraph(PARRAFOS_FIJOS['introduccion'].format(nombre=nombre_caso))
    doc.add_paragraph()  # Espacio
    
    # ========================================================================
    # DESCRIPCIÓN DE LA PRUEBA
    # ========================================================================
    subtitulo = doc.add_paragraph()
    run = subtitulo.add_run("Descripción de la prueba")
    run.bold = True
    run.font.size = Pt(12)
    
    doc.add_paragraph(PARRAFOS_FIJOS['descripcion_prueba'])
    
    # ========================================================================
    # VARIABLES DEL TEST (Descripción técnica)
    # ========================================================================
    doc.add_paragraph("A continuación, se presenta una relación de las puntuaciones o variables de la prueba; se especifica cómo se obtienen y se dan algunas características de su significación psicológica y psicométrica:")
    
    # TR
    p_tr = doc.add_paragraph()
    p_tr.add_run("TR. ").bold = True
    p_tr.add_run("Esta puntuación alude al número total de elementos procesados o intentados en todo el test. TR es una medida cuantitativa del conjunto total de elementos que se procesaron, tanto los relevantes como los irrelevantes. Es una medida muy fiable y con una distribución normal de la atención (selectiva y sostenida), de la velocidad de procesamiento, de la cantidad de trabajo realizado y de la motivación.")
    
    # E
    p_e = doc.add_paragraph()
    p_e.add_run("E. ").bold = True
    p_e.add_run("Esta puntuación directa E (errores) es la suma de todas las equivocaciones; incluye los errores de omisión (O) y los menos frecuentes errores de comisión (C). Los errores O se dan cuando no se marcan los elementos relevantes. Los errores C se producen cuando se marcan elementos irrelevantes; y la flexibilidad cognitiva. Estos errores son una medida del control atencional, el cumplimiento de una regla, la precisión de la búsqueda visual, la flexibilidad cognitiva y la calidad de la actuación.")
    
    # TOT
    p_tot = doc.add_paragraph()
    p_tot.add_run("TOT. ").bold = True
    p_tot.add_run("Es el número de elementos procesados (TR) menos el número total de errores E cometidos (O + C). Es una medida fiable y con distribución normal de control atencional e inhibitorio y de la relación entre la velocidad y precisión de los sujetos.")
    
    # TA
    p_ta = doc.add_paragraph()
    p_ta.add_run("TA. ").bold = True
    p_ta.add_run("Es el número total de aciertos, las veces que la letra d tenía dos rayas y fue marcada por el sujeto.")
    
    # CON
    p_con = doc.add_paragraph()
    p_con.add_run("CON. ").bold = True
    p_con.add_run("Esta medida (Concentración) se deriva del número de elementos relevantes correctamente marcados (TA) menos el número de comisiones (C).")
    
    # VAR
    p_var = doc.add_paragraph()
    p_var.add_run("VAR. ").bold = True
    p_var.add_run("Esta puntuación de variación viene dada por la diferencia entre la serie de mayor y menor productividad (TR) de las 14 líneas de test.")
    
    doc.add_paragraph()  # Espacio
    
    # ========================================================================
    # INSERTAR GRÁFICO D2
    # ========================================================================
    
    # Título de resultados
    titulo_resultados = doc.add_paragraph()
    titulo_resultados.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = titulo_resultados.add_run(PARRAFOS_FIJOS['titulo_resultados'])
    run.bold = True
    run.font.size = Pt(14)
    doc.add_paragraph()  # Espacio

    # Ruta al gráfico (en el mismo directorio que el script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    grafico_path = os.path.join(script_dir, 'grafico_D2.png')
    
    if os.path.exists(grafico_path):
        # Añadir el gráfico
        # Obtener dimensiones de página (ignorar márgenes como se especifica)
        section = doc.sections[0]
        page_width = section.page_width
        page_height = section.page_height
        
        # Leer dimensiones de la imagen
        from PIL import Image
        try:
            img = Image.open(grafico_path)
            img_width, img_height = img.size
            img_aspect = img_width / img_height
            
            # Calcular el tamaño máximo manteniendo la proporción
            # Usar el ancho de página como límite
            max_width = page_width
            max_height = page_height
            
            # Calcular dimensiones finales
            if img_aspect > (max_width / max_height):
                # La imagen es más ancha proporcionalmente
                final_width = max_width
                final_height = max_width / img_aspect
            else:
                # La imagen es más alta proporcionalmente
                final_height = max_height
                final_width = max_height * img_aspect
            
            # Añadir la imagen al documento
            paragraph_img = doc.add_paragraph()
            paragraph_img.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            run_img = paragraph_img.add_run()
            run_img.add_picture(grafico_path, width=int(final_width * 0.9))  # 90% del ancho para un margen mínimo
        except ImportError:
            # Si PIL no está disponible, usar un tamaño fijo razonable
            paragraph_img = doc.add_paragraph()
            paragraph_img.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            run_img = paragraph_img.add_run()
            run_img.add_picture(grafico_path, width=Inches(7))
    
    doc.add_paragraph()  # Espacio

    # ========================================================================
    # SALTO DE PÁGINA Y RESULTADOS
    # ========================================================================
    doc.add_page_break()
    
    titulo_resumen = doc.add_paragraph()
    run = titulo_resumen.add_run(PARRAFOS_FIJOS['titulo_resumen'].format(nombre=nombre_caso))
    run.bold = True
    run.font.size = Pt(14)
    doc.add_paragraph()  # Espacio
    
    # Tabla con puntuaciones directas
    tabla = doc.add_table(rows=3, cols=8)
    tabla.style = 'Light Grid Accent 1'
    
    # Encabezados
    headers = ['TR', 'TA', 'O', 'C', 'E', 'TOT', 'CON', 'VAR']
    for i, header in enumerate(headers):
        cell = tabla.rows[0].cells[i]
        cell.text = header
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # Puntuaciones directas
    valores = [
        resultados['TR_total'],
        resultados['TA_total'],
        resultados['O_total'],
        resultados['C_total'],
        resultados['E_total'],
        resultados['TOT'],
        resultados['CON'],
        resultados['VAR']
    ]
    for i, valor in enumerate(valores):
        cell = tabla.rows[1].cells[i]
        cell.text = str(valor)
        cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # Clasificaciones (PT)
    clasificaciones_texto = [
        clasificaciones['TR'],
        clasificaciones['TA'],
        clasificaciones['O'],
        clasificaciones['C'],
        '-',
        clasificaciones['TOT'],
        clasificaciones['CON'],
        clasificaciones['VAR']
    ]
    for i, clasif in enumerate(clasificaciones_texto):
        cell = tabla.rows[2].cells[i]
        cell.text = clasif
        cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    doc.add_paragraph()  # Espacio
    
    # ========================================================================
    # RESUMEN DEL RENDIMIENTO
    # ========================================================================
    
    # Párrafos fijos
    doc.add_paragraph(PARRAFOS_FIJOS['rendimiento_general'].format(nombre=nombre_caso))
    doc.add_paragraph()  # Espacio
    
    # ========================================================================
    # PÁRRAFOS CONDICIONALES
    # ========================================================================
    
    # VARIABILIDAD
    p_var_titulo = doc.add_paragraph()
    run = p_var_titulo.add_run("🔹 Variabilidad del rendimiento (VAR)")
    run.bold = True
    run.font.size = Pt(11)
    
    # Seleccionar párrafo VAR según condición especial
    var_key = clasificaciones['VAR']
    if clasificaciones.get('VAR_especial', False) and var_key in ['alto', 'muy alto']:
        var_key = var_key + '_especial'
    
    doc.add_paragraph(PARRAFOS_VAR[var_key].format(nombre=nombre_caso))

    # VELOCIDAD DE PROCESAMIENTO
    p_tr_titulo = doc.add_paragraph()
    run = p_tr_titulo.add_run("🔹 Velocidad de procesamiento (TR)")
    run.bold = True
    run.font.size = Pt(11)
    
    # Normalizar nivel para selección de párrafo
    tr_nivel = normalizar_nivel(clasificaciones['TR'])
    
    doc.add_paragraph(PARRAFOS_TR[tr_nivel])
    
    # ERRORES DE OMISIÓN
    p_o_titulo = doc.add_paragraph()
    run = p_o_titulo.add_run("🔹 Precisión y errores de omisión (O)")
    run.bold = True
    run.font.size = Pt(11)
    
    # Normalizar nivel para selección de párrafo
    o_nivel = normalizar_nivel(clasificaciones['O'])
    
    doc.add_paragraph(PARRAFOS_O[o_nivel])
    
    # ERRORES DE COMISIÓN
    p_c_titulo = doc.add_paragraph()
    run = p_c_titulo.add_run("🔹 Errores de comisión (C)")
    run.bold = True
    run.font.size = Pt(11)
    
    # Normalizar nivel para selección de párrafo
    c_nivel = normalizar_nivel(clasificaciones['C'])
    
    doc.add_paragraph(PARRAFOS_C[c_nivel])
    
    # CONCENTRACIÓN
    p_con_titulo = doc.add_paragraph()
    run = p_con_titulo.add_run("🔹 Concentración (CON)")
    run.bold = True
    run.font.size = Pt(11)
    
    # Normalizar nivel para selección de párrafo
    con_nivel = normalizar_nivel(clasificaciones['CON'])
    
    doc.add_paragraph(PARRAFOS_CON[con_nivel])
    doc.add_paragraph()  # Espacio
    
    # ========================================================================
    # SÍNTESIS FINAL
    # ========================================================================
    p_sintesis_titulo = doc.add_paragraph()
    run = p_sintesis_titulo.add_run("🔹 Síntesis del perfil atencional")
    run.bold = True
    run.font.size = Pt(11)
    
    doc.add_paragraph(SINTESIS_INTRO.format(nombre=nombre_caso))
    
    # Párrafo de cierre según combinación de clasificaciones
    parrafo_cierre = obtener_parrafo_cierre(
        clasificaciones['TR'],
        clasificaciones['O'],
        clasificaciones['C'],
        clasificaciones['CON'],
        clasificaciones['VAR'],
        clasificaciones.get('VAR_especial', False),
        nombre_caso
    )
    doc.add_paragraph(parrafo_cierre)
    
    return doc


def guardar_informe(doc, ruta_salida):
    """
    Guarda el documento generado
    
    Args:
        doc: Documento Word
        ruta_salida: Ruta donde guardar el archivo
    """
    doc.save(ruta_salida)
    print(f"Informe generado exitosamente en: {ruta_salida}")
