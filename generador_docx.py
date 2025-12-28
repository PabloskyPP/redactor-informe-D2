"""
Módulo para generar el informe en formato DOCX
"""
import os
from datetime import datetime
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Emu
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from PIL import Image
from textos import (
    PARRAFOS_FIJOS, PARRAFOS_VAR, PARRAFOS_TR, 
    PARRAFOS_O, PARRAFOS_C, PARRAFOS_CON,
    SINTESIS_INTRO, obtener_parrafo_cierre, normalizar_nivel
)


def agregar_textbox_vertical(paragraph, text, x_pos, y_pos, width=Inches(0.3), height=Inches(1.5)):
    """
    Añade un cuadro de texto rotado verticalmente al párrafo
    
    Args:
        paragraph: Párrafo de docx donde añadir el textbox
        text: Texto a mostrar
        x_pos: Posición X en EMUs
        y_pos: Posición Y en EMUs  
        width: Ancho del cuadro de texto
        height: Alto del cuadro de texto
    
    Note: Esta función usa manipulación XML directa para crear textboxes posicionados
    """
    # Convertir dimensiones a EMUs si son Inches
    if isinstance(width, Inches):
        width = int(width)
    if isinstance(height, Inches):
        height = int(height)
    if isinstance(x_pos, Inches):
        x_pos = int(x_pos)
    if isinstance(y_pos, Inches):
        y_pos = int(y_pos)
    
    # Crear el textbox XML con posicionamiento absoluto y rotación
    # Nota: La rotación vertical se logra con rot="270" (270 grados = rotación hacia la izquierda)
    textbox_xml = f'''
    <w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
         xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
         xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
         xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"
         xmlns:v="urn:schemas-microsoft-com:vml"
         xmlns:w10="urn:schemas-microsoft-com:office:word">
        <w:drawing>
            <wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" 
                       relativeHeight="251659264" behindDoc="0" locked="0" 
                       layoutInCell="1" allowOverlap="1">
                <wp:simplePos x="0" y="0"/>
                <wp:positionH relativeFrom="page">
                    <wp:posOffset>{x_pos}</wp:posOffset>
                </wp:positionH>
                <wp:positionV relativeFrom="page">
                    <wp:posOffset>{y_pos}</wp:posOffset>
                </wp:positionV>
                <wp:extent cx="{width}" cy="{height}"/>
                <wp:effectExtent l="0" t="0" r="0" b="0"/>
                <wp:wrapNone/>
                <wp:docPr id="1" name="Textbox"/>
                <wp:cNvGraphicFramePr/>
                <a:graphic>
                    <a:graphicData uri="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">
                        <wps:wsp xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">
                            <wps:cNvSpPr/>
                            <wps:spPr>
                                <a:xfrm rot="2700000">
                                    <a:off x="0" y="0"/>
                                    <a:ext cx="{width}" cy="{height}"/>
                                </a:xfrm>
                                <a:prstGeom prst="rect">
                                    <a:avLst/>
                                </a:prstGeom>
                                <a:noFill/>
                                <a:ln>
                                    <a:noFill/>
                                </a:ln>
                            </wps:spPr>
                            <wps:txbx>
                                <w:txbxContent>
                                    <w:p>
                                        <w:r>
                                            <w:rPr>
                                                <w:sz w:val="20"/>
                                                <w:b/>
                                            </w:rPr>
                                            <w:t>{text}</w:t>
                                        </w:r>
                                    </w:p>
                                </w:txbxContent>
                            </wps:txbx>
                            <wps:bodyPr rot="0" vert="wordArtVert"/>
                        </wps:wsp>
                    </a:graphicData>
                </a:graphic>
            </wp:anchor>
        </w:drawing>
    </w:r>
    '''
    
    # Parsear el XML y añadirlo al párrafo
    try:
        textbox_element = parse_xml(textbox_xml)
        paragraph._p.append(textbox_element)
    except Exception as e:
        # Si hay error en la creación del textbox, registrar advertencia pero continuar
        # para no romper el documento
        import warnings
        warnings.warn(f"No se pudo crear textbox: {e}")


def agregar_portada(doc: Document, nombre_completo: str, datos: dict) -> None:
    """
    Agrega la portada del informe
    
    Args:
        doc: Documento de Word
        nombre_completo: Nombre completo del encuestado
        datos: Diccionario con datos generales (edad, fecha_aplicacion, etc.)
    """
    # Título
    titulo = doc.add_heading('D2, TEST DE ATENCIÓN', 0)
    titulo.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    # Aumentar tamaño de fuente del título
    for run in titulo.runs:
        run.font.size = Pt(24)
    
    # Espacio
    doc.add_paragraph().add_run().add_break()
    
    # Información del participante
    info = doc.add_paragraph()
    info.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # Nombre del encuestado
    nombre_run = info.add_run(f"Nombre del encuestado: {nombre_completo}\n")
    nombre_run.bold = True
    nombre_run.font.size = Pt(14)
    
    # Edad
    if datos.get('edad'):
        edad_run = info.add_run(f"Edad: {datos['edad']} años\n")
        edad_run.font.size = Pt(14)
    
    # Fecha de aplicación (si está disponible)
    if datos.get('fecha_aplicacion'):
        fecha_app_run = info.add_run(f"Fecha de aplicación: {datos['fecha_aplicacion']}\n")
        fecha_app_run.font.size = Pt(14)
    
    # Fecha del informe
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    fecha_informe_run = info.add_run(f"Fecha del informe: {fecha_actual}\n")
    fecha_informe_run.font.size = Pt(14)
    
    # Espacio
    doc.add_paragraph().add_run().add_break()
    
    # Nota confidencial
    nota = doc.add_paragraph()
    nota.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    nota_run = nota.add_run(f"Este es un informe de evaluación cognitiva, obtenido a partir del rendimiento de {nombre_completo} en la prueba D2, test de atención.")
    nota.add_run("\nInforme confidencial de uso profesional y educativo")
    nota_run.italic = True
    nota_run.font.size = Pt(12)

