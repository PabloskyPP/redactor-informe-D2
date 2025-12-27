"""
Ejemplo de uso del generador de informes Test D2

Este archivo muestra cómo usar el programa paso a paso
"""

# ============================================================================
# CONFIGURACIÓN BÁSICA
# ============================================================================

# 1. Asegúrate de tener instaladas las dependencias
# Ejecuta en la terminal: pip install -r requirements.txt

# 2. Configura las rutas de tu archivo Excel y donde quieres guardar el informe
RUTA_EXCEL = r"C:\Users\Pablo\OneDrive\Escritorio\data\2312_21312.xlsx"
RUTA_SALIDA = r"C:\Users\Pablo\OneDrive\Escritorio\data\Informe_D2_Resultado.docx"

# 3. Configura el nombre del evaluado (opcional - se usará sub_num del Excel si está disponible)
NOMBRE_EVALUADO = "Juan Pérez"

# ============================================================================
# EJECUTAR EL PROGRAMA
# ============================================================================

from lector_datos import leer_datos_excel, calcular_puntuaciones_directas
from reglas_psicometricas import obtener_puntuaciones_tipicas
from generador_docx import crear_informe_docx, guardar_informe


def generar_informe_completo():
    """
    Genera el informe completo del test D2
    """
    print("Iniciando generación de informe...")
    
    # Leer datos
    datos = leer_datos_excel(RUTA_EXCEL)
    print(f"Edad del evaluado: {datos['edad']} años")
    if datos.get('nombre_completo'):
        print(f"Nombre completo: {datos['nombre_completo']}")
        print(f"Nombre: {datos['nombre']}")
    
    # Calcular puntuaciones directas
    resultados = calcular_puntuaciones_directas(datos)
    print("\nPuntuaciones directas calculadas:")
    print(f"  TR total: {resultados['TR_total']}")
    print(f"  TA total: {resultados['TA_total']}")
    print(f"  Errores O: {resultados['O_total']}")
    print(f"  Errores C: {resultados['C_total']}")
    print(f"  CON: {resultados['CON']}")
    print(f"  VAR: {resultados['VAR']}")
    
    # Obtener clasificaciones
    clasificaciones = obtener_puntuaciones_tipicas(resultados)
    print("\nClasificaciones:")
    print(f"  Velocidad (TR): {clasificaciones['TR']}")
    print(f"  Omisiones (O): {clasificaciones['O']}")
    print(f"  Comisiones (C): {clasificaciones['C']}")
    print(f"  Concentración (CON): {clasificaciones['CON']}")
    print(f"  Variabilidad (VAR): {clasificaciones['VAR']}")
    
    # Generar documento
    documento = crear_informe_docx(resultados, clasificaciones, NOMBRE_EVALUADO)
    
    # Guardar
    guardar_informe(documento, RUTA_SALIDA)
    
    print(f"\n✅ Informe generado exitosamente en: {RUTA_SALIDA}")


if __name__ == "__main__":
    generar_informe_completo()


# ============================================================================
# NOTAS IMPORTANTES
# ============================================================================

"""
ESTRUCTURA DEL EXCEL REQUERIDA:

Hoja "info":
  - Columna "age" con la edad del evaluado

Hoja "D2":
  - Columna "row": número de fila (1-14)
  - Columna "letter_number": posición de la letra (1-47)
  - Columna "target": 'si' si es estímulo relevante, 'no' si no lo es
  - Columna "selected": 'TRUE' si fue marcado, 'FALSE' si no

INTERPRETACIÓN DE LAS CLASIFICACIONES:

TR (Velocidad):
  - bajo = lento
  - normal = normal
  - alto = rápido

O (Omisiones):
  - bajo = atento (pocos errores)
  - normal = atención normal
  - alto = despistado (muchos errores)

C (Comisiones):
  - bajo = preciso (pocos errores)
  - normal = precisión normal
  - alto = impreciso (muchos errores)

CON (Concentración):
  - bajo = desconcentrado
  - normal = concentración normal
  - alto = concentrado

VAR (Variabilidad):
  - bajo = muy estable
  - normal = estabilidad normal
  - alto = muy variable
"""
