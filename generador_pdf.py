"""
Módulo para convertir DOCX a PDF e insertar imagen como página 3
"""
import os
import subprocess
import tempfile
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image
import sys


def convertir_docx_a_pdf(ruta_docx, ruta_pdf):
    """
    Convierte un archivo DOCX a PDF usando Word (Windows) o LibreOffice
    
    Args:
        ruta_docx: Ruta al archivo DOCX
        ruta_pdf: Ruta donde guardar el PDF
        
    Returns:
        bool: True si la conversión fue exitosa, False en caso contrario
    """
    try:
        # Obtener directorio de salida
        directorio_salida = os.path.dirname(ruta_pdf)
        
        # Intentar usar Word si estamos en Windows
        if sys.platform == 'win32':
            try:
                import win32com.client
                
                # Crear instancia de Word
                word = win32com.client.Dispatch('Word.Application')
                word.Visible = False
                
                # Abrir el documento
                doc = word.Documents.Open(ruta_docx)
                
                # Guardar como PDF (formato 17 es PDF)
                doc.SaveAs(ruta_pdf, FileFormat=17)
                
                # Cerrar documento y Word
                doc.Close()
                word.Quit()
                
                return os.path.exists(ruta_pdf)
                
            except ImportError:
                print("    pywin32 no está instalado. Intentando con LibreOffice...")
                print("    Para usar Word, instala: pip install pywin32")
            except Exception as e:
                print(f"    Error al usar Word: {e}")
                print("    Intentando con LibreOffice...")
        
        # Intentar con LibreOffice (fallback o para Linux/Mac)
        # Buscar LibreOffice en ubicaciones comunes de Windows
        posibles_rutas = [
            r'C:\Program Files\LibreOffice\program\soffice.exe',
            r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
            'libreoffice',  # En PATH
            'soffice'  # En PATH
        ]
        
        ejecutable = None
        for ruta in posibles_rutas:
            if os.path.exists(ruta) or ruta in ['libreoffice', 'soffice']:
                ejecutable = ruta
                break
        
        if not ejecutable:
            print("Error: No se encontró LibreOffice instalado")
            print("Instala LibreOffice desde: https://www.libreoffice.org/download/download/")
            print("O instala pywin32 para usar Word: pip install pywin32")
            return False
        
        comando = [
            ejecutable,
            '--headless',
            '--convert-to',
            'pdf',
            '--outdir',
            directorio_salida,
            ruta_docx
        ]
        
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if resultado.returncode != 0:
            print(f"Error al convertir DOCX a PDF: {resultado.stderr}")
            return False
        
        # LibreOffice guarda el PDF con el mismo nombre que el DOCX pero con extensión .pdf
        nombre_base = os.path.splitext(os.path.basename(ruta_docx))[0]
        pdf_generado = os.path.join(directorio_salida, f"{nombre_base}.pdf")
        
        # Si el PDF generado tiene un nombre diferente al deseado, renombrarlo
        if pdf_generado != ruta_pdf and os.path.exists(pdf_generado):
            os.rename(pdf_generado, ruta_pdf)
        
        return os.path.exists(ruta_pdf)
        
    except subprocess.TimeoutExpired:
        print("Error: La conversión de DOCX a PDF excedió el tiempo límite")
        return False
    except Exception as e:
        print(f"Error al convertir DOCX a PDF: {e}")
        return False


def crear_pdf_desde_imagen(ruta_imagen, ruta_pdf_salida):
    """
    Crea un PDF con una sola página conteniendo la imagen
    
    Args:
        ruta_imagen: Ruta a la imagen PNG
        ruta_pdf_salida: Ruta donde guardar el PDF
        
    Returns:
        bool: True si se creó correctamente, False en caso contrario
    """
    try:
        # Abrir la imagen para obtener sus dimensiones
        img = Image.open(ruta_imagen)
        img_width, img_height = img.size
        
        # Calcular el tamaño de página A4 en puntos (1 punto = 1/72 pulgadas)
        page_width, page_height = A4
        
        # Calcular la escala para ajustar la imagen a la página manteniendo proporción
        # Dejar un pequeño margen
        margen = 20
        escala_ancho = (page_width - 2 * margen) / img_width
        escala_alto = (page_height - 2 * margen) / img_height
        escala = min(escala_ancho, escala_alto)
        
        # Dimensiones finales de la imagen
        final_width = img_width * escala
        final_height = img_height * escala
        
        # Calcular posición para centrar la imagen
        x = (page_width - final_width) / 2
        y = (page_height - final_height) / 2
        
        # Crear el PDF con la imagen
        c = canvas.Canvas(ruta_pdf_salida, pagesize=A4)
        c.drawImage(
            ruta_imagen,
            x, y,
            width=final_width,
            height=final_height,
            preserveAspectRatio=True
        )
        c.showPage()
        c.save()
        
        return True
        
    except Exception as e:
        print(f"Error al crear PDF desde imagen: {e}")
        return False