def crear_informe_docx(resultados, clasificaciones, nombre_caso="caso"):
    """
    Crea el documento Word con el informe del test D2
    
    Args:
        resultados: Dict con puntuaciones directas y datos del encuestado
        clasificaciones: Dict con clasificaciones (PT)
        nombre_caso: Nombre del evaluado (fallback si no está en resultados)
        
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
    
    # Extraer nombres de resultados
    nombre_completo = resultados.get('nombre_completo') or nombre_caso
    nombre = resultados.get('nombre') or nombre_caso
    
    # Preparar datos para la portada
    datos_portada = {
        'edad': resultados.get('edad'),
        'fecha_aplicacion': resultados.get('fecha_aplicacion')
    }
    
    # 1. PORTADA (Primera página)
    agregar_portada(doc, nombre_completo, datos_portada)
    doc.add_page_break()
    
    # ========================================================================
    # TÍTULO E INTRODUCCIÓN
    # ========================================================================
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

    # Ruta al gráfico final (en el mismo directorio que el script)
    # Ahora usamos grafico_D2_final.png que incluye todas las superposiciones
    script_dir = os.path.dirname(os.path.abspath(__file__))
    grafico_path = os.path.join(script_dir, 'grafico_D2_final.png')
    
    if os.path.exists(grafico_path):
        # Añadir el gráfico con dimensionamiento mejorado
        # Obtener dimensiones de página (ignorar márgenes como se especifica en issue)
        section = doc.sections[-1]
        page_width = section.page_width
        page_height = section.page_height
        
        # Leer dimensiones de la imagen
        try:
            img = Image.open(grafico_path)
            img_width, img_height = img.size
            img_aspect = img_width / img_height
            page_aspect = page_width / page_height
            
            # Calcular dimensiones finales para ajustar tanto al techo como a la base
            # manteniendo la proporción y sin deformación
            if img_aspect > page_aspect:
                # La imagen es más ancha proporcionalmente - limitar por ancho
                final_width = page_width
                final_height = page_width / img_aspect
            else:
                # La imagen es más alta proporcionalmente - limitar por alto
                final_height = page_height
                final_width = page_height * img_aspect
            
            # Añadir la imagen al documento con el tamaño calculado
            paragraph_img = doc.add_paragraph()
            paragraph_img.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            run_img = paragraph_img.add_run()
            picture = run_img.add_picture(grafico_path, width=int(final_width), height=int(final_height))
            
        except Exception as e:
            # Si hay algún error, usar un tamaño fijo razonable
            paragraph_img = doc.add_paragraph()
            paragraph_img.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            run_img = paragraph_img.add_run()
            run_img.add_picture(grafico_path, width=Inches(7))
    
    doc.add_paragraph()  # Espacio

    # ========================================================================
    # SALTO DE PÁGINA Y RESULTADOS
    # ========================================================================
    
    titulo_resumen = doc.add_paragraph()
    run = titulo_resumen.add_run(PARRAFOS_FIJOS['titulo_resumen'].format(nombre=nombre))
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
    doc.add_paragraph(PARRAFOS_FIJOS['rendimiento_general'].format(nombre=nombre))
    doc.add_paragraph()  # Espacio
    
    # ========================================================================
    # PÁRRAFOS CONDICIONALES
    # ========================================================================
    
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

        # VARIABILIDAD
    p_var_titulo = doc.add_paragraph()
    run = p_var_titulo.add_run("🔹 Variabilidad del rendimiento (VAR)")
    run.bold = True
    run.font.size = Pt(11)
    
    # Seleccionar párrafo VAR según condición especial
    var_key = clasificaciones['VAR']
    if clasificaciones.get('VAR_especial', False) and var_key in ['alto', 'muy alto']:
        var_key = var_key + '_especial'
    
    doc.add_paragraph(PARRAFOS_VAR[var_key].format(nombre=nombre))

    doc.add_paragraph()  # Espacio
    
    # ========================================================================
    # SÍNTESIS FINAL
    # ========================================================================
    p_sintesis_titulo = doc.add_paragraph()
    run = p_sintesis_titulo.add_run("🔹 Síntesis del perfil atencional")
    run.bold = True
    run.font.size = Pt(11)
    
    doc.add_paragraph(SINTESIS_INTRO.format(nombre=nombre))
    
    # Párrafo de cierre según combinación de clasificaciones
    parrafo_cierre = obtener_parrafo_cierre(
        clasificaciones['TR'],
        clasificaciones['O'],
        clasificaciones['C'],
        clasificaciones['CON'],
        clasificaciones['VAR'],
        clasificaciones.get('VAR_especial', False),
        nombre
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
