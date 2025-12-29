"""
Programa principal para generar informe del test D2
"""
import sys
import os
from lector_datos import leer_datos_excel, calcular_puntuaciones_directas, mostrar_celdas_seleccionadas
from reglas_psicometricas import obtener_puntuaciones_tipicas
from generador_docx import crear_informe_docx, guardar_informe
from generador_imagen_final import generar_imagen_final


def main():
    """
    Función principal que ejecuta todo el proceso
    """
    # Configuración
    RUTA_EXCEL = r"C:\Users\Pablo\OneDrive\Escritorio\data\pablo prada_1.xlsx"
    script_dir = os.path.dirname(RUTA_EXCEL)
    RUTA_SALIDA = os.path.join(script_dir, "Informe_D2_Resultado.docx")
    RUTA_IMAGEN_FINAL = os.path.join(script_dir, "grafico_D2_final.png")
    RUTA_SALIDA = r"C:\Users\Pablo\OneDrive\Escritorio\data\Informe_D2_Resultado.docx"
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
    except Exception as e:
        print(f"   X Error al leer el archivo: {e}")
        sys.exit(1)
    
    print()

    # Mostrar celdas seleccionadas
    mostrar_celdas_seleccionadas(resultados)

    
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
    
    print()
    
    # Paso 3: Generar imagen final grafico_D2_final.png
    print("Paso 3: Generando imagen final con superposiciones...")
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_base = os.path.join(script_dir, 'grafico_D2.png')
        ruta_final = os.path.join(script_dir, 'grafico_D2_final.png')
        
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
    
    # Paso 6: Guardar el informe
    print("Paso 6: Guardando informe...")
    try:
        guardar_informe(documento, RUTA_SALIDA)
        print(f"    Informe guardado en: {RUTA_SALIDA}")
    except Exception as e:
        print(f"   X Error al guardar el informe: {e}")
        sys.exit(1)
    
    print()
    print("=" * 70)
    print("PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    print()
    print(f"Puede abrir el informe en: {RUTA_SALIDA}")


if __name__ == "__main__":
    main()
