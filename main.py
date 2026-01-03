"""
Programa principal para generar informe del test Raven
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
    RUTA_EXCEL = r"C:\Users\Pablo\OneDrive\Escritorio\data\Pablo Prada Campello.xlsx"
    script_dir = os.path.dirname(RUTA_EXCEL)
    RUTA_SALIDA = os.path.join(script_dir, "Informe_Raven_Resultado.docx")
    RUTA_SALIDA = r"C:\Users\Pablo\OneDrive\Escritorio\data\Informe_Raven_Resultado.docx"
    NOMBRE_CASO = "pablo"  # Nombre de fallback si no está en el Excel (se usa sub_num si está disponible)
    
    print("=" * 70)
    print("GENERADOR DE INFORME TEST RAVEN")
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
    
    # Paso 2: Calcular puntuaciones directas
    print("Paso 2: Calculando puntuaciones directas...")
    try:
        resultados = calcular_puntuaciones_directas(datos)
        print(f"    Puntuación directa A: {resultados['PD_A']}")
        print(f"    Puntuación directa B: {resultados['PD_B']}")
        print(f"    Puntuación directa C: {resultados['PD_C']}")
        print(f"    Puntuación directa D: {resultados['PD_D']}")
        print(f"    Puntuación directa E: {resultados['PD_E']}")
        print(f"    Puntuación directa total: {resultados['PD_total']}")
        print(f"    Discrepancia: {resultados['Discrepancia']}")
    except Exception as e:
        print(f"   X Error al calcular puntuaciones: {e}")
        sys.exit(1)
    
    
    # Paso 4: Obtener puntuaciones típicas (clasificaciones)
    print("Paso 4: Obteniendo puntuaciones típicas (baremos)...")
    try:
        clasificaciones = obtener_puntuaciones_tipicas(resultados)

        print(f"    Percentil: {resultados['Percentil']}")
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