def insertar_imagen_en_pagina_3(ruta_pdf_original, ruta_imagen, ruta_pdf_salida):
    """
    Inserta una imagen como página 3 en un PDF existente
    
    El resultado será:
    - Página 1: contenido original
    - Página 2: contenido original
    - Página 3: imagen grafico_D2_final
    - Página 4+: resto del contenido original
    
    Args:
        ruta_pdf_original: Ruta al PDF original (generado desde DOCX)
        ruta_imagen: Ruta a la imagen PNG a insertar
        ruta_pdf_salida: Ruta donde guardar el PDF final
        
    Returns:
        bool: True si se insertó correctamente, False en caso contrario
    """
    try:
        # Leer el PDF original
        lector_original = PdfReader(ruta_pdf_original)
        num_paginas = len(lector_original.pages)
        
        # Crear PDF temporal con la imagen
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            pdf_imagen_temp = tmp_file.name
        
        if not crear_pdf_desde_imagen(ruta_imagen, pdf_imagen_temp):
            return False
        
        # Leer el PDF con la imagen
        lector_imagen = PdfReader(pdf_imagen_temp)
        pagina_imagen = lector_imagen.pages[0]
        
        # Crear el PDF de salida
        escritor = PdfWriter()
        
        # Copiar las primeras 2 páginas del PDF original
        for i in range(min(2, num_paginas)):
            escritor.add_page(lector_original.pages[i])
        
        # Insertar la página con la imagen (página 3)
        escritor.add_page(pagina_imagen)
        
        # Copiar el resto de las páginas del PDF original (desde la página 3 en adelante)
        for i in range(2, num_paginas):
            escritor.add_page(lector_original.pages[i])
        
        # Guardar el PDF final
        with open(ruta_pdf_salida, 'wb') as archivo_salida:
            escritor.write(archivo_salida)
        
        # Limpiar archivo temporal
        try:
            os.unlink(pdf_imagen_temp)
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"Error al insertar imagen en página 3: {e}")
        return False


def generar_pdf_final(ruta_docx, ruta_imagen, ruta_pdf_salida):
    """
    Función principal que convierte DOCX a PDF e inserta la imagen como página 3
    
    Args:
        ruta_docx: Ruta al archivo DOCX
        ruta_imagen: Ruta a la imagen grafico_D2_final.png
        ruta_pdf_salida: Ruta donde guardar el PDF final
        
    Returns:
        bool: True si todo el proceso fue exitoso, False en caso contrario
    """
    try:
        # Crear un PDF temporal desde el DOCX
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            pdf_temp = tmp_file.name
        
        # Paso 1: Convertir DOCX a PDF
        print("    Convirtiendo DOCX a PDF...")
        if not convertir_docx_a_pdf(ruta_docx, pdf_temp):
            print("    Error al convertir DOCX a PDF")
            return False
        
        # Paso 2: Insertar imagen como página 3
        print("    Insertando imagen como página 3...")
        if not insertar_imagen_en_pagina_3(pdf_temp, ruta_imagen, ruta_pdf_salida):
            print("    Error al insertar imagen en página 3")
            # Limpiar archivo temporal
            try:
                os.unlink(pdf_temp)
            except:
                pass
            return False
        
        # Limpiar archivo temporal
        try:
            os.unlink(pdf_temp)
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"Error en el proceso de generación de PDF: {e}")
        return False
