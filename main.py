"""
Programa principal para generar informe del test D2
"""
import sys
import os
from lector_datos import leer_datos_excel, calcular_puntuaciones_directas, mostrar_celdas_seleccionadas
from reglas_psicometricas import obtener_puntuaciones_tipicas
from generador_docx import crear_informe_docx, guardar_informe
from generador_imagen_final import generar_imagen_final
from generador_pdf import generar_pdf_final


def main():
    """
    Función principal que ejecuta todo el proceso
    """
    # Configuración
    RUTA_EXCEL = r"C:\Users\Pablo\OneDrive\Escritorio\data\Pablo Prada Campello.xlsx"
    
    # Usar la carpeta del script como base para archivos de salida
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Crear directorio de salida si no existe (relativo al script)
    directorio_salida = os.path.join(script_dir, "informes_generados")
    os.makedirs(directorio_salida, exist_ok=True)
    
    NOMBRE_CASO = "pablo"  # Nombre de fallback si no está en el Excel (se usa sub_num si está disponible)
    
    print("=" * 70)
    print("GENERADOR DE INFORME TEST D2 - ATENCIÓN")
    print("=" * 70)
    print()
    
    # Paso 1: Leer datos del Excel
    print("Paso 1: Leyendo datos del archivo Excel...")
    try:
        datos = leer_datos_excel(RUTA_EXCEL)
        print(f"    Edad del evaluado: {datos['edad']} años")
        if datos.get('nombre_completo'):
            print(f"    Nombre completo: {datos['nombre_completo']}")
            print(f"    Nombre: {datos['nombre']}")
        print(f"    Datos del test D2 cargados correctamente")
        
        # Configurar nombres de archivos de salida usando el nombre completo del encuestado
        nombre_completo = datos.get('nombre_completo', NOMBRE_CASO)
        RUTA_SALIDA_DOCX = os.path.join(directorio_salida, f"Informe_D2_{nombre_completo}.docx")
        RUTA_SALIDA_PDF = os.path.join(directorio_salida, f"Informe_D2_{nombre_completo}.pdf")
        RUTA_IMAGEN_FINAL = os.path.join(directorio_salida, "grafico_D2_final.png")
    except Exception as e:
        print(f"   X Error al leer el archivo: {e}")
        sys.exit(1)
    
    print()
    
    # Paso 2: Calcular puntuaciones directas
    print("Paso 2: Calculando puntuaciones directas...")
    try:
        resultados = calcular_puntuaciones_directas(datos)
        print(f"    TR total: {resultados['TR_total']}")
        print(f"    TA total: {resultados['TA_total']}")
        print(f"    O total: {resultados['O_total']}")
        print(f"    C total: {resultados['C_total']}")
        print(f"    E total: {resultados['E_total']}")
        print(f"    TOT: {resultados['TOT']}")
        print(f"    CON: {resultados['CON']}")
        print(f"    TR max: {resultados['TR_max']}")
        print(f"    TR min: {resultados['TR_min']}")
        print(f"    VAR: {resultados['VAR']}")
    except Exception as e:
        print(f"   X Error al calcular puntuaciones: {e}")
        sys.exit(1)
    
    # Mostrar celdas seleccionadas
    try:
        print()
        mostrar_celdas_seleccionadas(resultados)
    except Exception as e:
        print(f"   X Error al mostrar celdas seleccionadas: {e}")
    
    print()
    
    # Paso 3: Generar imagen final grafico_D2_final.png
    print("Paso 3: Generando imagen final con superposiciones...")
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_base = os.path.join(script_dir, 'grafico_D2.png')
        ruta_final = RUTA_IMAGEN_FINAL
        
        exito = generar_imagen_final(resultados, resultados['datos_d2'], ruta_base, ruta_final)
        if exito:
            print(f"    Imagen final generada correctamente: grafico_D2_final.png")
        else:
            print(f"   X Error al generar la imagen final")
            sys.exit(1)
    except Exception as e:
        print(f"   X Error al generar la imagen final: {e}")
        sys.exit(1)
    
    print()
    
    # Paso 4: Obtener puntuaciones típicas (clasificaciones)
    print("Paso 4: Obteniendo puntuaciones típicas (baremos)...")
    try:
        clasificaciones = obtener_puntuaciones_tipicas(resultados)
        print(f"    TR: {clasificaciones['TR']}")
        print(f"    O: {clasificaciones['O']}")
        print(f"    C: {clasificaciones['C']}")
        print(f"    CON: {clasificaciones['CON']}")
        print(f"    VAR: {clasificaciones['VAR']}")
    except Exception as e:
        print(f"   X Error al obtener clasificaciones: {e}")
        sys.exit(1)
    
    print()
    
    # Paso 5: Generar informe DOCX
    print("Paso 5: Generando informe en formato Word...")
    try:
        documento = crear_informe_docx(resultados, clasificaciones, NOMBRE_CASO)
        print(f"    Documento generado correctamente")
    except Exception as e:
        print(f"   X Error al generar el documento: {e}")
        sys.exit(1)
    
    print()
    
    # Paso 6: Guardar el informe DOCX (temporal)
    print("Paso 6: Guardando informe DOCX...")
    try:
        guardar_informe(documento, RUTA_SALIDA_DOCX)
        print(f"    Informe DOCX guardado en: {RUTA_SALIDA_DOCX}")
    except Exception as e:
        print(f"   X Error al guardar el informe: {e}")
        sys.exit(1)
    
    print()
    
    # Paso 7: Convertir DOCX a PDF e insertar imagen como página 3
    print("Paso 7: Generando PDF final con imagen en página 3...")
    try:
        # Obtener ruta de la imagen final desde la carpeta de informes
        ruta_imagen = RUTA_IMAGEN_FINAL
        
        if not os.path.exists(ruta_imagen):
            print(f"   X Error: No se encuentra la imagen en {ruta_imagen}")
            sys.exit(1)
        
        exito = generar_pdf_final(RUTA_SALIDA_DOCX, ruta_imagen, RUTA_SALIDA_PDF)
        if exito:
            print(f"    PDF generado correctamente: {RUTA_SALIDA_PDF}")
        else:
            print(f"   X Error al generar el PDF final")
            sys.exit(1)
    except Exception as e:
        print(f"   X Error al generar PDF: {e}")
        sys.exit(1)
    
    print()
    print("=" * 70)
    print("PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    print()
    print(f"Puede abrir el informe en: {RUTA_SALIDA_PDF}")


if __name__ == "__main__":
    main()