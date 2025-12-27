"""
Programa principal para generar informe del test D2
"""
import sys
from lector_datos import leer_datos_excel, calcular_puntuaciones_directas
from reglas_psicometricas import obtener_puntuaciones_tipicas
from generador_docx import crear_informe_docx, guardar_informe


def main():
    """
    Función principal que ejecuta todo el proceso
    """
    # Configuración
    RUTA_EXCEL = r"C:\Users\Pablo\OneDrive\Escritorio\data\2312_21312.xlsx"
    RUTA_SALIDA = r"C:\Users\Pablo\OneDrive\Escritorio\data\Informe_D2_Resultado.docx"
    NOMBRE_CASO = "caso"  # Nombre de fallback si no está en el Excel (se usa sub_num si está disponible)
    
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
    
    # Paso 3: Obtener puntuaciones típicas (clasificaciones)
    print("Paso 3: Obteniendo puntuaciones típicas (baremos)...")
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
    
    # Paso 4: Generar informe DOCX
    print("Paso 4: Generando informe en formato Word...")
    try:
        documento = crear_informe_docx(resultados, clasificaciones, NOMBRE_CASO)
        print(f"    Documento generado correctamente")
    except Exception as e:
        print(f"   X Error al generar el documento: {e}")
        sys.exit(1)
    
    print()
    
    # Paso 5: Guardar el informe
    print("Paso 5: Guardando informe...")
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
